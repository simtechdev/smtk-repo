###############################################################################

%define with_worker_mpm 1

%if %{?rhel} <= 6
%define with_event_mpm  1
%endif

%if %{?rhel} == 7
%define with_event_mpm  0
%endif

###############################################################################

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

###############################################################################

%define httpd_version       2.4.18
%define httpd_mmn           20120211

%define httpd_webroot       /var/www
%define httpd_suexec_caller apache

%define service_user        apache
%define service_group       apache

###############################################################################

Summary:              Apache HTTP Server
Name:                 httpd
Version:              %{httpd_version}
Release:              2%{?dist}
License:              Apache License, Version 2.0
Group:                System Environment/Daemons
URL:                  http://httpd.apache.org/

Source0:              http://www.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
Source1:              %{name}.init
Source2:              %{name}.sysconfig
Source3:              %{name}.conf

Source10:             %{name}-extra-info.conf
Source11:             %{name}-extra-languages.conf
Source12:             %{name}-extra-ssl.conf

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc >= 3.0 ncurses-devel
BuildRequires:        apr-devel, apr-util-devel, openldap-devel, db4-devel, expat-devel, findutils
BuildRequires:        perl, pkgconfig, pcre-devel >= 5.0 libuuid-devel

Requires:             apr >= 1.4.2, apr-util >= 1.3.10, pcre >= 5.0
Requires:             gawk, findutils, openldap, kaosv >= 2.7.0

Requires(post):       /sbin/chkconfig, /bin/mktemp, /bin/rm, /bin/mv
Requires(post):       sh-utils, textutils, /usr/sbin/useradd

Provides:             httpd-mmn = %{httpd_mmn}

Conflicts:            thttpd

Obsoletes:            apache = %{version}-%{release}
Obsoletes:            secureweb = %{version}-%{release}
Obsoletes:            mod_dav = %{version}-%{release}

###############################################################################

%description
Apache is a powerful, full-featured, efficient, and freely-available
Web server. Apache is also the most popular Web server on the
Internet.

###############################################################################

%package devel
Group:                Development/Libraries
Summary:              Development tools for the Apache HTTP server.

Requires:             libtool, httpd = %{version}
Requires:             apr-devel >= 1.4.2, apr-util-devel >= 1.3.10

Obsoletes:            secureweb-devel = %{version}-%{release}
Obsoletes:            apache-devel = %{version}-%{release}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for Apache.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

###############################################################################

%package manual
Group:                Documentation
Summary:              Documentation for the Apache HTTP server.

Obsoletes:            secureweb-manual = %{version}-%{release}
Obsoletes:            apache-manual = %{version}-%{release}

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/.

###############################################################################

%package -n mod_ssl
Group:                System Environment/Daemons
Summary:              SSL/TLS module for the Apache HTTP server

Requires:             openssl-devel
Requires:             httpd, make, httpd-mmn = %{httpd_mmn}

Requires(post):       openssl, dev, /bin/cat

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

###############################################################################

%prep
%setup -q

httpd_vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`

if test "x${httpd_vmmn}" != "x%{httpd_mmn}"; then
    : Error: Upstream MMN is now ${httpd_vmmn}, packaged MMN is %{httpd_mmn}.
    : Update the 'httpd_mmn' macro and rebuild.
    exit 1
fi


%build
rm -rf srclib/{apr,apr-util,pcre}

%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
    support/apxs.in

mkdir -p "prefork"
pushd "prefork"
../configure \
    --prefix=%{_sysconfdir}/httpd \
    --with-apr=/usr/bin/apr-1-config \
    --with-apr-util=/usr/bin/apu-1-config \
    --with-pcre=/usr/bin/pcre-config \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=%{_libdir}/httpd/modules \
    --datadir=%{httpd_webroot} \
    --with-installbuilddir=%{_libdir}/httpd/build \
    --with-mpm=prefork \
    --enable-suexec --with-suexec \
    --with-suexec-caller=%{suexec_caller} \
    --with-suexec-docroot=%{httpd_webroot} \
    --with-suexec-logfile=%{_localstatedir}/log/httpd/suexec.log \
    --with-suexec-bin=%{_sbindir}/suexec \
    --with-suexec-uidmin=500 --with-suexec-gidmin=500 \
    --enable-pie \
    --with-pcre \
    --enable-mods-shared=all \
    --enable-ssl --with-ssl --enable-distcache \
    --enable-proxy \
    --enable-cache \
    --enable-disk-cache \
    --enable-ldap --enable-authnz-ldap \
    --enable-cgid \
    --enable-authn-anon --enable-authn-alias \
    --disable-imagemap

make %{?_smp_mflags}
popd

%if %{with_worker_mpm}
mkdir -p "worker"
pushd "worker"
../configure \
    --prefix=%{_sysconfdir}/httpd \
    --with-apr=/usr/bin/apr-1-config \
    --with-apr-util=/usr/bin/apu-1-config \
    --with-pcre=/usr/bin/pcre-config \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=%{_libdir}/httpd/modules \
    --datadir=%{httpd_webroot} \
    --with-installbuilddir=%{_libdir}/httpd/build \
    --with-mpm=worker \
    --enable-suexec --with-suexec \
    --with-suexec-caller=%{suexec_caller} \
    --with-suexec-docroot=%{httpd_webroot} \
    --with-suexec-logfile=%{_localstatedir}/log/httpd/suexec.log \
    --with-suexec-bin=%{_sbindir}/suexec \
    --with-suexec-uidmin=500 --with-suexec-gidmin=500 \
    --enable-pie \
    --with-pcre \
    --enable-mods-shared=all

make %{?_smp_mflags}
popd
%endif

%if %{with_event_mpm}
mkdir -p "event"
pushd "event"
../configure \
    --prefix=%{_sysconfdir}/httpd \
    --with-apr=/usr/bin/apr-1-config \
    --with-apr-util=/usr/bin/apu-1-config \
    --with-pcre=/usr/bin/pcre-config \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=%{_libdir}/httpd/modules \
    --datadir=%{httpd_webroot} \
    --with-installbuilddir=%{_libdir}/httpd/build \
    --with-mpm=event \
    --enable-suexec --with-suexec \
    --with-suexec-caller=%{suexec_caller} \
    --with-suexec-docroot=%{httpd_webroot} \
    --with-suexec-logfile=%{_localstatedir}/log/httpd/suexec.log \
    --with-suexec-bin=%{_sbindir}/suexec \
    --with-suexec-uidmin=500 --with-suexec-gidmin=500 \
    --enable-pie \
    --with-pcre \
    --enable-mods-shared=all

make %{?_smp_mflags}
popd
%endif


%install
rm -rf %{buildroot}

pushd prefork
    %{make_install} DESTDIR=%{buildroot}
popd

%if %{with_worker_mpm}
install -dm 755 %{buildroot}%{_sbindir}
install -pm 755 worker/httpd %{buildroot}%{_sbindir}/httpd.worker
%endif

%if %{with_event_mpm}
install -dm 755 %{buildroot}%{_sbindir}
install -pm 755 event/httpd %{buildroot}%{_sbindir}/httpd.event
%endif

rm -rf %{buildroot}%{_sysconfdir}/httpd/logs

rm -rf %{buildroot}%{_libdir}/httpd/modules/*.exp \
       %{buildroot}%{httpd_webroot}/htdocs/* \
       %{buildroot}%{httpd_webroot}/cgi-bin/*

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/rc.d/init.d
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/conf.d
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/conf.modules.d
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/vhost.d
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/xtra
install -dm 755 %{buildroot}%{httpd_webroot}/html
install -dm 755 %{buildroot}%{_localstatedir}/lib/dav
install -dm 755 %{buildroot}%{_localstatedir}/cache/mod_ssl
install -dm 755 %{buildroot}%{_localstatedir}/cache/httpd/cache-root
install -dm 755 %{buildroot}%{_localstatedir}/log/httpd

ln -s ../..%{_localstatedir}/log/httpd %{buildroot}/etc/httpd/logs
ln -s ../..%{_localstatedir}/run %{buildroot}/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules %{buildroot}/etc/httpd/modules

mv %{buildroot}%{httpd_webroot}/build %{buildroot}%{_libdir}/httpd/build

install -pm 755 %{SOURCE1} \
                %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
install -pm 644 %{SOURCE2} \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE3} \
                %{buildroot}%{_sysconfdir}/%{name}/conf/%{name}.conf
install -pm 644 build/rpm/httpd.logrotate \
                %{buildroot}/etc/logrotate.d/httpd

install -pm 664 %{SOURCE10} \
                %{buildroot}%{_sysconfdir}/%{name}/conf/extra/%{name}-info.conf
install -pm 664 %{SOURCE11} \
                %{buildroot}%{_sysconfdir}/%{name}/conf/extra/%{name}-languages.conf
install -pm 664 %{SOURCE12} \
                %{buildroot}%{_sysconfdir}/%{name}/conf/extra/%{name}-ssl.conf

chmod 755 %{buildroot}%{_sbindir}/suexec

touch %{buildroot}%{_localstatedir}/cache/mod_ssl/scache.{dir,pag,sem}
echo %{httpd_mmn} > %{buildroot}%{_includedir}/httpd/.mmn


%check
if readelf -d %{buildroot}%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
    : Module contain non-relocatable code
    exit 1
fi


%clean
rm -rf %{buildroot}

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} \
    -s /sbin/nologin -d %{service_home} %{service_user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  /sbin/chkconfig --add httpd
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} httpd stop > /dev/null 2>&1
  %{__chkconfig} --del httpd
fi

###############################################################################

%files
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE NOTICE

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/%{name}/modules
%{_sysconfdir}/%{name}/logs
%{_sysconfdir}/%{name}/run
%dir %{_sysconfdir}/%{name}/conf
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_sysconfdir}/%{name}/conf.modules.d
%dir %{_sysconfdir}/%{name}/xtra
%dir %{_sysconfdir}/%{name}/vhost.d
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/httpd/conf/mime.types
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-manual.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-mpm.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-vhosts.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/proxy-html.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-manual.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-mpm.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-vhosts.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/proxy-html.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/httpd.conf

%config %{_sysconfdir}/logrotate.d/%{name}
%config %{_sysconfdir}/rc.d/init.d/%{name}
%config %{_sysconfdir}/sysconfig/%{name}

%{_bindir}/ab
%{_sbindir}/htcacheclean
%{_bindir}/htdbm
%{_bindir}/htdigest
%{_bindir}/htpasswd
%{_bindir}/logresolve
%{_sbindir}/httpd
%if %{with_worker_mpm}
%{_sbindir}/httpd.worker
%endif
%if %{with_event_mpm}
%{_sbindir}/httpd.event
%endif
%{_bindir}/httxt2dbm
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%{_sbindir}/fcgistarter
%attr(4510,root,%{httpd_suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod_[a-r]*.so
%{_libdir}/httpd/modules/mod_s[petu]*.so
%{_libdir}/httpd/modules/mod_s[lo]*.so
%{_libdir}/httpd/modules/mod_[t-z]*.so

%dir %{httpd_webroot}
%dir %{httpd_webroot}/cgi-bin
%dir %{httpd_webroot}/html
%dir %{httpd_webroot}/icons
%dir %{httpd_webroot}/error
%dir %{httpd_webroot}/error/include
%{httpd_webroot}/icons/*
%{httpd_webroot}/error/README
%config(noreplace) %{httpd_webroot}/error/*.var
%config(noreplace) %{httpd_webroot}/error/include/*.html

%attr(0700,root,root) %dir %{_localstatedir}/log/httpd

%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/cache-root

%{_mandir}/man1/*
%{_mandir}/man8/rotatelogs*
%{_mandir}/man8/suexec*
%{_mandir}/man8/apachectl.8*
%{_mandir}/man8/fcgistarter.8*
%{_mandir}/man8/httpd.8*
%{_mandir}/man8/htcacheclean.8*

###############################################################################

%files manual
%defattr(-,root,root)
%{httpd_webroot}/manual
%{httpd_webroot}/error/README

###############################################################################

%files -n mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/mod_ssl
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.sem

###############################################################################

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_bindir}/apxs
%{_sbindir}/checkgid
%{_bindir}/dbmmanage
%{_sbindir}/envvars*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/instdso.sh
%{_libdir}/httpd/build/config.nice
%{_libdir}/httpd/build/mkdir.sh

###############################################################################

%changelog
* Fri Mar 11 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.2.31-2
- Added custom configs

* Tue Mar 08 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.2.31-1
- Added kaosv, sysconfig and httpd.conf

* Tue Mar 08 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.2.31-0
- Initial build.

