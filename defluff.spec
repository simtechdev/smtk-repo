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

%ifarch x86_64
%define release_arch      x86_64
%else
%define release_arch      i386 
%endif

###############################################################################

Summary:         Tool, which works on existing deflate streams
Name:            defluff
Version:         0.3.2
Release:         0%{?dist}
Group:           Applications/Multimedia
License:         Freeware
URL:             http://encode.ru/threads/1214-defluff-a-deflate-huffman-optimizer

Source0:         https://source.gongled.me/%{name}/%{name}-%{version}.%{release_arch}.zip

ExclusiveArch:   %{release_arch}

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
It repeats the huffman coding step of the deflate process, trying to find a 
representation that is as short as possible. Since most deflate implementations
are optimized for speed, they don't try that hard, and defluff is often able to
squeeze out a few more bits.

###############################################################################

%prep
%setup -qcn %{name}-%{version}

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 %{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

###############################################################################

%changelog
* Thu Dec 31 2015 Gleb Goncharov <yum@gongled.me> - 0.3.2-0
- Initial build 

