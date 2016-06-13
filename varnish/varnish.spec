################################################################################

%define _posixroot          /
%define _root               /root
%define _bin                /bin
%define _sbin               /sbin
%define _srv                /srv
%define _home               /home
%define _opt                /opt
%define _lib32              %{_posixroot}lib
%define _lib64              %{_posixroot}lib64
%define _libdir32           %{_prefix}%{_lib32}
%define _libdir64           %{_prefix}%{_lib64}
%define _logdir             %{_localstatedir}/log
%define _rundir             %{_localstatedir}/run
%define _lockdir            %{_localstatedir}/lock/subsys
%define _cachedir           %{_localstatedir}/cache
%define _spooldir           %{_localstatedir}/spool
%define _crondir            %{_sysconfdir}/cron.d
%define _loc_prefix         %{_prefix}/local
%define _loc_exec_prefix    %{_loc_prefix}
%define _loc_bindir         %{_loc_exec_prefix}/bin
%define _loc_libdir         %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32       %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64       %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir     %{_loc_exec_prefix}/libexec
%define _loc_sbindir        %{_loc_exec_prefix}/sbin
%define _loc_bindir         %{_loc_exec_prefix}/bin
%define _loc_datarootdir    %{_loc_prefix}/share
%define _loc_includedir     %{_loc_prefix}/include
%define _loc_mandir         %{_loc_datarootdir}/man
%define _rpmstatedir        %{_sharedstatedir}/rpm-state
%define _pkgconfigdir       %{_libdir}/pkgconfig

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

#################################################################################

%define service_user varnish
%define service_user_log varnishlog
%define service_group varnish

#################################################################################

Summary:          High-performance HTTP accelerator
Name:             varnish
Version:          4.1.1
Release:          2%{?dist}
License:          BSD
Group:            System Environment/Daemons
URL:              https://www.varnish-cache.org/

Source0:          http://repo.varnish-cache.org/source/%{name}-%{version}.tar.gz
Source1:          %{name}.init
Source2:          %{name}.sysconfig
Source3:          %{name}.logrotate
Source4:          varnish_reload_vcl
Source6:          %{name}.service
Source7:          %{name}log.init
Source8:          %{name}log.service
Source9:          %{name}ncsa.init
Source10:         %{name}ncsa.service

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    gcc-c++ automake autoconf jemalloc-devel libedit-devel libtool
BuildRequires:    ncurses-devel pcre-devel pkgconfig python-docutils >= 0.6 python-sphinx
%if 0%{?rhel} >= 7
BuildRequires:    systemd-units
%endif

Requires:         gcc kaosv jemalloc libedit logrotate ncurses pcre pkgconfig python
Requires:         varnish-libs = %{version}-%{release}

Requires(pre):    shadow-utils
Requires(post):   /sbin/chkconfig, /usr/bin/uuidgen
Requires(preun):  /sbin/chkconfig
Requires(preun):  /sbin/service
%if 0%{?rhel} >= 7
Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units
%endif

#################################################################################

%description
This is Varnish Cache, a high-performance HTTP accelerator.

Varnish Cache stores web pages in memory so web servers don't have to
create the same web page over and over again. Varnish Cache serves
pages much faster than any application server; giving the website a
significant speed up.

Documentation wiki and additional information about Varnish Cache is
available on the following web site: https://www.varnish-cache.org/

#################################################################################

%package libs
Summary:          Libraries for %{name}
Group:            System Environment/Libraries

BuildRequires:    ncurses-devel

%description libs
Libraries for %{name}. Varnish Cache is a high-performance HTTP accelerator

#################################################################################

%package libs-devel
Summary:          Development files for %{name}-libs
Group:            System Environment/Libraries

BuildRequires:    ncurses-devel

Requires:         varnish-libs = %{version}-%{release}

%description libs-devel
Development files for %{name}-libs. Varnish Cache is a high-performance HTTP accelerator

#################################################################################

%prep
%setup -qn %{name}-%{version}

%build
export CFLAGS="$CFLAGS -O2 -g -Wp,-D_FORTIFY_SOURCE=0"

libtoolize --copy --force
aclocal -I m4
autoheader
automake --add-missing --copy --foreign
autoconf
%configure

make %{?_smp_mflags}
rm -rf doc/html

%install
rm -rf %{buildroot}

make install \
    DESTDIR=%{buildroot} \
    INSTALL="install -p"

find %{buildroot}%{_libdir}/ -name '*.la' -delete

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -dm 755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{_rundir}/%{name}
%if 0%{?rhel} == 6
install -dm 755 %{buildroot}%{_initrddir}
%endif
%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
%endif

install -pm 644 etc/example.vcl %{buildroot}%{_sysconfdir}/%{name}/default.vcl
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 755 %{SOURCE4} %{buildroot}%{_sbindir}
%if 0%{?rhel} == 6
install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 755 %{SOURCE7} %{buildroot}%{_initrddir}/%{name}log
install -pm 755 %{SOURCE9} %{buildroot}%{_initrddir}/%{name}ncsa
%endif
%if 0%{?rhel} >= 7
install -pm 0644 %{SOURCE6} %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE8} %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE10} %{buildroot}%{_unitdir}
%endif

# echo %{_libdir}/varnish > %{buildroot}%{_sysconfdir}/ld.so.conf.d/varnish-%{_arch}.conf

%clean
rm -rf %{buildroot}

###############################################################################

%pre
if [[ $1 -eq 1 ]] ; then
    %{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
    %{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin %{service_user}
    %{__getent} passwd %{service_user_log} >/dev/null || \
        %{__useradd} -r -g %{service_group} -d /dev/null -s /sbin/nologin %{service_user_log}
fi
exit 0

%post
%if 0%{?rhel} == 6
if [[ $1 -eq 1 ]] ; then
    %{__chkconfig} --add %{name}
    %{__chkconfig} --add %{name}log
    %{__chkconfig} --add %{name}ncsa
fi
%endif

%if 0%{?rhel} == 7
if [[ $1 -eq 1 ]] ; then
    %{systemd_post} %{name}.service
    %{systemd_post} %{name}log.service
    %{systemd_post} %{name}ncsa.service
fi
%endif

if [[ ! -f %{_sysconfdir}/%{name}/secret ]] ; then
    uuidgen > %{_sysconfdir}/%{name}/secret
    chmod 600 %{_sysconfdir}/%{name}/secret
fi

%preun
%if 0%{?rhel} >= 7
if [[ $1 -lt 1 ]] ; then
    %{systemd_preun} %{name}.service
    %{systemd_preun} %{name}log.service
    %{systemd_preun} %{name}ncsa.service
fi
%endif

%if 0%{?rhel} >= 7
if [[ $1 -lt 1 ]] ; then
    %{__service} %{name} stop &> /dev/null
    %{__service} %{name}log stop &> /dev/null
    %{__service} %{name}ncsa stop &> /dev/null
    %{__chkconfig} --del %{name}
    %{__chkconfig} --del %{name}log
    %{__chkconfig} --del %{name}ncsa
fi
%endif

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{_sysconfdir}/%{name}
%dir %attr(755,%{service_user_log},%{service_group}) %{_logdir}/%{name}
%{_sbindir}/*
%{_bindir}/*
%{_sharedstatedir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%{_docdir}/%{name}/

%config(noreplace) %{_sysconfdir}/%{name}/default.vcl
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%if 0%{?rhel} == 6
%{_initrddir}/%{name}
%{_initrddir}/%{name}log
%{_initrddir}/%{name}ncsa
%endif

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}ncsa.service
%{_unitdir}/%{name}log.service
%endif

%files libs
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*
%{_libdir}/%{name}

%files libs-devel
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/lib*.so
%dir %{_includedir}/varnish
%{_includedir}/varnish/*
%{_libdir}/pkgconfig/varnishapi.pc
%{_datarootdir}/%{name}
%{_datarootdir}/aclocal

###############################################################################

%changelog
* Wed Jun 08 2016 Alexey Egorychev <aegorychev@simtechdev.com> - 4.1.1-2
- Change init script for using kaosv.
- Remove unused variables.

* Thu Jul 24 2014 Lasse Karstensen <lkarsten@varnish-software.com> - 4.1.1-1
- This changelog is not in use. See doc/changes.rst for release notes.

