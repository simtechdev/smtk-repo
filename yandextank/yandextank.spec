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

%define   package_name   yandex-tank

################################################################################

Summary:        Performance measure tool
Name:           yandextank
Version:        1.7.30
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            https://tech.yandex.ru/tank/

Source0:        https://pypi.python.org/packages/source/y/%{name}/%{name}-%{version}.tar.gz

Patch0:         %{name}.patch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  python-devel

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      x86_64

Requires:       python-importlib
Requires:       python-ipaddr
Requires:       python-lxml
Requires:       python-psutil
Requires:       python-progressbar
Requires:       python-requests
Requires:       python-tornado
Requires:       python-TornadIO2

################################################################################

%description
Yandex.Tank is an extendable open source load testing tool for advanced linux users
which is especially good as a part of automated load testing suit.

################################################################################

%prep
%setup -qn %{name}-%{version}
%patch0 -p1

%clean
rm -rf %{buildroot}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_usrbin}/%{package_name}

################################################################################

%changelog
* Tue Feb 23 2016 Gleb Goncharov <yum@gongled.me> - 1.7.30-0
- Updated to the latest version.

* Sun Aug 2 2015 Gleb Goncharov <yum@gongled.me> - 1.7.12-2
- Reduce limits of resource checks.

* Sat Aug 1 2015 Gleb Goncharov <yum@gongled.me> - 1.7.12-1
- Minor fix with dependencies.

* Sat Aug 1 2015 Gleb Goncharov <yum@gongled.me> - 1.7.12-0
- Initial build
