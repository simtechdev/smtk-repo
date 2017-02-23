###############################################################################

# rpmbuilder:qa-rpaths 0x0001,0x0010

################################################################################

%define debug_package     %{nil}

################################################################################

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

%define service_user         varnish
%define service_group        varnish
%define service_name         %{name}
%define service_home         %{_localstatedir}/%{name}
%define logger_user          varnishlog

###############################################################################

Summary:           High-performance HTTP accelerator
Name:              varnish
Version:           5.0.0
Release:           0%{?dist}
License:           BSD
Group:             System Environment/Daemons
URL:               https://www.varnish-cache.org/

Source0:           http://repo.varnish-cache.org/source/%{name}-%{version}.tar.gz
Source1:           %{name}.initrc
Source2:           %{name}.sysconfig
Source3:           %{name}.logrotate
Source4:           %{name}_reload_vcl
Source5:           %{name}.params
Source6:           %{name}.service
Source9:           %{name}ncsa.initrc
Source10:          %{name}ncsa.service

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     automake autoconf jemalloc-devel libedit-devel libtool
BuildRequires:     ncurses-devel pcre-devel pkgconfig python-docutils >= 0.6
BuildRequires:     python-sphinx

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
BuildRequires:     systemd-units
%endif

Requires:          gcc jemalloc libedit logrotate ncurses pcre

Requires(pre):     shadow-utils
Requires(post):    /sbin/chkconfig /usr/bin/uuidgen
Requires(preun):   /sbin/chkconfig /sbin/service
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
Requires(post):    systemd-units systemd-sysv
Requires(preun):   systemd-units
Requires(postun):  systemd-units
%endif

Provides:          %{name}-libs = %{version}-%{release}
Provides:          %{name}-docs = %{version}-%{release}
Provides:          %{name}-debuginfo = %{version}-%{release}

Obsoletes:         %{name}-libs < %{version}-%{release}
Obsoletes:         %{name}-docs < %{version}-%{release}
Obsoletes:         %{name}-debuginfo < %{version}-%{release}

Conflicts:         %{name}-libs < %{version}-%{release}
Conflicts:         %{name}-docs < %{version}-%{release}
Conflicts:         %{name}-debuginfo < %{version}-%{release}

###############################################################################

%description
This is Varnish Cache, a high-performance HTTP accelerator.

Varnish Cache stores web pages in memory so web servers don't have to
create the same web page over and over again. Varnish Cache serves
pages much faster than any application server; giving the website a
significant speed up.

Documentation wiki and additional information about Varnish Cache is
available on: https://www.varnish-cache.org/

###############################################################################

%package devel
Summary:           Development files for %{name}
Group:             System Environment/Libraries

BuildRequires:     ncurses-devel

Requires:          %{name} = %{version}-%{release}
Requires:          pkgconfig python

Provides:          %{name}-libs-devel = %{version}-%{release}

Obsoletes:         %{name}-libs-devel < %{version}-%{release}

Conflicts:         %{name}-libs-devel < %{version}-%{release}

%description devel
Development files for %{name}-libs
Varnish Cache is a high-performance HTTP accelerator

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%build
%if 0%{?rhel} == 6
export CFLAGS="$CFLAGS -O2 -g -Wp,-D_FORTIFY_SOURCE=0"
%endif

%configure \
    --localstatedir=%{_sharedstatedir} \
    --without-rst2html
make %{?_smp_mflags}

rm -rf doc/html/_sources doc/sphinx/build

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'

install -dm 755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{_rundir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sbindir}
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
%else
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_initrddir}
%endif

install -pm 644 etc/example.vcl %{buildroot}%{_sysconfdir}/%{name}/default.vcl
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 644 %{SOURCE4} %{buildroot}%{_sbindir}/%{name}_reload_vcl
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
install -pm 644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}.service
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{name}/%{name}.params
install -pm 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}ncsa.service
sed -i 's,sysconfig/varnish,varnish/varnish.params,' %{buildroot}%{_sbindir}/%{name}_reload_vcl
%else
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 755 %{SOURCE9} %{buildroot}%{_initrddir}/%{name}ncsa
%endif

echo %{_libdir}/%{name} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%clean
rm -rf %{buildroot}

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{logger_user} >/dev/null || \
    useradd -r -g %{service_group} -d /dev/null -s /sbin/nologin \
      %{logger_user}
getent passwd %{service_user} >/dev/null || \
    useradd -r -g %{service_group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
      %{service_user}
exit 0

%post
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%service_add_post %{service_name}.service
%service_add_post %{service_name}ncsa.service
%else
%{__chkconfig} --add %{service_name}
%{__chkconfig} --add %{service_name}ncsa
%endif

test -f %{_sysconfdir}/%{name}/secret || \
  (uuidgen > %{_sysconfdir}/%{name}/secret && \
  chmod 0600 %{_sysconfdir}/%{name}/secret)

chown %{logger_user}:%{service_group} %{_logdir}/%{name}/
%{__ldconfig}

%preun
if [[ $1 -eq 0 ]]; then
  %if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
    %service_del_preun %{service_name}.service
    %service_del_preun %{service_name}ncsa.service
  %else
    %{__service} %{name} stop > /dev/null 2>&1
    %{__service} %{name}ncsa stop > /dev/null 2>%1
    %{__chkconfig} --del %{name}
    %{__chkconfig} --del %{name}ncsa
  %endif
fi

%postun
%service_del_postun %{service_name}.service
%service_del_postun %{service_name}ncsa.service
%{__ldconfig}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE doc/html doc/changes*.html
%dir %{_sysconfdir}/%{name}/
%{_sbindir}/*
%{_bindir}/*
%{_sharedstatedir}/%{name}
%{_logdir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%{_docdir}/%{name}/
%{_libdir}/*.so.*
%{_libdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/default.vcl
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%config(noreplace)%{_sysconfdir}/%{name}/%{name}.params
%{_unitdir}/%{service_name}.service
%{_unitdir}/%{service_name}ncsa.service
%else
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{service_name}
%{_initrddir}/%{service_name}ncsa
%endif

%files devel
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_includedir}/%{name}
%{_libdir}/lib*.so
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/%{name}api.pc
%{_datarootdir}/%{name}
%{_datarootdir}/aclocal

###############################################################################

%changelog
* Thu Feb 23 2017 Gleb Goncharov <ggoncharov@simtechdev.com> - 5.0.0-0
- Initial build

