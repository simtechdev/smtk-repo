################################################################################

# Global variables
%define _name             php
%define pkg_name          %{name}
%define _root_sysconfdir  %{_sysconfdir}
%define _root_bindir      %{_bindir}
%define _root_sbindir     %{_sbindir}
%define _root_includedir  %{_includedir}
%define _root_libdir      %{_libdir}
%define _root_prefix      %{_prefix}
%define _root_initddir    %{_initrddir}

# API/ABI check
%define apiver      20131106
%define zendver     20131226
%define pdover      20080721

# Extension version
%define fileinfover 1.0.5
%define pharver     2.0.2
%define zipver      1.12.5
%define jsonver     1.2.1
%define opcachever  7.0.6-dev

# Adds -z now to the linker flags
%define _hardened_build 1

# Version (used for php embedded library soname)
%define embed_version 5.6

# MySQL socket and binary path
%define mysql_sock     %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)
%define mysql_config   %{_root_libdir}/mysql/mysql_config

# Enable systemd
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%define with_systemd 1
%else
%define with_systemd 0
%endif

# PHP-FPM
%ifarch %{ix86} x86_64
%define with_fpm 1
%else
%define with_fpm 0
%endif

%define with_libmysql   1
%define with_zts        1
%define with_dtrace     1
%define with_phpdbg     1
%define with_ldap       1

%if 0%{?__isa_bits:1}
%define isasuffix -%{__isa_bits}
%else
%define isasuffix %nil
%endif

%define _httpd_mmn         %(cat %{_root_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)
%define _httpd_confdir     %{_root_sysconfdir}/httpd/conf.d
%define _httpd_moddir      %{_libdir}/httpd/modules
%define _root_httpd_moddir %{_root_libdir}/httpd/modules

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 6
# httpd/2.4
%define _httpd_apxs        %{_root_bindir}/apxs
%define _httpd_modconfdir  %{_root_sysconfdir}/httpd/conf.modules.d
%define _httpd_contentdir  /usr/share/httpd
%else
# httpd/2.2
%define _httpd_apxs        %{_root_sbindir}/apxs
%define _httpd_modconfdir  %{_root_sysconfdir}/httpd/conf.d
%define _httpd_contentdir  /var/www
%endif

# Temporary files
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%define with_tmpfiles 1
%else
%define with_tmpfiles 0
%endif

%define with_zip     1
%define with_libzip  0
%define zipmod       zip

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%define db_devel  db4-devel
%else
%define db_devel  libdb-devel
%endif

################################################################################

Summary:          PHP scripting language for creating dynamic web sites
Name:             php56
Version:          5.6.20
Release:          0%{?dist}
License:          PHP and Zend and BSD
Group:            Development/Languages
URL:              http://www.php.net/

Source0:          https://secure.php.net/distributions/php-%{version}%{?rcver}.tar.bz2
Source1:          php.conf
Source2:          php.ini
Source3:          macros.php
Source4:          php-fpm.conf
Source5:          php-fpm-www.conf
Source6:          php-fpm.service
Source7:          php-fpm.logrotate
Source8:          php-fpm.sysconfig
Source9:          php.modconf
Source10:         php.ztsmodconf
Source11:         php-fpm.init

Source50:         opcache.ini
Source51:         opcache-default.blacklist

Patch5:           php-5.2.0-includedir.patch
Patch6:           php-5.2.4-embed.patch
Patch7:           php-5.3.0-recode.patch
Patch8:           php-5.6.17-libdb.patch

Patch21:          php-5.4.7-odbctimer.patch

Patch40:          php-5.4.0-dlopen.patch
Patch42:          php-5.6.13-systzdata-v13.patch
Patch43:          php-5.4.0-phpize.patch
Patch45:          php-5.4.8-ldap_r.patch
Patch46:          php-5.4.9-fixheader.patch
Patch47:          php-5.4.9-phpinfo.patch
Patch48:          php-5.5.0-icuconfig.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    bzip2-devel, curl-devel >= 7.9, gmp-devel
BuildRequires:    httpd-devel >= 2.0.46-1, pam-devel
BuildRequires:    libstdc++-devel, openssl-devel

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:    sqlite-devel >= 3.6.0
%else
BuildRequires:    sqlite-devel >= 3.0.0
%endif

BuildRequires:    zlib-devel, pcre-devel >= 6.6, smtpdaemon, libedit-devel
BuildRequires:    bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires:    libtool-ltdl-devel

%if %{with_libzip}
BuildRequires:    libzip-devel >= 0.11
%endif

Requires:         httpd-mmn = %{_httpd_mmn}
Requires:         %{name}-common%{?_isa} = %{version}-%{release}
Requires:         %{name}-cli = %{version}-%{release}
Requires:         %{name}-cli%{?_isa} = %{version}-%{release}

Requires(pre):    httpd

%if %{with_dtrace}
BuildRequires:    systemtap-sdt-devel
%endif

%if %{with_zts}
Provides:         php-zts = %{version}-%{release}
Provides:         php-zts%{?_isa} = %{version}-%{release}
%endif

Provides:         php = %{version}-%{release}
Provides:         php%{?_isa} = %{version}-%{release}
Provides:         mod_php = %{version}-%{release}

%if %{with_zts}
Provides:         %{name}-zts = %{version}-%{release}
Provides:         %{name}-zts%{?_isa} = %{version}-%{release}
%endif

# Don't provides extensions, which are not shared library, as .so
%{?filter_provides_in: %filter_provides_in %{_libdir}/php/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_libdir}/php-zts/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}

################################################################################

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The %{name} package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

################################################################################

%package cli
Group:            Development/Languages
Summary:          Command-line interface for PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}
Provides:         php-cgi = %{version}-%{release}
Provides:         php-cgi%{?_isa} = %{version}-%{release}
Provides:         php-pcntl = %{version}-%{release}
Provides:         php-pcntl%{?_isa} = %{version}-%{release}
Provides:         php-readline = %{version}-%{release}
Provides:         php-readline%{?_isa} = %{version}-%{release}
Provides:         php-cli = %{version}-%{release}
Provides:         php-cli%{?_isa} = %{version}-%{release}

%description cli
The %{name}-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.

################################################################################

%if %{with_phpdbg}
%package phpdbg
Group:            Development/Languages
Summary:          Interactive PHP debugger

BuildRequires:    readline-devel

Requires:         %{name}-common%{?_isa} = %{version}-%{release}
Provides:         php-phpdbg = %{version}-%{release}
Provides:         php-phpdbg%{?_isa} = %{version}-%{release}

%description phpdbg
Implemented as a SAPI module, phpdbg can excert complete control over
the environment without impacting the functionality or performance of
your code.

phpdbg aims to be a lightweight, powerful, easy to use debugging
platform for PHP
%endif

################################################################################

%if %{with_fpm}
%package fpm
Group:            Development/Languages
Summary:          PHP FastCGI Process Manager
License:          PHP and Zend and BSD

BuildRequires:    libevent-devel >= 1.4.11

%if %{with_systemd}
BuildRequires:    systemd-devel
BuildRequires:    systemd-units

Requires:         systemd-units

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(post):   systemd-sysv
%endif

Requires(pre):    /usr/sbin/useradd

Requires:         %{name}-common%{?_isa} = %{version}-%{release}
Provides:         php-fpm = %{version}-%{release}
Provides:         php-fpm%{?_isa} = %{version}-%{release}

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

################################################################################

%package common
Group:            Development/Languages
Summary:          Common files for PHP
License:          PHP and BSD and ASL 1.0

Provides:         php(api) = %{apiver}%{isasuffix}
Provides:         php(zend-abi) = %{zendver}%{isasuffix}

Provides:         %{name}-bz2 = %{version}
Provides:         %{name}-bz2%{?_isa} = %{version}

Provides:         %{name}-calendar = %{version}
Provides:         %{name}-calendar%{?_isa} = %{version}

Provides:         %{name}-core = %{version}
Provides:         %{name}-core%{?_isa} = %{version}

Provides:         %{name}-ctype = %{version}
Provides:         %{name}-ctype%{?_isa} = %{version}

Provides:         %{name}-curl = %{version}
Provides:         %{name}-curl%{?_isa} = %{version}

Provides:         %{name}-date = %{version}
Provides:         %{name}-date%{?_isa} = %{version}

Provides:         %{name}-ereg = %{version}
Provides:         %{name}-ereg%{?_isa} = %{version}

Provides:         %{name}-exif = %{version}
Provides:         %{name}-exif%{?_isa} = %{version}

Provides:         %{name}-fileinfo = %{version}
Provides:         %{name}-fileinfo%{?_isa} = %{version}

Provides:         %{name}-pecl-Fileinfo = %{fileinfover}
Provides:         %{name}-pecl-Fileinfo%{?_isa} = %{fileinfover}

Provides:         %{name}-pecl(Fileinfo) = %{fileinfover}
Provides:         %{name}-pecl(Fileinfo)%{?_isa} = %{fileinfover}

Provides:         %{name}-filter = %{version}
Provides:         %{name}-filter%{?_isa} = %{version}

Provides:         %{name}-ftp = %{version}
Provides:         %{name}-ftp%{?_isa} = %{version}

Provides:         %{name}-gettext = %{version}
Provides:         %{name}-gettext%{?_isa} = %{version}

Provides:         %{name}-gmp = %{version}
Provides:         %{name}-gmp%{?_isa} = %{version}

Provides:         %{name}-hash = %{version}
Provides:         %{name}-hash%{?_isa} = %{version}

Provides:         %{name}-mhash = %{version}
Provides:         %{name}-mhash%{?_isa} = %{version}

Provides:         %{name}-iconv = %{version}
Provides:         %{name}-iconv%{?_isa} = %{version}

Provides:         %{name}-json = %{version}
Provides:         %{name}-json%{?_isa} = %{version}

Provides:         %{name}-pecl-json = %{jsonver}
Provides:         %{name}-pecl-json%{?_isa} = %{jsonver}

Provides:         %{name}-pecl(json) = %{jsonver}
Provides:         %{name}-pecl(json)%{?_isa} = %{jsonver}

Provides:         %{name}-libxml = %{version}
Provides:         %{name}-libxml%{?_isa} = %{version}

Provides:         %{name}-openssl = %{version}
Provides:         %{name}-openssl%{?_isa} = %{version}

Provides:         %{name}-pecl-phar = %{pharver}
Provides:         %{name}-pecl-phar%{?_isa} = %{pharver}

Provides:         %{name}-pecl(phar) = %{pharver}
Provides:         %{name}-pecl(phar)%{?_isa} = %{pharver}

Provides:         %{name}-phar = %{version}
Provides:         %{name}-phar%{?_isa} = %{version}

Provides:         %{name}-pcre = %{version}
Provides:         %{name}-pcre%{?_isa} = %{version}

Provides:         %{name}-reflection = %{version}
Provides:         %{name}-reflection%{?_isa} = %{version}

Provides:         %{name}-session = %{version}
Provides:         %{name}-session%{?_isa} = %{version}

Provides:         %{name}-shmop = %{version}
Provides:         %{name}-shmop%{?_isa} = %{version}

Provides:         %{name}-simplexml = %{version}
Provides:         %{name}-simplexml%{?_isa} = %{version}

Provides:         %{name}-sockets = %{version}
Provides:         %{name}-sockets%{?_isa} = %{version}

Provides:         %{name}-spl = %{version}
Provides:         %{name}-spl%{?_isa} = %{version}

Provides:         %{name}-standard = %{version}
Provides:         %{name}-standard%{?_isa} = %{version}

Provides:         %{name}-tokenizer = %{version}
Provides:         %{name}-tokenizer%{?_isa} = %{version}

%if %{with_zip}
Provides:         %{name}-zip = %{version}
Provides:         %{name}-zip%{?_isa} = %{version}

Provides:         %{name}-pecl-zip = %{zipver}
Provides:         %{name}-pecl-zip%{?_isa} = %{zipver}

Provides:         %{name}-pecl(zip) = %{zipver}
Provides:         %{name}-pecl(zip)%{?_isa} = %{zipver}
%endif

Provides:         %{name}-zlib = %{version}
Provides:         %{name}-zlib%{?_isa} = %{version}

%description common
The %{name}-common package contains files used by both the %{name}
package and the %{name}-cli package.

################################################################################

%package devel
Group:            Development/Libraries
Summary:          Files needed for building PHP extensions

Requires:         %{name}-cli%{?_isa} = %{version}-%{release}, autoconf, automake
Requires:         pcre-devel%{?_isa}

%if %{with_zts}
Provides:         php-zts-devel = %{version}-%{release}
Provides:         php-zts-devel%{?_isa} = %{version}-%{release}
%endif

Provides:         php-devel = %{version}-%{release}
Provides:         php-devel%{?_isa} = %{version}-%{release}

%if %{with_zts}
Provides:         %{name}-zts-devel = %{version}-%{release}
Provides:         %{name}-zts-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
The %{name}-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

################################################################################

%package imap
Summary:          A module for PHP applications that use IMAP
Group:            Development/Languages

Requires:         %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires:    krb5-devel, openssl-devel, libc-client-devel

Provides:         php-imap = %{version}-%{release}
Provides:         php-imap%{?_isa} = %{version}-%{release}

%description imap
The %{name}-imap package contains a dynamic shared object that will
add support for the IMAP protocol to PHP.

################################################################################

%if %{with_ldap}
%package ldap
Summary:          A module for PHP applications that use LDAP
Group:            Development/Languages
License:          PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:    cyrus-sasl-devel, openldap-devel, openssl-devel

Provides:         php-ldap = %{version}-%{release}
Provides:         php-ldap%{?_isa} = %{version}-%{release}

%description ldap
The %{name}-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.
%endif

################################################################################

%package pdo
Summary:          A database access abstraction module for PHP applications
Group:            Development/Languages
License:          PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}
Provides:         php-pdo-abi = %{pdover}%{isasuffix}
Provides:         php(pdo-abi) = %{pdover}%{isasuffix}

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
Provides:         php-sqlite3 = %{version}
Provides:         php-sqlite3%{?_isa} = %{version}
%endif

Provides:         php-pdo_sqlite = %{version}
Provides:         php-pdo_sqlite3%{?_isa} = %{version}
Provides:         php-pdo = %{version}-%{release}
Provides:         php-pdo%{?_isa} = %{version}-%{release}

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
Provides:         %{name}-sqlite3 = %{version}
Provides:         %{name}-sqlite3%{?_isa} = %{version}
%endif

Provides:         %{name}-pdo_sqlite = %{version}
Provides:         %{name}-pdo_sqlite%{?_isa} = %{version}

%description pdo
The %{name}-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

################################################################################

%if %{with_libmysql}
%package          mysql
Summary:          A module for PHP applications that use MySQL databases
Group:            Development/Languages
License:          PHP

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
BuildRequires:    mysql-devel > 4.1.0
%else
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:    mysql-devel < 5.2
%else
BuildRequires:    mysql-devel < 5.1
%endif
%endif

Requires:         %{name}-pdo%{?_isa}

Provides:         php_database = %{version}-%{release}
Provides:         php-mysqli = %{version}-%{release}
Provides:         php-mysqli%{?_isa} = %{version}-%{release}
Provides:         php-pdo_mysql = %{version}-%{release}
Provides:         php-pdo_mysql%{?_isa} = %{version}-%{release}
Provides:         php-mysql = %{version}-%{release}
Provides:         php-mysql%{?_isa} = %{version}-%{release}

Provides:         %{name}-mysqli = %{version}-%{release}
Provides:         %{name}-mysqli%{?_isa} = %{version}-%{release}
Provides:         %{name}-pdo_mysql = %{version}-%{release}
Provides:         php%{name}pdo_mysql%{?_isa} = %{version}-%{release}

Conflicts:        %{name}-mysqlnd

%description mysql
The %{name}-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the %{name} package.
%endif

################################################################################

%package mysqlnd
Summary:          A module for PHP applications that use MySQL databases
Group:            Development/Languages
License:          PHP

Requires:         %{name}-pdo%{?_isa} = %{version}-%{release}

Provides:         php_database = %{version}-%{release}

Provides:         php-mysql = %{version}-%{release}
Provides:         php-mysql%{?_isa} = %{version}-%{release}

Provides:         php-mysqli = %{version}-%{release}
Provides:         php-mysqli%{?_isa} = %{version}-%{release}

Provides:         php-pdo_mysql = %{version}-%{release}
Provides:         php-pdo_mysql%{?_isa} = %{version}-%{release}

Provides:         php-mysqlnd = %{version}-%{release}
Provides:         php-mysqlnd%{?_isa} = %{version}-%{release}

Provides:         %{name}-mysql = %{version}-%{release}
Provides:         %{name}-mysql%{?_isa} = %{version}-%{release}

Provides:         %{name}-mysqli = %{version}-%{release}
Provides:         %{name}-mysqli%{?_isa} = %{version}-%{release}

Provides:         %{name}-pdo_mysql = %{version}-%{release}
Provides:         %{name}-pdo_mysql%{?_isa} = %{version}-%{release}

%if ! %{with_libmysql}
Obsoletes:        %{name}-mysql < %{version}-%{release}
%endif

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

################################################################################

%package pgsql
Summary:          A PostgreSQL database module for PHP
Group:            Development/Languages
License:          PHP

BuildRequires:    krb5-devel, openssl-devel, postgresql-devel

Requires:         %{name}-pdo%{?_isa} = %{version}-%{release}

Provides:         php_database = %{version}-%{release}

Provides:         php-pdo_pgsql = %{version}-%{release}
Provides:         php-pdo_pgsql%{?_isa} = %{version}-%{release}

Provides:         php-pgsql = %{version}-%{release}
Provides:         php-pgsql%{?_isa} = %{version}-%{release}

Provides:         %{name}-pdo_pgsql = %{version}-%{release}
Provides:         %{name}-pdo_pgsql%{?_isa} = %{version}-%{release}

%description pgsql
The %{name}-pgsql add PostgreSQL database support to PHP.
-PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
%{name} package.

################################################################################

%package process
Summary:          Modules for PHP script using system process interfaces
Group:            Development/Languages
License:          PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:         php-posix = %{version}-%{release}
Provides:         php-posix%{?_isa} = %{version}-%{release}
Provides:         php-sysvsem = %{version}-%{release}
Provides:         php-sysvsem%{?_isa} = %{version}-%{release}
Provides:         php-sysvshm = %{version}-%{release}
Provides:         php-sysvshm%{?_isa} = %{version}-%{release}
Provides:         php-sysvmsg = %{version}-%{release}
Provides:         php-sysvmsg%{?_isa} = %{version}-%{release}
Provides:         php-process = %{version}-%{release}
Provides:         php-process%{?_isa} = %{version}-%{release}

Provides:         %{name}-posix = %{version}-%{release}
Provides:         %{name}-posix%{?_isa} = %{version}-%{release}
Provides:         %{name}-sysvsem = %{version}-%{release}
Provides:         %{name}-sysvsem%{?_isa} = %{version}-%{release}
Provides:         %{name}-sysvshm = %{version}-%{release}
Provides:         %{name}-sysvshm%{?_isa} = %{version}-%{release}
Provides:         %{name}-sysvmsg = %{version}-%{release}
Provides:         %{name}-sysvmsg%{?_isa} = %{version}-%{release}

%description process
The %{name}-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

################################################################################

%package odbc
Summary:          A module for PHP applications that use ODBC databases
Group:            Development/Languages
License:          PHP

Requires:         %{name}-pdo%{?_isa} = %{version}-%{release}

BuildRequires:    unixODBC-devel

Provides:         php_database = %{version}-%{release}
Provides:         php-pdo_odbc = %{version}-%{release}
Provides:         php-pdo_odbc%{?_isa} = %{version}-%{release}
Provides:         php-odbc = %{version}-%{release}
Provides:         php-odbc%{?_isa} = %{version}-%{release}

Provides:         %{name}-pdo_odbc = %{version}-%{release}
Provides:         %{name}-pdo_odbc%{?_isa} = %{version}-%{release}

%description odbc
The %{name}-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the %{name}
package.

################################################################################

%package soap
Summary:          A module for PHP applications that use the SOAP protocol
Group:            Development/Languages
License:          PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:    libxml2-devel

Provides:         php-soap = %{version}-%{release}
Provides:         php-soap%{?_isa} = %{version}-%{release}

%description soap
The %{name}-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

################################################################################

%package interbase
Summary:          A module for PHP applications that use Interbase/Firebird databases
Group:            Development/Languages
License:          PHP

BuildRequires:    firebird-devel

Requires:         %{name}-pdo%{?_isa} = %{version}-%{release}

Provides:         php_database = %{version}-%{release}
Provides:         php-firebird = %{version}-%{release}
Provides:         php-firebird%{?_isa} = %{version}-%{release}
Provides:         php-pdo_firebird = %{version}-%{release}
Provides:         php-pdo_firebird%{?_isa} = %{version}-%{release}
Provides:         php-interbase = %{version}-%{release}
Provides:         php-interbase%{?_isa} = %{version}-%{release}

Provides:         %{name}-firebird = %{version}-%{release}
Provides:         %{name}-firebird%{?_isa} = %{version}-%{release}
Provides:         %{name}-pdo_firebird = %{version}-%{release}
Provides:         %{name}-pdo_firebird%{?_isa} = %{version}-%{release}

%description interbase
The %{name}-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.

################################################################################

%package snmp
Summary:          A module for PHP applications that query SNMP-managed devices
Group:            Development/Languages
License:          PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}, net-snmp

BuildRequires:    net-snmp-devel

Provides:         php-snmp = %{version}-%{release}
Provides:         php-snmp%{?_isa} = %{version}-%{release}

%description snmp
The %{name}-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the %{name} package.

################################################################################

%package xml
Summary:          A module for PHP applications which use XML
Group:            Development/Languages
License:          PHP

BuildRequires:    libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:         php-dom = %{version}-%{release}
Provides:         php-dom%{?_isa} = %{version}-%{release}
Provides:         php-xsl = %{version}-%{release}
Provides:         php-xsl%{?_isa} = %{version}-%{release}
Provides:         php-domxml = %{version}-%{release}
Provides:         php-domxml%{?_isa} = %{version}-%{release}
Provides:         php-wddx = %{version}-%{release}
Provides:         php-wddx%{?_isa} = %{version}-%{release}
Provides:         php-xmlreader = %{version}-%{release}
Provides:         php-xmlreader%{?_isa} = %{version}-%{release}
Provides:         php-xmlwriter = %{version}-%{release}
Provides:         php-xmlwriter%{?_isa} = %{version}-%{release}
Provides:         php-xml = %{version}-%{release}
Provides:         php-xml%{?_isa} = %{version}-%{release}

Provides:         %{name}-dom = %{version}-%{release}
Provides:         %{name}-dom%{?_isa} = %{version}-%{release}
Provides:         %{name}-xsl = %{version}-%{release}
Provides:         %{name}-xsl%{?_isa} = %{version}-%{release}
Provides:         %{name}-domxml = %{version}-%{release}
Provides:         %{name}-domxml%{?_isa} = %{version}-%{release}
Provides:         %{name}-wddx = %{version}-%{release}
Provides:         %{name}-wddx%{?_isa} = %{version}-%{release}
Provides:         %{name}-xmlreader = %{version}-%{release}
Provides:         %{name}-xmlreader%{?_isa} = %{version}-%{release}
Provides:         %{name}-xmlwriter = %{version}-%{release}
Provides:         %{name}-xmlwriter%{?_isa} = %{version}-%{release}

%description xml
The %{name}-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

################################################################################

%package xmlrpc
Summary:          A module for PHP applications which use the XML-RPC protocol
Group:            Development/Languages
License:          PHP and BSD

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:         php-xmlrpc = %{version}-%{release}
Provides:         php-xmlrpc%{?_isa} = %{version}-%{release}

%description xmlrpc
The %{name}-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

################################################################################

%package mbstring
Summary:          A module for PHP applications which need multi-byte string handling
Group:            Development/Languages
License:          PHP and LGPLv2 and BSD and OpenLDAP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:         php-mbstring = %{version}-%{release}
Provides:         php-mbstring%{?_isa} = %{version}-%{release}

%description mbstring
The %{name}-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

################################################################################

%package gd
Summary:          A module for PHP applications for using the gd graphics library
Group:            Development/Languages
License:          PHP and BSD

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:    libjpeg-devel, libpng-devel, freetype-devel
BuildRequires:    libXpm-devel, t1lib-devel

Provides:         php-gd = %{version}-%{release}
Provides:         php-gd%{?_isa} = %{version}-%{release}

%description gd
The %{name}-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

################################################################################

%package bcmath
Summary:          A module for PHP applications for using the bcmath library
Group:            Development/Languages
License:          PHP and LGPLv2+

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:         php-bcmath = %{version}-%{release}
Provides:         php-bcmath%{?_isa} = %{version}-%{release}

%description bcmath
The %{name}-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

################################################################################

%package dba
Summary:          A database abstraction layer module for PHP applications
Group:            Development/Languages
License:          PHP

BuildRequires:    %{db_devel}, tokyocabinet-devel

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:         php-dba = %{version}-%{release}
Provides:         php-dba%{?_isa} = %{version}-%{release}

%description dba
The %{name}-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

################################################################################

%package mcrypt
Summary:          Standard PHP module provides mcrypt library support
Group:            Development/Languages
License:          PHP

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:    libmcrypt-devel

Provides:         php-mcrypt = %{version}-%{release}
Provides:         php-mcrypt%{?_isa} = %{version}-%{release}

%description mcrypt
The %{name}-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

################################################################################

%package tidy
Summary:          Standard PHP module provides tidy library support
Group:            Development/Languages

Requires:         %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:    libtidy-devel

Provides:         php-tidy = %{version}-%{release}
Provides:         php-tidy%{?_isa} = %{version}-%{release}

%description tidy
The %{name}-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

################################################################################

%package mssql
Summary:          MSSQL database module for PHP
Group:            Development/Languages
License:          PHP

Requires:         %{name}-pdo%{?_isa} = %{version}-%{release}

BuildRequires:    freetds-devel

Provides:         php_database = %{version}-%{release}
Provides:         php-pdo_dblib = %{version}-%{release}
Provides:         php-pdo_dblib%{?_isa} = %{version}-%{release}
Provides:         php-mssql = %{version}-%{release}
Provides:         php-mssql%{?_isa} = %{version}-%{release}

Provides:         %{name}-pdo_dblib = %{version}-%{release}
Provides:         %{name}-pdo_dblib%{?_isa} = %{version}-%{release}

%description mssql
The %{name}-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

################################################################################

%package embedded
Summary:          PHP library for embedding in applications
Group:            System Environment/Libraries
Requires:         %{name}-common%{?_isa} = %{version}-%{release}

Provides:        php-embedded-devel = %{version}-%{release}
Provides:        php-embedded-devel%{?_isa} = %{version}-%{release}
Provides:        php-embedded = %{version}-%{release}
Provides:        php-embedded%{?_isa} = %{version}-%{release}

Provides:        %{name}-embedded-devel = %{version}-%{release}
Provides:        %{name}-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The %{name}-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

################################################################################

%package opcache
Summary:         An opcode cache Zend extension
Group:           Development/Languages

Requires:        %{name}-common%{?_isa} = %{version}-%{release}

Provides:        php-pecl-zendopcache = %{opcachever}, php-pecl-zendopcache%{?_isa} = %{opcachever}
Provides:        php-pecl(OPcache) = %{opcachever}, php-pecl(OPcache) = %{opcachever}
Provides:        php-opcache = %{version}-%{release}
Provides:        php-opcache%{?_isa} = %{version}-%{release}

Provides:        %{name}-pecl-zendopcache = %{opcachever}, %{name}-pecl-zendopcache%{?_isa} = %{opcachever}
Provides:        %{name}-pecl(OPcache) = %{opcachever}, %{name}-pecl(OPcache) = %{opcachever}

%description opcache
The %{name}-opcache package contains an opcode cache used for caching and
optimizing intermediate code.

################################################################################

%package pspell
Summary:         A module for PHP applications for using pspell interfaces
Group:           System Environment/Libraries
License:         PHP

Requires:        %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:   aspell-devel >= 0.50.0

Provides:        php-pspell = %{version}-%{release}
Provides:        php-pspell%{?_isa} = %{version}-%{release}

%description pspell
The %{name}-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

################################################################################

%package recode
Summary:         A module for PHP applications for using the recode library
Group:           System Environment/Libraries
License:         PHP

Requires:        %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:   recode-devel

Provides:        php-recode = %{version}-%{release}
Provides:        php-recode%{?_isa} = %{version}-%{release}

%description recode
The %{name}-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

################################################################################

%package intl
Summary:         Internationalization extension for PHP applications
Group:           System Environment/Libraries
License:         PHP

Requires: %{name}-common%{?_isa} = %{version}-%{release}

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:   libicu-devel >= 4.0
%else
BuildRequires:   libicu42-devel >= 4.0
%endif

Provides:        php-intl = %{version}-%{release}
Provides:        php-intl%{?_isa} = %{version}-%{release}

%description intl
The %{name}-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

################################################################################

%package enchant
Summary:         Enchant spelling extension for PHP applications
Group:           System Environment/Libraries
License:         PHP

Requires:        %{name}-common%{?_isa} = %{version}-%{release}

BuildRequires:   enchant-devel >= 1.2.4

Provides:        php-enchant = %{version}-%{release}
Provides:        php-enchant%{?_isa} = %{version}-%{release}

%description enchant
The %{name}-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

################################################################################

%prep
%setup -q -n php-%{version}%{?rcver}
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb

%patch21 -p1 -b .odbctimer

%patch40 -p1 -b .dlopen
%patch42 -p1 -b .systzdata
%patch43 -p1 -b .phpize

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif

%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo
%patch48 -p1 -b .icuconfig

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-cli build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
%if %{with_fpm}
    build-fpm \
%endif
%if %{with_phpdbg}
    build-phpdbg
%endif

# Affected by systzdata patch
%{__rm} -f ext/date/tests/timezone_location_get.phpt
# Fails sometime
%{__rm} -f ext/sockets/tests/mcast_ipv?_recv.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ \t]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_ZIP_VERSION /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_ZENDOPCACHE_VERSION /{s/.* "//;s/".*$//;p}' ext/opcache/ZendAccelerator.h)
if test "$ver" != "%{opcachever}"; then
   : Error: Upstream OPcache version is now ${ver}, expecting %{opcachever}.
   : Update the opcachever macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

%if %{with_tmpfiles}
# php-fpm configuration files for tmpfiles.d
echo "d %{_localstatedir}/run/php-fpm 755 root root" >php-fpm.tmpfiles
%endif

# bring in newer config.guess and config.sub for aarch64 support
cp -f /usr/lib/rpm/config.{guess,sub} .

%build
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.7. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_root_prefix} \
    --with-png-dir=%{_root_prefix} \
    --with-xpm-dir=%{_root_prefix} \
    --enable-gd-native-ttf \
    --with-t1lib=%{_root_prefix} \
    --without-gdbm \
    --with-jpeg-dir=%{_root_prefix} \
    --with-openssl \
    --with-pcre-regex \
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_root_prefix} \
    --with-system-tzdata \
    --with-mhash \
%if %{with_dtrace}
    --enable-dtrace \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

with_shared="--with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_root_prefix} \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_root_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_root_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_root_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_root_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_root_prefix} \
      --with-pdo-sqlite=shared,%{_root_prefix} \
      --with-pdo-dblib=shared,%{_root_prefix} \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
      --with-sqlite3=shared,%{_root_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
%if %{with_libzip}
      --with-libzip \
%endif
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_root_prefix} \
      --with-tidy=shared,%{_root_prefix} \
      --with-mssql=shared,%{_root_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_root_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
      --with-icu-dir=%{_root_prefix} \
%else
      --with-icu-config=%{_root_bindir}/icu42-icu-config
%endif
      --with-enchant=shared,%{_root_prefix} \
      --with-recode=shared,%{_root_prefix} \
      --enable-opcache"

with_shared2="--enable-pdo=shared \
      --with-mysql=shared,%{_root_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --without-pdo-sqlite"

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem \
      --disable-opcache"

# Build /usr/bin/php with the CLI SAPI, /usr/bin/php-cgi with the CGI SAPI,
# and all the shared extensions
pushd build-cli
build --enable-force-cgi-redirect \
      --disable-phpdbg \
      --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-fastcgi \
      --without-readline \
      --with-libedit \
      ${with_shared}
popd

# Build Apache module
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
      ${with_shared2} ${without_shared}
popd

%if %{with_fpm}
# Build php-fpm
pushd build-fpm
build --enable-fpm \
%if %{with_systemd}
      --with-fpm-systemd \
%endif
      --libdir=%{_libdir}/php \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe cli (mainly for modules)
pushd build-ztscli
EXTENSION_DIR=%{_libdir}/php-zts/modules
build --enable-force-cgi-redirect \
      --disable-phpdbg \
      --enable-pcntl \
      --enable-fastcgi \
      --without-readline \
      --with-libedit \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      ${with_shared}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      ${with_shared2} ${without_shared} \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d
popd
%endif

%if %{with_phpdbg}
# Build /usr/bin/phpdbg with readline support
pushd build-phpdbg
EXTENSION_DIR=%{_libdir}/php/modules
build --enable-phpdbg \
      --libdir=%{_libdir}/php \
      --with-readline \
      --without-libedit \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

%check

%install
%{__rm} -rf %{buildroot}

%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=%{buildroot}

# rename extensions build with mysqlnd
mv %{buildroot}%{_libdir}/php-zts/modules/mysql.so \
   %{buildroot}%{_libdir}/php-zts/modules/mysqlnd_mysql.so
mv %{buildroot}%{_libdir}/php-zts/modules/mysqli.so \
   %{buildroot}%{_libdir}/php-zts/modules/mysqlnd_mysqli.so
mv %{buildroot}%{_libdir}/php-zts/modules/pdo_mysql.so \
   %{buildroot}%{_libdir}/php-zts/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the extensions for the ZTS version modules for libmysql
make -C build-zts install-modules \
     INSTALL_ROOT=%{buildroot}
%endif

# rename ZTS binary
mv %{buildroot}%{_bindir}/php        %{buildroot}%{_bindir}/zts-php
mv %{buildroot}%{_bindir}/phpize     %{buildroot}%{_bindir}/zts-phpize
mv %{buildroot}%{_bindir}/php-config %{buildroot}%{_bindir}/zts-php-config
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers INSTALL_ROOT=%{buildroot}

%if %{with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm INSTALL_ROOT=%{buildroot}
%endif

%if %{with_phpdbg}
# Install the phpdbg binary
make -C build-phpdbg install-phpdbg INSTALL_ROOT=%{buildroot}
%endif

# Install everything from the CLI/CGI SAPI build
make -C build-cli install INSTALL_ROOT=%{buildroot}

# rename extensions build with mysqlnd
mv %{buildroot}%{_libdir}/php/modules/mysql.so \
   %{buildroot}%{_libdir}/php/modules/mysqlnd_mysql.so
mv %{buildroot}%{_libdir}/php/modules/mysqli.so \
   %{buildroot}%{_libdir}/php/modules/mysqlnd_mysqli.so
mv %{buildroot}%{_libdir}/php/modules/pdo_mysql.so \
   %{buildroot}%{_libdir}/php/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the mysql extension build with libmysql
make -C build-apache install-modules \
     INSTALL_ROOT=%{buildroot}
%endif

# Install the default configuration file and icons
install -m 755 -d %{buildroot}%{_sysconfdir}/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/php.ini
install -m 755 -d %{buildroot}%{_httpd_contentdir}/icons
install -m 644 php.gif %{buildroot}%{_httpd_contentdir}/icons/php.gif

# For third-party packaging:
install -m 755 -d %{buildroot}%{_libdir}/php/pear \
                  %{buildroot}%{_datadir}/php

# install the DSO
install -m 755 -d %{buildroot}%{_httpd_moddir}
install -m 755 build-apache/libs/libphp5.so %{buildroot}%{_httpd_moddir}

# install the ZTS DSO
%if %{with_zts}
install -m 755 build-zts/libs/libphp5.so %{buildroot}%{_httpd_moddir}/libphp5-zts.so
%endif

sed -e 's/libphp5/lib%{_name}5/' %{SOURCE9} >modconf
sed -e 's/libphp5/lib%{_name}5/' %{SOURCE10} >ztsmodconf

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4 (fedora <= 17)
install -D -m 644 modconf %{buildroot}%{_httpd_confdir}/%{_name}.conf
%if %{with_zts}
cat ztsmodconf >>%{buildroot}%{_httpd_confdir}/%{_name}.conf
%endif
cat %{SOURCE1} >>%{buildroot}%{_httpd_confdir}/%{_name}.conf
%else
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 modconf %{buildroot}%{_httpd_modconfdir}/10-%{_name}.conf
%if %{with_zts}
cat ztsmodconf >>%{buildroot}%{_httpd_modconfdir}/10-%{_name}.conf
%endif
install -D -m 644 %{SOURCE1} %{buildroot}%{_httpd_confdir}/%{_name}.conf
%endif
sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -i %{buildroot}%{_httpd_confdir}/%{_name}.conf

sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -i %{buildroot}%{_httpd_confdir}/%{_name}.conf

install -m 755 -d %{buildroot}%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d %{buildroot}%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d %{buildroot}%{_localstatedir}/lib/php
install -m 700 -d %{buildroot}%{_localstatedir}/lib/php/session
install -m 700 -d %{buildroot}%{_localstatedir}/lib/php/wsdlcache

%if %{with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d %{buildroot}%{_localstatedir}/log/php-fpm
install -m 755 -d %{buildroot}%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d %{buildroot}%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/php-fpm.conf
sed -e 's:/var/run:%{_localstatedir}/run:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -e 's:/etc:%{_sysconfdir}:' \
    -i %{buildroot}%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/php-fpm.d/www.conf.default
sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -i %{buildroot}%{_sysconfdir}/php-fpm.d/www.conf.default
mv %{buildroot}%{_sysconfdir}/php-fpm.conf.default .
%if %{with_tmpfiles}
# tmpfiles.d
install -m 755 -d %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 644 php-fpm.tmpfiles %{buildroot}%{_sysconfdir}/tmpfiles.d/php-fpm.conf
%endif
%if %{with_systemd}
sed -e "s/daemonise = yes/daemonise = no/" \
    -i %{buildroot}%{_sysconfdir}/php-fpm.conf
# install systemd unit files and scripts for handling server startup
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/php-fpm.service
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/etc:%{_sysconfdir}:' \
    -e 's:/usr/sbin:%{_sbindir}:' \
    -i %{buildroot}%{_unitdir}/php-fpm.service
%else
# Service
install -m 755 -d %{buildroot}%{_root_initddir}
install -m 755 %{SOURCE11} %{buildroot}%{_root_initddir}/php-fpm
# Needed relocation for SCL
sed -e '/php-fpm.pid/s:/var:%{_localstatedir}:' \
    -e '/subsys/s/php-fpm/php-fpm/' \
    -e 's:/etc/sysconfig/php-fpm:%{_sysconfdir}/sysconfig/php-fpm:' \
    -e 's:/etc/php-fpm.conf:%{_sysconfdir}/php-fpm.conf:' \
    -e 's:/usr/sbin:%{_sbindir}:' \
    -i %{buildroot}%{_root_initddir}/php-fpm
%endif
# LogRotate
install -m 755 -d %{buildroot}%{_root_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} %{buildroot}%{_root_sysconfdir}/logrotate.d/php-fpm
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -i %{buildroot}%{_root_sysconfdir}/logrotate.d/php-fpm
# Environment file
install -m 755 -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/sysconfig/php-fpm
%endif

# Fix the link
(cd %{buildroot}%{_bindir}; ln -sfn phar.phar phar)

# Copy stub .ini file for opcache
install -m 644 %{SOURCE50} %{buildroot}%{_sysconfdir}/php.d/opcache.ini
# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} %{buildroot}%{_sysconfdir}/php.d/opcache-default.blacklist
sed -e 's:%{_root_sysconfdir}:%{_sysconfdir}:' \
    -i %{buildroot}%{_sysconfdir}/php.d/opcache.ini
%if %{with_zts}
install -m 644 %{buildroot}%{_sysconfdir}/php.d/opcache.ini %{buildroot}%{_sysconfdir}/php-zts.d/opcache.ini
install -m 644 %{SOURCE51} %{buildroot}%{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif


# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc imap \
    mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    bz2 calendar ctype exif ftp gettext gmp iconv simplexml \
    sockets tokenizer \
    pdo pdo_pgsql pdo_odbc pdo_sqlite json %{zipmod} \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
    sqlite3  \
%endif
%if %{with_libmysql}
    mysql mysqli pdo_mysql \
%endif
    interbase pdo_firebird \
    enchant phar fileinfo intl \
    mcrypt tidy pdo_dblib mssql pspell curl wddx \
    posix shmop sysvshm sysvsem sysvmsg recode xml; do

    # Make sure wddx is loaded after the xml extension, which it depends on
    if [ "$mod" = "wddx" ]
    then
        ini=xml_${mod}.ini
    else
        ini=${mod}.ini
    fi

    cat > %{buildroot}%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
    cp %{buildroot}%{_sysconfdir}/php.d/${ini} \
       %{buildroot}%{_sysconfdir}/php-zts.d/${ini}
%endif
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

mv files.xml files.xmlext

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
%if %{with_libmysql}
cat files.mysqli >> files.mysql
cat files.pdo_mysql >> files.mysql
%endif

# mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
cat files.pdo_firebird >> files.interbase

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat files.sqlite3 >> files.pdo
%endif

# Package most extensions in -common.
cat files.json files.curl files.phar files.fileinfo \
    files.bz2 files.calendar files.ctype files.exif files.ftp files.gettext \
    files.gmp files.iconv files.simplexml files.shmop files.xmlext \
    files.sockets files.tokenizer > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# Remove unpackaged files
rm -rf %{buildroot}%{_libdir}/php/modules/*.a \
       %{buildroot}%{_libdir}/php-zts/modules/*.a \
       %{buildroot}%{_bindir}/{phptar} \
       %{buildroot}%{_datadir}/pear \
       %{buildroot}%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
%{__rm} -rf %{buildroot}
%{__rm} -rf files.* macros.php

%if %{with_fpm}
%pre fpm
# Add the "apache" user as we don't require httpd
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0

%if %{with_systemd}
%post fpm
%systemd_post php-fpm.service

%preun fpm
%systemd_preun php-fpm.service

%postun fpm
%systemd_postun_with_restart php-fpm.service

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- php-fpm
if [ -f /etc/rc.d/init.d/php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi

%else

%post fpm
/sbin/chkconfig --add php-fpm

%preun fpm
if [ "$1" = 0 ] ; then
    /sbin/service php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php-fpm
fi

%postun fpm
if [ "$1" -ge "1" ] ; then
service php-fpm condrestart &> /dev/null || :
fi

%endif

%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%{_httpd_moddir}/libphp5.so
%if %{with_zts}
%{_httpd_moddir}/libphp5-zts.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%config(noreplace) %{_httpd_confdir}/%{_name}.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-%{_name}.conf
%endif
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root,-)
%doc CODING_STANDARDS CREDITS EXTENSIONS LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%doc libmagic_LICENSE
%doc phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php
%dir %{_libdir}/php/pear
%dir %{_datadir}/php

%files cli
%defattr(-,root,root,-)
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%doc sapi/cgi/README* sapi/cli/README

%if %{with_phpdbg}
%files phpdbg
%defattr(-,root,root,-)
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%endif

%if %{with_fpm}
%files fpm
%defattr(-,root,root,-)
%doc php-fpm.conf.default
%doc fpm_LICENSE
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf.default
%config(noreplace) %{_root_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm

%if %{with_tmpfiles}
%{_sysconfdir}/tmpfiles.d/php-fpm.conf
%endif
%if %{with_systemd}
%{_unitdir}/php-fpm.service
%else
%{_root_initddir}/php-fpm
%endif

%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%dir %{_localstatedir}/run/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html
%endif

%files devel
%defattr(-,root,root,-)
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
%{_bindir}/zts-php
%{_libdir}/php-zts/build
%endif
%{_mandir}/man1/php-config.1*

%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{embed_version}.so

%files opcache
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/php/modules/opcache.so
%config(noreplace) %{_sysconfdir}/php.d/opcache.ini
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/opcache.so
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache.ini
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif

%files pgsql -f files.pgsql

%if %{with_libmysql}
%files mysql -f files.mysql
%endif

%files odbc -f files.odbc

%files imap -f files.imap

%files ldap -f files.ldap

%files snmp -f files.snmp

%files xml -f files.xml

%files xmlrpc -f files.xmlrpc

%files mbstring -f files.mbstring
%defattr(-,root,root,-)
%doc libmbfl_LICENSE
%doc oniguruma_COPYING
%doc ucgendat_LICENSE

%files gd -f files.gd
%defattr(-,root,root,-)
%doc libgd_README
%doc libgd_COPYING

%files soap -f files.soap

%files bcmath -f files.bcmath
%defattr(-,root,root,-)
%doc libbcmath_COPYING

%files dba -f files.dba

%files pdo -f files.pdo

%files mcrypt -f files.mcrypt

%files tidy -f files.tidy

%files mssql -f files.mssql

%files pspell -f files.pspell

%files intl -f files.intl

%files process -f files.process

%files recode -f files.recode

%files interbase -f files.interbase

%files enchant -f files.enchant

%files mysqlnd -f files.mysqlnd

################################################################################

%changelog
* Sat Apr 23 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 5.6.20-0
- Updated to latest version

* Sat Mar 13 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 5.6.19-0
- Updated to latest version

* Sat Jan 16 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 5.6.17-0
- Initial build
