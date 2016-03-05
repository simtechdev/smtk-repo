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

%define short_name        imagew

###############################################################################

Summary:         Raster image scaling and processing utility. 
Name:            imageworsener
Version:         1.3.0
Release:         0%{?dist}
Group:           Applications/Multimedia
License:         GPLv3+
URL:             http://entropymine.com/imageworsener

Source0:         https://github.com/jsummers/%{name}/archive/%{version}.tar.gz 

BuildRequires:   binutils, make, gcc, libjpeg-turbo-devel

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
ImageWorsener is a raster image scaling and processing utility. All nontrivial 
automated image processing causes a loss of information. While ImageWorsener 
will degrade your images, its goal is to degrade them as little as possible.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
pushd scripts
%{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 %{short_name} %{buildroot}%{_bindir}/%{short_name}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{short_name}

###############################################################################

%changelog
* Wed Dec 30 2015 Gleb Goncharov <yum@gongled.me> - 1.0.0-0
- Initial build 

