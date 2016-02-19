################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __updalernatives  %{_sbindir}/update-alternatives

################################################################################

%define debug_package     %{nil}

################################################################################

%define service_user      zabbix
%define service_group     zabbix
%define service_home      %{_libdir}/zabbix

################################################################################

Name:                 zabbix
Version:              3.0.0
Release:              0%{?dist}
Summary:              The Enterprise-class open source monitoring solution
Group:                Applications/Internet
License:              GPLv2+
URL:                  http://www.zabbix.com/

Source0:              http://heanet.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/%{version}/zabbix-%{version}.tar.gz
Source1:              zabbix-web22.conf
Source2:              zabbix-web24.conf
Source3:              zabbix-logrotate.in

Source10:             zabbix-agent.init
Source11:             zabbix-server.init
Source12:             zabbix-proxy.init

Source20:             zabbix-agent.service
Source21:             zabbix-server.service
Source22:             zabbix-proxy.service
Source23:             zabbix-tmpfiles.conf

Patch0:               config.patch
Patch1:               fonts-config.patch
Patch2:               fping3-sourceip-option.patch

Buildroot:            %{_tmppath}/zabbix-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        mysql-devel
BuildRequires:        postgresql-devel
BuildRequires:        net-snmp-devel
BuildRequires:        openldap-devel
BuildRequires:        gnutls-devel
BuildRequires:        iksemel-devel
BuildRequires:        unixODBC-devel
BuildRequires:        curl-devel >= 7.13.1
BuildRequires:        OpenIPMI-devel >= 2
BuildRequires:        libssh2-devel >= 1.0.0
BuildRequires:        libxml2-devel
%if 0%{?rhel} >= 7
BuildRequires:        systemd
%endif

################################################################################

%description
Zabbix is the ultimate enterprise-level software designed for
real-time monitoring of millions of metrics collected from tens of
thousands of servers, virtual machines and network devices.

################################################################################

%package agent
Summary:              Zabbix Agent
Group:                Applications/Internet

Requires:             logrotate
Requires(pre):        /usr/sbin/useradd
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(preun):      systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

BuildRequires:        libxml2-devel

Obsoletes:            zabbix = %{version}-%{release}

%description agent
Zabbix agent to be installed on monitored systems.

################################################################################

%package get
Summary:              Zabbix Get
Group:                Applications/Internet

%description get
Zabbix get command line utility

################################################################################

%package sender
Summary:              Zabbix Sender
Group:                Applications/Internet

%description sender
Zabbix sender command line utility

################################################################################

%package server-mysql
Summary:              Zabbix server for MySQL or MariaDB database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Provides:             zabbix-server = %{version}-%{release}
Provides:             zabbix-server-implementation = %{version}-%{release}

Obsoletes:            zabbix = %{version}-%{release}
Obsoletes:            zabbix-server = %{version}-%{release}

%description server-mysql
Zabbix server with MySQL or MariaDB database support.

################################################################################

%package server-pgsql
Summary:              Zabbix server for PostgresSQL database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Provides:             zabbix-server = %{version}-%{release}
Provides:             zabbix-server-implementation = %{version}-%{release}

Obsoletes:            zabbix = %{version}-%{release}
Obsoletes:            zabbix-server = %{version}-%{release}

%description server-pgsql
Zabbix server with PostgresSQL database support.

################################################################################

%package proxy-mysql
Summary:              Zabbix proxy for MySQL or MariaDB database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Provides:             zabbix-proxy = %{version}-%{release}
Provides:             zabbix-proxy-implementation = %{version}-%{release}

Obsoletes:            zabbix = %{version}-%{release}
Obsoletes:            zabbix-proxy = %{version}-%{release}

%description proxy-mysql
Zabbix proxy with MySQL or MariaDB database support.

################################################################################

%package proxy-pgsql
Summary:              Zabbix proxy for PostgreSQL database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Provides:             zabbix-proxy = %{version}-%{release}
Provides:             zabbix-proxy-implementation = %{version}-%{release}

Obsoletes:            zabbix = %{version}
Obsoletes:            zabbix-proxy = %{version}-%{release}

%description proxy-pgsql
Zabbix proxy with PostgreSQL database support.

################################################################################

%package web
Summary:              Zabbix web frontend common package
Group:                Applications/Internet

BuildArch:            noarch

Requires:             httpd
Requires:             php >= 5.4
Requires:             php-gd
Requires:             php-bcmath
Requires:             php-mbstring
Requires:             php-xml
Requires:             php-ldap
Requires:             dejavu-sans-fonts
Requires:             zabbix-web-database = %{version}-%{release}

Requires(post):       %{_sbindir}/update-alternatives
Requires(preun):      %{_sbindir}/update-alternatives

%description web
Zabbix web frontend common package

################################################################################

%package web-mysql
Summary:              Zabbix web frontend for MySQL
Group:                Applications/Internet

BuildArch:            noarch

Requires:             php-mysql
Requires:             zabbix-web = %{version}-%{release}
Provides:             zabbix-web-database = %{version}-%{release}

%description web-mysql
Zabbix web frontend for MySQL

################################################################################

%package web-pgsql
Summary:              Zabbix web frontend for PostgreSQL
Group:                Applications/Internet

BuildArch:            noarch

Requires:             php-pgsql
Requires:             zabbix-web = %{version}-%{release}
Provides:             zabbix-web-database = %{version}-%{release}

%description web-pgsql
Zabbix web frontend for PostgreSQL

################################################################################

%prep
%setup0 -q -n zabbix-%{version}

%patch0 -p1
%patch1 -p1
%if 0%{?rhel} >= 7
%patch2 -p1
%endif

# remove obsolete fonts
%{__rm} -f frontends/php/fonts/DejaVuSans.ttf

# remove .htaccess files
%{__rm} -f frontends/php/app/.htaccess
%{__rm} -f frontends/php/conf/.htaccess
%{__rm} -f frontends/php/include/.htaccess
%{__rm} -f frontends/php/local/.htaccess

# remove translation source files and scripts
find frontends/php/locale -name '*.po' -delete
find frontends/php/locale -name '*.sh' -delete

# traceroute command path for global script
%{__sed} -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/mysql/data.sql
%{__sed} -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/postgresql/data.sql


%build
build_flags="
        --enable-dependency-tracking
        --sysconfdir=%{_sysconfdir}/%{name}
        --libdir=%{_libdir}/%{name}
        --mandir=%{_mandir}
        --enable-agent
        --enable-server
        --enable-proxy
        --enable-ipv6
        --with-net-snmp
        --with-ldap
        --with-libcurl
        --with-openipmi
        --with-jabber
        --with-unixodbc
        --with-ssh2
        --with-libxml2
        --with-openssl
"

%configure $build_flags --with-mysql
make %{?_smp_mflags}

%{__mv} src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
%{__mv} src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure $build_flags --with-postgresql
make %{?_smp_mflags}

%{__mv} src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
%{__mv} src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql


%install
%{__rm} -rf %{buildroot}

# install
make DESTDIR=%{buildroot} install

# clean unnecessary binaries
%{__rm} -f %{buildroot}%{_sbindir}/zabbix_server
%{__rm} -f %{buildroot}%{_sbindir}/zabbix_proxy

# install necessary directories
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sbindir}

install -dm 755 %{buildroot}%{_libdir}/zabbix
install -dm 755 %{buildroot}%{_libdir}/zabbix/modules

install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/web
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/alertscripts
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/externalscripts
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/zabbix_agentd.d
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/zabbix_server.d
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/zabbix_proxy.d

install -dm 755 %{buildroot}%{_localstatedir}/log/zabbix
install -dm 755 %{buildroot}%{_localstatedir}/run/zabbix

install -dm 755 %{buildroot}%{_docdir}/zabbix-agent-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-server-mysql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-server-pgsql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-proxy-mysql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-proxy-pgsql-%{version}

install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_mandir}/man8

install -dm 755 %{buildroot}%{_datadir}/zabbix

install -dm 755 %{buildroot}%{_sysconfdir}/httpd/conf.d

# install binaries
install -m 0755 -p src/zabbix_agent/zabbix_agentd %{buildroot}%{_sbindir}/
install -m 0755 -p src/zabbix_server/zabbix_server_* %{buildroot}%{_sbindir}/
install -m 0755 -p src/zabbix_proxy/zabbix_proxy_* %{buildroot}%{_sbindir}/
install -m 0755 -p src/zabbix_get/zabbix_get %{buildroot}%{_bindir}/
install -m 0755 -p src/zabbix_sender/zabbix_sender %{buildroot}%{_bindir}/

# install man
%{__gzip} -c man/zabbix_get.man > %{buildroot}%{_mandir}/man1/zabbix_get.1.gz
%{__gzip} -c man/zabbix_sender.man > %{buildroot}%{_mandir}/man1/zabbix_sender.1.gz
%{__gzip} -c man/zabbix_agentd.man > %{buildroot}%{_mandir}/man8/zabbix_agentd.8.gz
%{__gzip} -c man/zabbix_server.man > %{buildroot}%{_mandir}/man8/zabbix_server.8.gz
%{__gzip} -c man/zabbix_proxy.man > %{buildroot}%{_mandir}/man8/zabbix_proxy.8.gz

# install frontend files
find frontends/php -name '*.orig' -delete
%{__cp} -a frontends/php/* %{buildroot}%{_datadir}/zabbix

# install frontend configuration files
touch %{buildroot}%{_sysconfdir}/zabbix/web/zabbix.conf.php
%{__mv} %{buildroot}%{_datadir}/zabbix/conf/maintenance.inc.php %{buildroot}%{_sysconfdir}/zabbix/web/

# drop config files in place
%if 0%{?rhel} >= 7
install -m 0644 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/zabbix.conf
%else
install -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/zabbix.conf
%endif

# generate config files
cat conf/zabbix_agentd.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_agentd.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|g' \
        -e '/^# LogFileSize=.*/a \\nLogFileSize=0' \
        -e '/^# Include=$/a \\nInclude=%{_sysconfdir}/zabbix/zabbix_agentd.d/' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_agentd.conf

cat conf/zabbix_server.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_server.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_server.log|g' \
        -e '/^# LogFileSize=/a \\nLogFileSize=0' \
        -e '/^# AlertScriptsPath=/a \\nAlertScriptsPath=%{_sysconfdir}/zabbix/alertscripts' \
        -e '/^# ExternalScripts=/a \\nExternalScripts=%{_sysconfdir}/zabbix/externalscripts' \
        -e 's|^DBUser=root|DBUser=zabbix|g' \
        -e '/^# DBSocket=/a \\nDBSocket=%{_localstatedir}/lib/mysql/mysql.sock' \
        -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=/var/log/snmptrap/snmptrap.log' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_server.conf

cat conf/zabbix_proxy.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_proxy.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_proxy.log|g' \
        -e '/^# LogFileSize=/a \\nLogFileSize=0' \
        -e '/^# ExternalScripts=/a \\nExternalScripts=%{_sysconfdir}/zabbix/externalscripts' \
        -e 's|^DBUser=root|DBUser=zabbix|g' \
        -e '/^# DBSocket=/a \\nDBSocket=%{_localstatedir}/lib/mysql/mysql.sock' \
        -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=/var/log/snmptrap/snmptrap.log' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_proxy.conf

# install logrotate configuration files
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|server|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-server
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|agentd|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-agent
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|proxy|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-proxy

# install startup scripts
%if 0%{?rhel} >= 7
install -Dm 0644 -p %{SOURCE20} %{buildroot}%{_unitdir}/zabbix-agent.service
install -Dm 0644 -p %{SOURCE21} %{buildroot}%{_unitdir}/zabbix-server.service
install -Dm 0644 -p %{SOURCE22} %{buildroot}%{_unitdir}/zabbix-proxy.service
%else
install -Dm 0755 -p %{SOURCE10} %{buildroot}%{_sysconfdir}/init.d/zabbix-agent
install -Dm 0755 -p %{SOURCE11} %{buildroot}%{_sysconfdir}/init.d/zabbix-server
install -Dm 0755 -p %{SOURCE12} %{buildroot}%{_sysconfdir}/init.d/zabbix-proxy
%endif

# install systemd-tmpfiles conf
%if 0%{?rhel} >= 7
install -Dm 0644 -p %{SOURCE23} %{buildroot}%{_libdir}/tmpfiles.d/zabbix-agent.conf
install -Dm 0644 -p %{SOURCE23} %{buildroot}%{_libdir}/tmpfiles.d/zabbix-server.conf
install -Dm 0644 -p %{SOURCE23} %{buildroot}%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%endif

# copy sql files for servers
docdir=%{buildroot}%{_docdir}/zabbix-server-mysql-%{version}
cat database/mysql/schema.sql > $docdir/create.sql
cat database/mysql/images.sql >> $docdir/create.sql
cat database/mysql/data.sql >> $docdir/create.sql
%{__gzip} $docdir/create.sql

docdir=%{buildroot}%{_docdir}/zabbix-server-pgsql-%{version}
cat database/postgresql/schema.sql > $docdir/create.sql
cat database/postgresql/images.sql >> $docdir/create.sql
cat database/postgresql/data.sql >> $docdir/create.sql
%{__gzip} $docdir/create.sql

# copy sql files for proxies
docdir=%{buildroot}%{_docdir}/zabbix-proxy-mysql-%{version}
cp database/mysql/schema.sql $docdir/schema.sql
%{__gzip} $docdir/schema.sql

docdir=%{buildroot}%{_docdir}/zabbix-proxy-pgsql-%{version}
cp database/postgresql/schema.sql $docdir/schema.sql
%{__gzip} $docdir/schema.sql


%clean
%{__rm} -rf %{buildroot}

################################################################################

%pre agent
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
:


%post agent
%if 0%{?rhel} >= 7
%systemd_post zabbix-agent.service
%else
%{__chkconfig} --add zabbix-agent || :
%endif


%pre server-mysql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
:


%pre server-pgsql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
:


%pre proxy-mysql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
:


%pre proxy-pgsql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
:


%post server-mysql
%if 0%{?rhel} >= 7
%systemd_post zabbix-server.service
%else
%{__chkconfig} --add zabbix-server || :
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_server \
        zabbix-server %{_sbindir}/zabbix_server_mysql 10
:


%post server-pgsql
%if 0%{?rhel} >= 7
%systemd_post zabbix-server.service
%else
%{__chkconfig} --add zabbix-server || :
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_server \
        zabbix-server %{_sbindir}/zabbix_server_pgsql 10
:


%post proxy-mysql
%if 0%{?rhel} >= 7
%systemd_post zabbix-proxy.service
%else
%{__chkconfig} --add zabbix-proxy
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_proxy \
        zabbix-proxy %{_sbindir}/zabbix_proxy_mysql 10
:


%post proxy-pgsql
%if 0%{?rhel} >= 7
%systemd_post zabbix-proxy.service
%else
%{__chkconfig} --add zabbix-proxy
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_proxy \
        zabbix-proxy %{_sbindir}/zabbix_proxy_pgsql 10
:


%post web
%{__updalternatives} --install %{_datadir}/zabbix/fonts/graphfont.ttf \
        zabbix-web-font %{_datadir}/fonts/dejavu/DejaVuSans.ttf 10
:


%preun agent
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-agent.service
%else
%{__service} zabbix-agent stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-agent
%endif
fi
:


%preun server-mysql
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-server.service
%else
%{__service} zabbix-server stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-server
%endif
%{__updalternatives} --remove zabbix-server \
        %{_sbindir}/zabbix_server_mysql
fi
:


%preun server-pgsql
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-server.service
%else
%{__service} zabbix-server stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-server
%endif
%{__updalternatives} --remove zabbix-server \
        %{_sbindir}/zabbix_server_pgsql
fi
:


%preun proxy-mysql
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-proxy.service
%else
%{__service} zabbix-proxy stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-proxy
%endif
%{__updalternatives} --remove zabbix-proxy \
        %{_sbindir}/zabbix_proxy_mysql
fi
:


%preun proxy-pgsql
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-proxy.service
%else
%{__service} zabbix-proxy stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-proxy
%endif
%{__updalternatives} --remove zabbix-proxy \
        %{_sbindir}/zabbix_proxy_pgsql
fi
:


%preun web
if [ "$1" = 0 ]; then
%{__updalternatives} --remove zabbix-web-font \
        %{_datadir}/fonts/dejavu/DejaVuSans.ttf
fi
:


%postun agent
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-agent.service
%else
if [ $1 -ge 1 ]; then
%{__service} zabbix-agent try-restart >/dev/null 2>&1 || :
fi
%endif


%postun server-mysql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-server.service
%else
if [ $1 -ge 1 ]; then
%{__service} zabbix-server try-restart >/dev/null 2>&1 || :
fi
%endif


%postun server-pgsql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-server.service
%else
if [ $1 -ge 1 ]; then
%{__service} zabbix-server try-restart >/dev/null 2>&1 || :
fi
%endif


%postun proxy-mysql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [ $1 -ge 1 ]; then
%{__service} zabbix-proxy try-restart >/dev/null 2>&1 || :
fi
%endif


%postun proxy-pgsql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [ $1 -ge 1 ]; then
%{__service} zabbix-proxy try-restart >/dev/null 2>&1 || :
fi
%endif

################################################################################

%files agent
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-agent-%{version}/
%dir %{_sysconfdir}/zabbix/zabbix_agentd.d

%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix

%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-agent.service
%{_libdir}/tmpfiles.d/zabbix-agent.conf
%else
%{_sysconfdir}/init.d/zabbix-agent
%endif


%files get
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README

%{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get.1*


%files sender
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README

%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender.1*


%files server-mysql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-server-mysql-%{version}/
%dir %{_sysconfdir}/zabbix/alertscripts
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf

%{_mandir}/man8/zabbix_server.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-server.service
%{_libdir}/tmpfiles.d/zabbix-server.conf
%else
%{_sysconfdir}/init.d/zabbix-server
%endif
%{_sbindir}/zabbix_server_mysql


%files server-pgsql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-server-pgsql-%{version}/
%dir %{_sysconfdir}/zabbix/alertscripts
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf

%{_mandir}/man8/zabbix_server.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-server.service
%{_libdir}/tmpfiles.d/zabbix-server.conf
%else
%{_sysconfdir}/init.d/zabbix-server
%endif
%{_sbindir}/zabbix_server_pgsql


%files proxy-mysql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-proxy-mysql-%{version}/
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf

%{_mandir}/man8/zabbix_proxy.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-proxy.service
%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_mysql


%files proxy-pgsql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-proxy-pgsql-%{version}/
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf

%{_mandir}/man8/zabbix_proxy.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-proxy.service
%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_pgsql


%files web
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %attr(0750,apache,apache) %{_sysconfdir}/zabbix/web

%config(noreplace) %{_sysconfdir}/zabbix/web/maintenance.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/zabbix.conf

%ghost %attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/zabbix/web/zabbix.conf.php

%{_datadir}/zabbix


%files web-mysql
%defattr(-,root,root,-)


%files web-pgsql
%defattr(-,root,root,-)

################################################################################

%changelog
* Wed Feb 17 2016 Gleb Goncharov <yum@gongled.ru> - 3.0.0-0 
- Initial build.

