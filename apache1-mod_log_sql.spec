# TODO
# - split *.so to subpackages: mysql/dbi/ssl
%define		mod_name	log_sql
%define		apxs		/usr/sbin/apxs1
Summary:	SQL logging module for Apache
Summary(pl.UTF-8):	Moduł logowania zapytań do Apache do bazy SQL
Name:		apache1-mod_%{mod_name}
# NOTE: remember about apache-mod_log_sql when updating!
Version:	1.99
Release:	6
License:	Apache (?)
Group:		Networking/Daemons
Source0:	http://www.outoforder.cc/downloads/mod_log_sql/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e246a3d8e96d2d62715eb34f75c7c11d
Patch0:		mod_%{mod_name}-acam_libexecdir.patch
Patch1:		mod_%{mod_name}-subdirs.patch
URL:		http://www.outoforder.cc/projects/apache/mod_log_sql/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	apache1-mod_ssl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdbi-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 3.23.30
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_log_sql <= 1.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_log_sql is a logging module for Apache 1.3 and 2.0 which logs all
requests to a database.

%description -l pl.UTF-8
mod_log_sql jest modułem logującym dla Apache 1.3 i 2.0, który pozwala
na logowanie wszystkich zapytań do bazy danych.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0
%patch1 -p1

rm -f docs/{Makefile*,*.xml} contrib/Makefile*

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install *.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1.99-2.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG TODO contrib docs LICENSE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
