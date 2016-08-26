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

################################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

Summary:         Real-time web log analyzer and interactive viewer
Name:            goaccess
Version:         0.9.8
Release:         0%{?dist}
Group:           Development/Tools
License:         GPLv2+
URL:             http://goaccess.io

Source0:         http://tar.goaccess.io/goaccess-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        GeoIP
BuildRequires:   gcc-c++ make GeoIP-devel glib2-devel ncurses-devel

################################################################################

%description
Open source real-time web log analyzer and interactive viewer that runs
in a terminal in *nix systems. It provides fast and valuable HTTP statistics
for system administrators that require a visual server report on the fly.

################################################################################

%prep
%setup -q

%build
%configure --enable-debug --enable-geoip --enable-utf8

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

################################################################################

%changelog
* Wed Mar 09 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 0.9.8-0
- Updated to latest release
