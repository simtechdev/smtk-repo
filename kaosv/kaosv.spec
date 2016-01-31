###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

###############################################################################

Summary:         Bash lib for SysV init scripts
Name:            kaosv
Version:         2.7.2
Release:         0%{?dist}
Group:           Applications/System
License:         EKOL
URL:             http://essentialkaos.com
Vendor:          ESSENTIAL KAOS

Source0:         https://source.kaos.io/%{name}/%{name}-%{version}.tar.bz2

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        daemonize bash >= 4.0

###############################################################################

%description
Bash lib for SysV init scripts.

###############################################################################

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_initddir}
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}

install -pm 644 %{name} %{buildroot}%{_initddir}/
install -pm 755 supervisor %{buildroot}%{_loc_datarootdir}/%{name}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.EN LICENSE.RU
%{_initddir}/%{name}
%{_loc_datarootdir}/%{name}/supervisor

###############################################################################

%changelog
* Tue Nov 17 2015 Anton Novojilov <andy@essentialkaos.com> - 2.7.2-0
- Improved working with limits

* Tue Nov 10 2015 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- Fixed minor bug with output for unknown commands

* Wed Oct 28 2015 Anton Novojilov <andy@essentialkaos.com> - 2.7.0-0
- Return exit code 3 for status command if service is stoppped

* Sat Oct 24 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6.1-0
- Minor improvements

* Tue Aug 11 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- Added methods for executing default handlers (kv.start, kv.stop, kv.restart,
  kv.status, kv.usage)
- Added method for kaosv version compatibility check (kv.require)
- Code refactoring

* Sun Jul 26 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.5-0
- Fixed bug with status command which works only with sudo priveleges

* Fri Jul 24 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.4-0
- Fixed bug with pid and lock files naming

* Tue Jun 02 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.3-0
- Fixed minor bug with log file overriding with kv.daemonize

* Wed Mar 25 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.2-0
- Fixed bug with unchanged owner for pid dir
- Added restart pre and post handlers

* Sat Feb 21 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.1-0
- Fixed bug with checking safe paths
- Fixed bug with pid creation with kv.daemonize

* Mon Feb 02 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5-0
- Fixed bug with redefining basic commands
- Fixed bug with reading property from file
- Some minor improvements
- Refactoring

* Wed Dec 31 2014 Anton Novojilov <andy@essentialkaos.com> - 2.4-0
- Added property oom_adj for setting oom killer adjustment level

* Mon Dec 29 2014 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Fixed minor bug with user checking

* Fri Dec 26 2014 Anton Novojilov <andy@essentialkaos.com> - 2.3-0
- kv.daemonize create pid only if auto_pid is true

* Tue Dec 23 2014 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- Added supervisor feature

* Sat Nov 15 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1-0
- Added stdout and stderr redirection to kv[log] for kv.daemonize

* Fri Nov 07 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- Fixed typo

* Sat Oct 18 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0-0
- Changed syntax for kv.run function
- Added kv.error and kv.warn functions
- kv.run now uses user property by default
- Added kv.runAs function
- Added limits support in kv.daemonize
- Added ionice configuration
- Added nice and ionice support in kv.daemonize
- Added ionice support in kv.run (kv.runAs)
- Added support for nofile and nproc limits in kv.run and kv.daemonize
- daemonize_user property renamed to user
- daemonize_dir renamed to dir
- Added additional checks for dir and user properties
- Added property auto_actions_log for activation automatic logging about
  user actions (start, stop, etc...)
- Fixed major bug with limits while kv.daemonize usage
- Fixed major bug with arguments scope in kv.run
- Fixed minor bug with wrong pid owner after pid file restore
- Performance improvements

* Fri Oct 17 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Fixed bug with output redirection to log and default logger
- Small improvements

* Thu Oct 16 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Added method kv.checkSELinux for checking selinux mode

* Fri Oct 10 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- Fixed bug in prepare stage (users can't execute some commands without
  superuser privileges)
- Improved problems fixing
- Some minor improvements

* Tue Sep 16 2014 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Fixed major bug with directory creation in / directory
- Some minor improvements
