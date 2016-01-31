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

%define release_manpage   man1
%define release_mandir    %{_prefix}/man/%{release_manpage}

################################################################################

Summary:         Advanced PNG optimizer
Name:            optipng
Version:         0.7.5
Release:         0%{?dist}
Group:           Applications/Multimedia
License:         zlib/libpng
URL:             http://optipng.sourceforce.net/

Source0:         http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:   bash, binutils, gcc, make
BuildRequires:   glibc-devel
BuildRequires:   zlib-devel

################################################################################

%description
OptiPNG is a PNG optimizer that recompresses image files to a smaller size,
without losing any information. This program also converts external formats
(BMP, GIF, PNM and TIFF) to optimized PNG, and performs PNG integrity checks
and corrections.

################################################################################

%prep
%setup

%build
%{__rm} -rf %{buildroot}

./configure --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --with-system-zlib

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__gzip} -f %{buildroot}%{release_mandir}/%{name}.1

%{__install} -dm 755 %{buildroot}%{_loc_mandir}/%{release_manpage}

%{__mv} %{buildroot}%{release_mandir}/%{name}.1.gz \
    %{buildroot}%{_loc_mandir}/%{release_manpage}/%{name}.1.gz 

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%doc LICENSE.txt README.txt doc/*
%doc %{_loc_mandir}/%{release_manpage}/%{name}.1.gz
%{_bindir}/%{name}

################################################################################

%changelog
* Wed Dec 30 2015 Gleb Goncharov <yum@gongled.me> - 0.7.5-0
- Updated to latest version

* Fri Apr 16 2010 Steve Huff <shuff@vecna.org> - 0.6.4-1 - 8772/shuff
- Updated to 0.6.4.
- Converted to new configure script.

* Tue Feb 02 2010 Steve Huff <shuff@vecna.org> - 0.6.3-1
- Initial package.
