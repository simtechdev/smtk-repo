###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

###############################################################################

%define realname       hiredis
%define minor_ver      13
%define rel            3

###############################################################################

Summary:             Minimalistic C client for Redis
Name:                %{realname}
Version:             0.%{minor_ver}.%{rel}
Release:             0%{?dist}
License:             BSD
Group:               System Environment/Libraries
URL:                 https://github.com/redis/hiredis

Source0:             https://github.com/redis/%{realname}/archive/v0.%{minor_ver}.%{rel}.tar.gz

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       gcc make

###############################################################################

%description 
Hiredis is a minimalistic C client library for the Redis database.

###############################################################################

%package devel
Summary:             Header files and libraries for hiredis C development
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description devel 
The %{name}-devel package contains the header files and 
libraries to develop applications using a Redis database.

###############################################################################

%prep
%setup -qn %{realname}-0.%{minor_ver}.%{rel}

%build
%{__make} %{?_smp_mflags} OPTIMIZATION="%{optflags}" 

%install
%{__rm} -rf %{buildroot}
%{__make} install PREFIX=%{buildroot}%{_prefix} INSTALL_LIBRARY_PATH=%{buildroot}%{_libdir} LIBRARY_PATH=%{buildroot}%{_libdir}

ln -s %{_libdir}/lib%{name}.so.0.%{minor_ver} %{buildroot}%{_libdir}/lib%{name}.so.0

%clean 
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.0.%{minor_ver}
%{_libdir}/lib%{name}.so.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{realname}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/%{realname}.pc

###############################################################################

%changelog
* Mon Mar 21 2016 Gleb Goncharov <yum@gongled.ru> - 0.13.3-0
- Initial build 

