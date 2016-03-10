########################################################################################

%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache

%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include

%define zshcompl        %{_datarootdir}/zsh/site-functions
%define bashcompl       %{_sysconfdir}/bash_completion.d

########################################################################################

Summary:            YUM repository management utility
Name:               rep
Version:            1.6.4
Release:            0%{?dist}
License:            EKOL
Group:              Applications/System
URL:                http://essentialkaos.com
Vendor:             ESSENTIAL KAOS

Source0:            https://source.kaos.io/%{name}/%{name}-%{version}.tar.bz2

BuildArch:          noarch
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           createrepo_c sqlite rpm expect gawk bc

Provides:           %{name} = %{version}-%{release}

########################################################################################

%description
YUM repository management utility.

########################################################################################

%prep
%setup -q

%build
%install
rm -rf %{buildroot}

%{__install} -dm 755 %{buildroot}%{_bindir}
%{__install} -dm 755 %{buildroot}%{_sysconfdir}
%{__install} -dm 755 %{buildroot}%{zshcompl}
%{__install} -dm 755 %{buildroot}%{bashcompl}
%{__install} -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d

%{__install} -pm 755 %{name} %{buildroot}%{_bindir}/

%{__install} -pm 644 %{name}.conf %{buildroot}%{_sysconfdir}/
%{__install} -pm 644 %{name}.zsh %{buildroot}%{zshcompl}/_%{name}
%{__install} -pm 644 %{name}.bash %{buildroot}%{bashcompl}/%{name}

%{__install} -pm 644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
%{__rm} -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
  %{__mkdir} -p %{_cachedir}/%{name}/meta
  %{__mkdir} -p %{_cachedir}/%{name}/conf

  %{__chmod} 777 %{_cachedir}/%{name}/meta
  %{__chmod} 777 %{_cachedir}/%{name}/conf

  %{__mkdir} -p %{_logdir}/%{name}

  touch %{_logdir}/%{name}/testing.log
  touch %{_logdir}/%{name}/release.log

  %{__chmod} 666 %{_logdir}/%{name}/testing.log
  %{__chmod} 666 %{_logdir}/%{name}/release.log
fi

%postun
if [[ $1 -eq 0 ]] ; then
  %{__rm} -rf %{_cachedir}/%{name}
  %{__rm} -rf %{_logdir}/%{name}
fi

########################################################################################

%files
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/%{name}.conf
%doc LICENSE.EN LICENSE.RU
%{_bindir}/%{name}
%{_sysconfdir}
%{zshcompl}
%{bashcompl}

########################################################################################

%changelog
* Fri Aug 07 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.4-0
- Improved info output
- Refactoring

* Thu Jul 02 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.3-0
- Fixed bug with reindexation after interrupted indexation

* Fri Mar 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.2-0
- Code refactoring
- Improved UI

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Added negative search support for dates
- Fixed some minor bugs with UX

* Sat Nov 08 2014 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Negative search
- Some minor improvements and bugfixes
- Added new syntax for working with groups

* Fri Jul 04 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.6-0
- Small minor fixes in UI

* Tue Jul 01 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.5-0
- Improved date parsing in search query
- Small fixes in UI

* Fri Jun 20 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.4-0
- Fixed bug with signing package while releasing

* Mon Apr 28 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- Improved working with groups
- Improved group info output
- Fixed some minor bugs

* Sun Apr 27 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Fixed verion number

* Fri Apr 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-1
- Fixed dependencies

* Fri Apr 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Fixed bug with search command

* Fri Apr 18 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Improved info command
- Fixed bug with replace packages
- Some minor fixes

* Fri Dec 06 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- Fixed minor bug with text output

* Wed Dec 04 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Fixed bug with pre-add command
- Code refactoring
- Some minor UI fixes
- Changed separator length to 88 symbols

* Mon Dec 02 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.1-0
- Fixed bug with skipping some packages at release

* Thu Nov 14 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- Groups support
- Exact search support
- List command now shows only latest packages
- Small UI improvements
- Some minor improvements

* Fri Oct 04 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.8-0
- Fixed bug with checking some src packages
- Fixed bug with checking sign

* Wed Sep 25 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.7-0
- Improved argument parsing
- Improved info command
- Improved performance

* Sun Aug  4 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.6-0
- Improved config parsing
- Improved argument parsing
- Improved overall performance
- Shmin usage

* Sun Jul 28 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.5-0
- Fixed bug with adding package from current dir
- Added more command aliases
- Minor UI improvements

* Thu Jul  4 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-0
- Some UI improvements

* Sun Jun 30 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.3-0
- Add no-colors argument
- Version changed to new versioning policy

* Wed Jun 26 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- Improved info command output
- Fixed bug with meta cache building

* Tue Jun 25 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- Improved add command
- Fixed some minor bugs in add command

* Mon Jun 24 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Added init command for init file structure
- Added info command for view package information
- Small improvements

* Wed Jun 19 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Using createrepo_c instead createrepo (now reindex blazing fast)
- New metadata build system (now meta rebuilding incredible fast)
- Added more createrepo args in config

* Wed Jun 19 2013 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Fixed bug with secure signing
- Updated argument parsing

* Thu Jun 13 2013 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Improved package processing
- Renaming added packages to default name format

* Thu Jun 13 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.4-0
- Fixed minor bug with version showing
- Updated bash script compression

* Wed Apr 10 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.3-0
- Added information about time spent for reindex and meta update
- Fixed reindex bug with createrepo-0.9.9-17+
- New simplified search
- Full reindex support

* Thu Jan 24 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Fixed config replace bug in spec file

* Tue Jan 22 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- Fixed bug with package signing on systems with non-latin locale
- Fixed bug with --move argument usage
- Fixed bug with reindex and meta update when no package was added or released
- Improved argument parsing
- Improved search query processing
- Improved pre/post command handlers executing
- Improved batch package signing
- Improved search output
- Improved package list output
- Added --no-source argument for source package skipping
- Added autocomplete for bash
- Added autocomplete for zsh
- Added actions logging

* Mon Jun 18 2012 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- First public release
