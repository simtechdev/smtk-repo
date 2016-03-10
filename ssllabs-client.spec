###############################################################################

# rpmbuilder:relative-pack true

###############################################################################

%define  debug_package %{nil}

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

Summary:         Command-line client for the SSL Labs API
Name:            ssllabs-client
Version:         1.0.8
Release:         0%{?dist}
Group:           Applications/System
License:         EKOL
URL:             http://essentialkaos.com

Source0:         https://source.kaos.io/%{name}/%{name}-%{version}.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.4

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Command-line client for the SSL Labs API.

###############################################################################

%prep
%setup -q

%build
export GOPATH=$(pwd)

mkdir -p src/github.com/essentialkaos
mkdir -p src/pkg.re/essentialkaos

mv ssllabs.v1 src/pkg.re/essentialkaos
mv ek.v1 src/pkg.re/essentialkaos
mv ssllabs_client src/github.com/essentialkaos

go build src/github.com/essentialkaos/ssllabs_client/%{name}.go

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 %{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.EN LICENSE.RU
%{_bindir}/%{name}

###############################################################################

%changelog
* Fri Jan 15 2016 Gleb Goncharov <yum@gongled.me> - 1.0.8-0
- Updated to latest version 

* Wed Dec 30 2015 Gleb Goncharov <yum@gongled.me> - 1.0.5-0
- Updated to latest version 

* Sat Nov 14 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.4-0
- Small minor fixes

* Wed Oct 14 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.3-0
- Fixed output for custom formats
- Minor fixes

* Tue Oct 13 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Fixed output for check result without grade
- Fixed progress output for empty statusMessages
- Improved forwarding warnings
- Improved DH public server param (Ys) reuse warnings
- Improved help

* Mon Oct 12 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- Fixed bug with detailed output for endpoint without https support
- Added dev api support

* Thu Oct 08 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- Initial release
