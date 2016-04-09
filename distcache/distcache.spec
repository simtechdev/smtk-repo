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

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

###############################################################################

%define service_user     distcache
%define service_group    distcache
%define service_home     /

###############################################################################

Summary:           Distributed SSL session cache
Name:              distcache
Version:           1.4.5
Release:           0%{?dist}
License:           LGPLv2
Group:             System Environment/Daemons
URL:               http://www.distcache.org/

Source0:           http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:           dc_server.init
Source2:           dc_client.init

Patch0:            %{name}-%{version}-setuid.patch
Patch1:            %{name}-%{version}-libdeps.patch
Patch2:            %{name}-%{version}-limits.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:     automake >= 1.7, autoconf >= 2.50, libtool, openssl-devel

Requires(post):    /sbin/chkconfig, /sbin/ldconfig, shadow-utils
Requires(preun):   /sbin/service, /sbin/chkconfig

###############################################################################

%description
The distcache package provides a variety of functionality for
enabling a network-based session caching system, primarily for
(though not restricted to) SSL/TLS session caching.

###############################################################################

%package devel
Summary:           Development tools for distcache distributed session cache
Group:             Development/Libraries
Requires:          %{name} = %{version}-%{release}

%description devel
This package includes the libraries that implement the necessary
network functionality, the session caching protocol, and APIs for
applications wishing to use a distributed session cache, or indeed
even to implement a storage mechanism for a session cache server.

###############################################################################

%prep
%setup -q
%patch0 -p1 -b .setuid
%patch1 -p1 -b .libdeps
%patch2 -p1 -b .limits

%build
libtoolize --force --copy && aclocal && autoconf
automake -aic || : automake failed
pushd ssl
autoreconf -i || : autoreconf failed
popd

%configure --enable-shared --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install} DESTDIR=%{buildroot}
%{__make} -C ssl install DESTDIR=%{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/rc.d/init.d

install -pm 755 %{SOURCE1} \
        %{buildroot}%{_sysconfdir}/rc.d/init.d/dc_server
install -pm 755 %{SOURCE2} \
        %{buildroot}%{_sysconfdir}/rc.d/init.d/dc_client

rm -f %{buildroot}%{_bindir}/{nal_test,piper} \
      %{buildroot}%{_libdir}/lib*.la

%clean
rm -rf %{buildroot}

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} -s /sbin/nologin -d %{service_home} %{service_user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
    %{__chkconfig} --add dc_server
    %{__chkconfig} --add dc_client
    %{__ldconfig} 
fi

%preun
if [[ $1 -eq 0 ]]; then
    %{__service} dc_server stop > /dev/null 2>&1
    %{__service} dc_client stop > /dev/null 2>&1
    %{__chkconfig} --del dc_server
    %{__chkconfig} --del dc_client
fi

%postun -p %{__ldconfig} 

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/sslswamp
%{_bindir}/dc_*
%{_sysconfdir}/rc.d/init.d/dc_*
%doc ANNOUNCE CHANGES README LICENSE FAQ
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/swamp

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_includedir}/libnal
%{_libdir}/*.so
%{_mandir}/man2/*

###############################################################################

%changelog
* Sat Apr 09 2016 Gleb Goncharov <yum@gongled.ru> - 1.4.5-0
- Initial build 

