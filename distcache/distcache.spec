
Summary: Distributed SSL session cache
Name: distcache
Version: 1.4.5
Release: 23
License: LGPLv2
Group: System Environment/Daemons
URL: http://www.distcache.org/
Source0: http://downloads.sourceforge.net/distcache/%{name}-%{version}.tar.bz2
Patch0: distcache-1.4.5-setuid.patch
Patch1: distcache-1.4.5-libdeps.patch
Patch2: distcache-1.4.5-limits.patch
Source1: dc_server.init
Source2: dc_client.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake >= 1.7, autoconf >= 2.50, libtool, openssl-devel
Requires(post): /sbin/chkconfig, /sbin/ldconfig, shadow-utils
Requires(preun): /sbin/service, /sbin/chkconfig

%description
The distcache package provides a variety of functionality for
enabling a network-based session caching system, primarily for
(though not restricted to) SSL/TLS session caching.

%package devel
Group: Development/Libraries
Summary: Development tools for distcache distributed session cache
Requires: distcache = %{version}-%{release}

%description devel
This package includes the libraries that implement the necessary
network functionality, the session caching protocol, and APIs for
applications wishing to use a distributed session cache, or indeed
even to implement a storage mechanism for a session cache server.

%prep
%setup -q
%patch0 -p1 -b .setuid
%patch1 -p1 -b .libdeps
%patch2 -p1 -b .limits

%build
libtoolize --force --copy && aclocal && autoconf
automake -aic --gnu || : automake ate my hamster
pushd ssl
autoreconf -i || : let it fail too
popd
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make -C ssl install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -p -m 755 $RPM_SOURCE_DIR/dc_server.init \
        $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dc_server
install -p -m 755 $RPM_SOURCE_DIR/dc_client.init \
        $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dc_client

mkdir -p $RPM_BUILD_ROOT%{_sbindir}

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/{nal_test,piper} \
      $RPM_BUILD_ROOT%{_libdir}/lib*.la

%post
/sbin/chkconfig --add dc_server
/sbin/chkconfig --add dc_client
/sbin/ldconfig
# Add the "distcache" user
/usr/sbin/useradd -c "Distcache" -u 94 \
        -s /sbin/nologin -r -d / distcache 2> /dev/null || :

%preun
if [ $1 = 0 ]; then
    /sbin/service dc_server stop > /dev/null 2>&1
    /sbin/service dc_client stop > /dev/null 2>&1
    /sbin/chkconfig --del dc_server
    /sbin/chkconfig --del dc_client
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/sslswamp
%{_bindir}/dc_*
%{_sysconfdir}/rc.d/init.d/dc_*
%doc ANNOUNCE CHANGES README LICENSE FAQ
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/swamp

%files devel
%defattr(-,root,root,-)
%{_includedir}/distcache
%{_includedir}/libnal
%{_libdir}/*.so
%{_mandir}/man2/*

%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.5-21
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> 1.4.5-18
- rebuild with new openssl
- have to run autoreconf in the ssl subdir due to new libtool

* Wed Feb 13 2008 Joe Orton <jorton@redhat.com> 1.4.5-17
- fix libnal build

* Wed Dec  5 2007 Joe Orton <jorton@redhat.com> 1.4.5-16
- rebuild for new OpenSSL

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 1.4.5-15
- fix License, BuildRoot, Source0, drop .la files, detabify

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.5-14.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.4.5-14
- rebuild for -devel deps

* Thu Mar  2 2006 Joe Orton <jorton@redhat.com> 1.4.5-13
- avoid uid collision with exim (#182091)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.5-12.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.5-12.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 1.4.5-12
- rebuilt with new openssl

* Fri Jul 29 2005 Joe Orton <jorton@redhat.com> 1.4.5-11
- add distcache user in post script, uid 93
- run daemons as distcache user rather than nobody

* Thu Jul 28 2005 Joe Orton <jorton@redhat.com> 1.4.5-10
- fix broken deps

* Tue Jul 26 2005 Joe Orton <jorton@redhat.com> 1.4.5-9
- add epoch and release to devel->main dependency
- don't build static libraries

* Fri May  6 2005 Joe Orton <jorton@redhat.com> 1.4.5-8
- make libdistcache{,server} depend on libnal
- add scriplet requirements

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 1.4.5-7
- rebuild with openssl-0.9.7e

* Tue Aug 31 2004 Joe Orton <jorton@redhat.com> 1.4.5-6
- move ldconfig from preun to postun (#131289)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 17 2004 Joe Orton <jorton@redhat.com> 1.4.5-4
- run ldconfig in %%post and %%postun

* Sun May  2 2004 Joe Orton <jorton@redhat.com> 1.4.5-3
- add BuildRequires: openssl-devel (#122265)

* Tue Apr 13 2004 Joe Orton <jorton@redhat.com> 1.4.5-2
- dc_client: go setuid later (#120711)

* Tue Apr  6 2004 Joe Orton <jorton@redhat.com> 1.4.5-1
- update to 1.4.5 (#119135)
- include sslswamp
- build shared libraries

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- mv /etc/init.d -> /etc/rc.d/init.d

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 25 2004 Joe Orton <jorton@redhat.com> 0.4.2-9
- add BuildRequires (#114115)
- add config lines to init scripts

* Tue Jan 20 2004 Joe Orton <jorton@redhat.com> 0.4.2-8
- rebuild

* Fri Nov 28 2003 Joe Orton <jorton@redhat.com> 0.4.2-7
- sync with upstream: use -sock{owner,perms} in dc_client

* Wed Nov 26 2003 Joe Orton <jorton@redhat.com> 0.4.2-6
- set socket owner and permissions in dc_client

* Wed Nov 26 2003 Joe Orton <jorton@redhat.com> 0.4.2-5
- rebuild in new environment

* Tue Nov 18 2003 Joe Orton <jorton@redhat.com> 0.4.2-4
- fix %%preun to allow --erase to succeed (#110115)

* Thu Jul 31 2003 Joe Orton <jorton@redhat.com> 0.4.2-3
- add dc_client init script
- pass -sessions to dc_server

* Wed Jul  2 2003 Joe Orton <jorton@redhat.com> 0.4.2-2
- have dc_server drop to 'nobody' user after bind()
- add init script for dc_server
- build everything using -fPIC

* Mon Jun  9 2003 Joe Orton <jorton@redhat.com> 0.4.2-1
- Initial build.

