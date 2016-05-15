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

Summary:         Terminal session recorder
Name:            asciinema
Version:         1.2.0
Release:         0%{?dist}
Group:           Applications/System
License:         GPLv3
URL:             https://asciinema.org

Source0:         %{name}-%{version}.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.4

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Asciinema [as-kee-nuh-muh] is a free and open source solution for recording 
terminal sessions and sharing them on the web.

###############################################################################

%prep
%setup -q

%build
export GOPATH=$(pwd)

mkdir -p .src && mv * .src && mv .src src

pushd src/github.com/%{name}/%{name}
    go build
    cp *.md $GOPATH
    cp LICENSE $GOPATH
    cp man/%{name}.1 $GOPATH
    mv %{name} $GOPATH
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}

install -pm 755 %{name} %{buildroot}%{_bindir}/
install -pm 755 %{name}.1 %{buildroot}%{_mandir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc CONTRIBUTING.md CHANGELOG.md LICENSE README.md
%{_mandir}/%{name}.1
%{_bindir}/%{name}

###############################################################################

%changelog
* Tue Apr 26 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.2.0-0
- Initial build.

