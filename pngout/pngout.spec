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

%define release_ver       20150319

%ifarch x86_64
%define release_arch      x86_64
%else
%define release_arch      i686
%endif

###############################################################################

Summary:         Optimizer for PNG images 
Name:            pngout
Version:         2015.03.19
Release:         0%{?dist}
Group:           Applications/System
License:         Freeware
URL:             http://www.jonof.id.au/pngout

Source0:         http://static.jonof.id.au/dl/kenutils/%{name}-%{release_ver}-linux-static.tar.gz

ExclusiveArch:   %{release_arch}

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Freeware command line optimizer for PNG images written by Ken Silverman. 
The transformation is lossless, meaning that the resulting image is visually 
identical to the source image. This program can often get higher compression
than other optimizers by 5–10%.

###############################################################################

%prep
%setup -qn %{name}-%{release_ver}-linux-static

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 %{release_arch}/%{name}-static %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

###############################################################################

%changelog
* Wed Dec 30 2015 Gleb Goncharov <yum@gongled.me> - 1.0.0-0
- Initial build 

