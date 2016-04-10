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

Summary:         Recompression utilities for .PNG, .MNG and .ZIP files
Name:            advancecomp
Version:         1.20
Release:         0%{?dist}
Group:           Applications/Multimedia
License:         GPL
URL:             http://advancename.sourceforge.net

Source0:         https://github.com/amadvance/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:   gcc-c++, zlib-devel

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
AdvanceCOMP is a set of recompression utilities for .PNG, .MNG and .ZIP files.
The main features are :
* Recompress ZIP, PNG and MNG files using the Deflate 7-Zip implementation.
* Recompress MNG files using Delta and Move optimization.

################################################################################

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{make_install}

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING HISTORY README
%{_bindir}/*
%{_mandir}/man?/*

################################################################################

%changelog
* Sat Apr 09 2016 Gleb Goncharov <inbox@gongled.me> - 1.20-0 
- Updated to release 1.20.

* Mon Aug 14 2006 Dag Wieers <dag@wieers.com> - 1.15-1 - 7981/dag
- Updated to release 1.15.

* Wed Feb 23 2005 Matthias Saou <http://freshrpms.net/> 1.14-1
- Update to 1.14.

* Mon Nov 29 2004 Matthias Saou <http://freshrpms.net/> 1.13-1
- Update to 1.13.

* Tue Nov  2 2004 Matthias Saou <http://freshrpms.net/> 1.12-1
- Update to 1.12.

* Tue Aug 24 2004 Matthias Saou <http://freshrpms.net/> 1.11-1
- Update to 1.11.

* Mon May 17 2004 Matthias Saou <http://freshrpms.net/> 1.10-1
- Update to 1.10.

* Mon Nov  3 2003 Matthias Saou <http://freshrpms.net/> 1.7-2
- Rebuild for Fedora Core 1.
- Added missing build dependencies, thanks to mach.

* Tue Aug 26 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.7.

* Thu May 22 2003 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.

