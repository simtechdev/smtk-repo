################################################################################

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

Summary:        GONGLED repository for CentOS/RHEL
Name:           gongled-release
Version:        0.1
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://yum.gongled.ru/

Source0:        gongled-release.repo
Source1:        gongled-testing.repo
Source2:        RPM-GPG-KEY-GONGLED

Requires:       epel-release 
Requires:       yum-plugin-priorities

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

################################################################################

%description
This package contains yum repo file for access to gongled's repository.

################################################################################

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -dm 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -pm 644 %{SOURCE0} \
    %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/pki/rpm-gpg

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
%config(noreplace) /etc/pki/rpm-gpg/*

################################################################################

%changelog
* Sun Aug 02 2015 Gleb Goncharov <yum@gongled.me> - 0.1-0
- Initial build.
