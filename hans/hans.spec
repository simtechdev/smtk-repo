########################################################################################

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

########################################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

########################################################################################

Summary:        IP over ICMP tool
Name:           hans
Version:        0.4.4
Release:        2%{?dist}
License:        GPLv2
Group:          Development/Libraries
URL:            https://github.com/friedrich/hans

Source0:        https://github.com/friedrich/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}.sysconfig

Requires:       kaosv

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  make

BuildRoot:      %{_tmppath}/%{name}-%{version}

ExclusiveArch:  x86_64

Provides:       %{name} = %{version}

########################################################################################

%description
Hans makes it possible to tunnel IPv4 through ICMP echo packets, so you could call it
a ping tunnel. This can be useful when you find yourself in the situation that your
Internet access is firewalled, but pings are allowed.

########################################################################################

%prep
%setup -qn %{name}-%{version}

%clean
%{__rm} -rf %{buildroot}

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

install -dm 755 %{buildroot}
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_initrddir}

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 755 %{SOURCE1} \
                %{buildroot}%{_initrddir}/%{name}
install -pm 644 %{SOURCE2} \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}

cp -ap %{name} %{buildroot}%{_bindir}/%{name}

########################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

########################################################################################

%changelog
* Wed Nov 18 2015 Gleb Goncharov <yum@gongled.me> - 0.4.4-2
- Service config and sysconfig improved.
- Minor fixes related with stability.

* Wed Nov 18 2015 Gleb Goncharov <yum@gongled.me> - 0.4.4-1
- Service and sysconfig added.

* Tue Sep 15 2015 Gleb Goncharov <yum@gongled.me> - 0.4.4-0
- Initial build
