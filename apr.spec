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

%define apr_version 1

###############################################################################

Summary:         Apache Portable Runtime library
Name:            apr
Version:         1.5.2
Release:         0%{?dist}
Group:           System Environment/Libraries
License:         APL
URL:             https://apr.apache.org/

Source0:         http://www.apache.org/dist/%{name}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:   autoconf, libtool, doxygen, python

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

###############################################################################

%package devel
Group:           Development/Libraries
Summary:         APR library development kit
Requires:        %{name} = %{version}

%description devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.

###############################################################################

%prep
%setup -q

%build
./buildconf

%{configure} \
        --prefix=/usr \
        --includedir=%{_includedir}/apr-%{apr_version} \
        --with-installbuilddir=%{_libdir}/apr/build-%{apr_version} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

%{__make} %{?_smp_mflags}
%{__make} dox

%install
rm -rf %{buildroot} 

%{make_install} DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/apr.exp
mv docs/dox/html html

%clean
rm -rf %{buildroot}

###############################################################################

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/libapr-%{apr_version}.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/APRDesign.html docs/canonical_filenames.html
%doc docs/incomplete_types docs/non_apr_programs
%doc html
%{_bindir}/apr*config
%{_libdir}/libapr-%{apr_version}.*a
%{_libdir}/libapr-%{apr_version}.so
%dir %{_libdir}/apr
%dir %{_libdir}/apr/build-%{apr_version}
%{_libdir}/apr/build-%{apr_version}/*
%{_libdir}/pkgconfig/apr-%{apr_version}.pc
%dir %{_includedir}/apr-%{apr_version}
%{_includedir}/apr-%{apr_version}/*.h

###############################################################################

%changelog
* Sat Apr 09 2016 Gleb Goncharov <yum@gongled.ru> 1.5.2-0
- Initial build 

