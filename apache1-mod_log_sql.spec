# todo: split *.so to subpackages: mysql/dbi/ssl
%define		mod_name	log_sql
%define		apxs		/usr/sbin/apxs1
Summary:	SQL logging module for Apache
Summary(pl):	Modu³ logowania zapytañ do Apache do bazy SQL
Name:		apache1-mod_%{mod_name}
# NOTE: remember about apache-mod_log_sql when updating!
Version:	1.99
Release:	2
License:	Apache (?)
Group:		Networking/Daemons
Source0:	http://www.outoforder.cc/downloads/mod_log_sql/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e246a3d8e96d2d62715eb34f75c7c11d
Patch0:		mod_%{mod_name}-acam_libexecdir.patch
URL:		http://www.outoforder.cc/projects/apache/mod_log_sql/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.20
BuildRequires:	apache1-mod_ssl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdbi-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 3.23.30
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache1
Obsoletes:	apache-mod_log_sql <= 1.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_log_sql is a logging module for Apache 1.3 and 2.0 which logs all requests
to a database.

%description -l pl
mod_log_sql jest modu³em loguj±cym dla Apache 1.3 i 2.0, który pozwala na
logowanie wszystkich zapytañ do bazy danych.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pkglibdir}}

install *.so $RPM_BUILD_ROOT%{_pkglibdir}
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

rm docs/Makefile* docs/*.xml contrib/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_libexecdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_libexecdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG TODO contrib docs LICENSE
%attr(755,root,root) %{_pkglibdir}/*
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
