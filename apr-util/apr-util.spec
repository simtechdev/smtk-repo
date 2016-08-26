###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

###############################################################################

%define apu_version 1

###############################################################################

Summary:           Apache Portable Runtime Utility library
Name:              apr-util
Version:           1.5.4
Release:           0%{?dist}
Group:             System Environment/Libraries
License:           APL
URL:               https://apr.apache.org/

Source0:           http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     autoconf libtool doxygen apr-devel >= 1.4.0
BuildRequires:     expat-devel libuuid-devel postgresql-devel
BuildRequires:     db4-devel mysql-devel sqlite-devel >= 3.0.0
BuildRequires:     freetds-devel unixODBC-devel openldap-devel
BuildRequires:     nss-devel openssl-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

###############################################################################

%package devel
Summary:           APR utility library development kit
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description devel
This package provides the support files which can be used to
build applications using the APR utility library.  The mission
of the Apache Portable Runtime (APR) is to provide a free
library of C data structures and routines.

###############################################################################

%package dbm
Summary:           APR utility library DBM driver
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description dbm
This package provides the DBM driver for the apr-util.

###############################################################################

%package pgsql
Summary:           APR utility library PostgreSQL DBD driver
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description pgsql
This package provides the PostgreSQL driver for the apr-util
DBD (database abstraction) interface.

###############################################################################

%package mysql
Summary:           APR utility library MySQL DBD driver
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.

###############################################################################

%package sqlite
Summary:           APR utility library SQLite DBD driver
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

###############################################################################

%package freetds
Summary:           APR utility library FreeTDS DBD driver
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description freetds
This package provides the FreeTDS driver for the apr-util DBD
(database abstraction) interface.

###############################################################################

%package odbc
Summary:           APR utility library ODBC DBD driver
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.

###############################################################################

%package ldap
Summary:           APR utility library LDAP support
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description ldap
This package provides the LDAP support for the apr-util.

###############################################################################

%package openssl
Summary:           APR utility library OpenSSL crypto support
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description openssl
This package provides crypto support for apr-util based on OpenSSL.

###############################################################################

%package nss
Summary:           APR utility library NSS crypto support
Group:             Development/Libraries

Requires:          %{name} = %{version}-%{release}

%description nss
This package provides crypto support for apr-util based on Mozilla NSS.

###############################################################################

%prep
%setup -q

%build
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apu_version} \
        --with-ldap \
        --without-gdbm \
        --with-sqlite3 \
        --with-pgsql \
        --with-mysql \
        --with-freetds \
        --with-odbc \
        --with-berkeley-db \
        --with-crypto \
        --with-openssl \
        --with-nss \
        --without-sqlite2
%{__make} %{?_smp_mflags}
%{__make} dox

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/aprutil.exp
mv docs/dox/html html

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/libaprutil-%{apu_version}.so.*
%dir %{_libdir}/%{name}-%{apu_version}

%files dbm
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_dbm_db*

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_dbd_pgsql*

%files mysql
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_dbd_mysql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_dbd_sqlite*

%files freetds
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_dbd_freetds*

%files odbc
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_dbd_odbc*

%files ldap
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_ldap*

%files openssl
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_crypto_openssl*

%files nss
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apu_version}/apr_crypto_nss*

%files devel
%defattr(-,root,root,-)
%doc html
%{_bindir}/apu-%{apu_version}-config
%{_libdir}/libaprutil-%{apu_version}.*a
%{_libdir}/libaprutil-%{apu_version}.so
%{_pkgconfigdir}/%{name}-%{apu_version}.pc
%{_includedir}/apr-%{apu_version}/*.h

###############################################################################

%changelog
* Sat Apr 09 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.5.4-0
- Initial build

