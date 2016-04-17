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

Summary:         Tool for quantizing PNG images in RGBA format
Name:            pngnq
Version:         1.1
Release:         0%{?dist}
Group:           Applications/Multimedia
License:         Unknown
URL:             http://sourceforge.net/projects/pngnq

Source0:         http://kent.dl.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

################################################################################

%description
Pngnq is an adaptation by Stuart Coyle of Greg Roelf's pnqquant using Anthony
Dekker's neuquant algorithm. The neuquant algorithm uses a neural network to
optimize the color map selection. This is fast and quite accurate, giving good
results on many types of images.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING
%doc %{_mandir}/man?/%{name}.*
%{_bindir}/%{name}
%{_bindir}/pngcomp

################################################################################

%changelog
* Thu Dec 31 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.1-0
- Initial build
