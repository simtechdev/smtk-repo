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

Summary:         Utilities for image_optim tool. 
Name:            imageoptim-utils
Version:         0.1
Release:         0%{?dist}
Group:           Applications/Multimedia
License:         GPL 
URL:             http://source.gongled.me 

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:        advancecomp
Requires:        gifsicle
Requires:        jhead
Requires:        jpegoptim
Requires:        libjpeg-turbo
Requires:        optipng
Requires:        pngcrush
Requires:        pngout
Requires:        pngquant

################################################################################

%description
Bundle of optimization tools for 

################################################################################

%build
%{__rm} -rf %{buildroot}
touch README

%install
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}
install -pm 644 README %{buildroot}%{_loc_datarootdir}/%{name}/README

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc %{_loc_datarootdir}/%{name}/README

################################################################################

%changelog
* Thu Dec 31 2015 Gleb Goncharov <yum@gongled.me> - 0.1-0
- Initial build

