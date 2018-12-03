%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _usrbin           /usr/bin
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

################################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

%define _smp_mflags -j1
%define common_name php-xhprof-extension

################################################################################

Summary:        php-xhprof-extension based on tideways/php-xhprof-extension
Name:           php71-xhprof-extension
Version:        4.1.6
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            https://github.com/tideways/php-xhprof-extension

Source0:        https://github.com/tideways/%{common_name}/archive/master.zip
Source1:        40-tideways.ini

BuildRoot:      %{_tmppath}/%{common_name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc php-devel >= 7.1
BuildRequires:  php-devel < 7.2

Requires:       php-cli >= 7.1
Requires:       php-cli < 7.2

################################################################################

%description
Home of the tideways_xhprof extension - a hierarchical Profiler for PHP.

################################################################################

%prep
%setup -qn %{common_name}-master

%build
%{_bindir}/phpize
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -dm 755 %{buildroot}%{_libdir64}/php/modules
install -dm 755 %{buildroot}%{_sysconfdir}/php.d

install -pm 644 modules/tideways_xhprof.so %{buildroot}%{_libdir64}/php/modules/tideways_xhprof.so
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/40-tideways.ini

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%{_libdir64}/php/modules/tideways_xhprof.so
%{_sysconfdir}/php.d/40-tideways.ini

%changelog

* Fri Nov 30 2018 Alexey Egorychev <aegorychev@simtechdev.com> - 4.1.6-0
- Initial build
