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

%define long_name         MySQLTuner-perl

################################################################################

Summary:        MySQL configuration assistant
Name:           mysqltuner
Version:        1.6.18
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            http://mysqltuner.com/

Source0:        https://github.com/major/%{long_name}/archive/%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{long_name}-%{version}-%{release}

BuildArch:      noarch

################################################################################

%description
MySQLTuner is a script written in Perl that allows you to review a MySQL installation
quickly and make adjustments to increase performance and stability. The current
configuration variables and status data is retrieved and presented in a brief format
along with some basic performance suggestions.

################################################################################

%prep
%setup -qn %{long_name}-%{version}

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_usrbin}

install -pm 644 %{name}.pl \
    %{buildroot}%{_usrbin}/%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(0755,root,root,-)
%{_usrbin}/%{name}

################################################################################

%changelog
* Tue Nov 29 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.6.18-0
- Updated to latest version

* Wed Dec 30 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.6.0-0
- Updated to latest version

* Sat Aug 1 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.4.0-0
- Initial build
