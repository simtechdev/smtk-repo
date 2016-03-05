%define contentdir /var/www
%define suexec_caller apache
%define mmn 20051115
%define mpms worker event

Summary: Apache HTTP Server
Name: httpd
Version: 2.2.31
Release: 1
URL: http://httpd.apache.org/
Vendor: Apache Software Foundation
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.gz
License: Apache License, Version 2.0
Group: System Environment/Daemons

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: apr-devel, apr-util-devel, openldap-devel, db4-devel, expat-devel, findutils, perl, pkgconfig, pcre-devel >= 5.0
BuildRequires: /usr/bin/apr-1-config, /usr/bin/apu-1-config

Requires: apr >= 1.4.2, apr-util >= 1.3.10, pcre >= 5.0, gawk, /usr/bin/find, openldap

Requires(post): /sbin/chkconfig, /bin/mktemp, /bin/rm, /bin/mv
Requires(post): sh-utils, textutils, /usr/sbin/useradd

Provides: httpd-mmn = %{mmn}

Conflicts: thttpd

Obsoletes: apache = %{version}-%{release}
Obsoletes: secureweb = %{version}-%{release}
Obsoletes: mod_dav = %{version}-%{release}

%description
Apache is a powerful, full-featured, efficient, and freely-available
Web server. Apache is also the most popular Web server on the
Internet.

%package devel
Group: Development/Libraries
Summary: Development tools for the Apache HTTP server.
Obsoletes: secureweb-devel = %{version}-%{release}
Obsoletes: apache-devel = %{version}-%{release}
Requires: libtool, httpd = %{version}
Requires: apr-devel >= 1.4.2, apr-util-devel >= 1.3.10

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for Apache.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server.
Obsoletes: secureweb-manual = %{version}-%{release}
Obsoletes: apache-manual = %{version}-%{release}

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/.

%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP server
Requires: openssl-devel
Requires: httpd, make, httpd-mmn = %{mmn}
Requires(post): openssl, dev, /bin/cat

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%prep
%setup -q

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '
/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}.
   : Update the mmn macro and rebuild.
   exit 1
fi

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
	support/apxs.in

function mpmbuild()
{
mpm=$1; shift
mkdir $mpm; pushd $mpm
../configure \
	--prefix=%{_sysconfdir}/httpd \
	--with-apr=/usr/bin/apr-1-config \
	--with-apr-util=/usr/bin/apu-1-config \
	--with-pcre=/usr/bin/pcre-config \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir}/httpd/conf \
	--includedir=%{_includedir}/httpd \
	--libexecdir=%{_libdir}/httpd/modules \
	--datadir=%{contentdir} \
	--with-installbuilddir=%{_libdir}/httpd/build \
	--with-mpm=$mpm \
	--enable-suexec --with-suexec \
	--with-suexec-caller=%{suexec_caller} \
	--with-suexec-docroot=%{contentdir} \
	--with-suexec-logfile=%{_localstatedir}/log/httpd/suexec.log \
	--with-suexec-bin=%{_sbindir}/suexec \
	--with-suexec-uidmin=500 --with-suexec-gidmin=500 \
	--enable-pie \
	--with-pcre \
	$*

make %{?_smp_mflags}
popd
}

 # Build everything and the kitchen sink with the prefork build
mpmbuild prefork \
	--enable-mods-shared=all \
	--enable-ssl --with-ssl --enable-distcache \
	--enable-proxy \
	--enable-cache \
	--enable-disk-cache \
	--enable-ldap --enable-authnz-ldap \
	--enable-cgid \
	--enable-authn-anon --enable-authn-alias \
	--disable-imagemap

# For the other MPMs, just build httpd and no optional modules
for f in %{mpms}; do
   mpmbuild $f --enable-mods-shared=all
done

%install
rm -rf %{buildroot}

pushd prefork
make DESTDIR=%{buildroot} install
popd

# install alternative MPMs
for f in %{mpms}; do
  install -m 755 ${f}/httpd %{buildroot}%{_sbindir}/httpd.${f}
done

# for holding mod_dav lock database
mkdir -p %{buildroot}%{_localstatedir}/lib/dav

# create a prototype session cache
mkdir -p %{buildroot}%{_localstatedir}/cache/mod_ssl
touch %{buildroot}%{_localstatedir}/cache/mod_ssl/scache.{dir,pag,sem}

# move the build directory to within the library directory
mv %{buildroot}%{contentdir}/build %{buildroot}%{_libdir}/httpd/build

# Make the MMN accessible to module packages
echo %{mmn} > %{buildroot}%{_includedir}/httpd/.mmn

# docroot
mkdir %{buildroot}%{contentdir}/html

# Set up /var directories
rmdir %{buildroot}%{_sysconfdir}/httpd/logs
mkdir -p %{buildroot}%{_localstatedir}/log/httpd
mkdir -p %{buildroot}%{_localstatedir}/cache/httpd/cache-root

# symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/httpd %{buildroot}/etc/httpd/logs
ln -s ../..%{_localstatedir}/run %{buildroot}/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules %{buildroot}/etc/httpd/modules

# install SYSV init stuff
mkdir -p %{buildroot}/etc/rc.d/init.d
install -m755 ./build/rpm/httpd.init \
	%{buildroot}/etc/rc.d/init.d/httpd
install -m755 ./build/rpm/htcacheclean.init \
	%{buildroot}/etc/rc.d/init.d/htcacheclean

# install log rotation stuff
mkdir -p %{buildroot}/etc/logrotate.d
install -m644 ./build/rpm/httpd.logrotate \
	%{buildroot}/etc/logrotate.d/httpd

# Remove unpackaged files
rm -rf %{buildroot}%{_libdir}/httpd/modules/*.exp \
	%{buildroot}%{contentdir}/htdocs/* \
	%{buildroot}%{contentdir}/cgi-bin/* 

# Make suexec a+rw so it can be stripped.  %%files lists real permissions
chmod 755 %{buildroot}%{_sbindir}/suexec

%pre
# Add the "apache" user
/usr/sbin/useradd -c "Apache" -u 48 \
	-s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%post
# Register the httpd service
/sbin/chkconfig --add httpd
/sbin/chkconfig --add htcacheclean

%preun
if [ $1 = 0 ]; then
	/sbin/service httpd stop > /dev/null 2>&1
	/sbin/service htcacheclean stop > /dev/null 2>&1
	/sbin/chkconfig --del httpd
	/sbin/chkconfig --del htcacheclean
fi

%post -n mod_ssl
umask 077

if [ ! -f %{_sysconfdir}/httpd/conf/server.key ] ; then
%{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 1024 > %{_sysconfdir}/httpd/conf/server.key 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

if [ ! -f %{_sysconfdir}/httpd/conf/server.crt ] ; then
cat << EOF | %{_bindir}/openssl req -new -key %{_sysconfdir}/httpd/conf/server.key -x509 -days 365 -out %{_sysconfdir}/httpd/conf/server.crt 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
fi

%check
# Check the built modules are all PIC
if readelf -d %{buildroot}%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

# Verify that the same modules were built into the httpd binaries
./prefork/httpd -l | grep -v prefork > prefork.mods
for mpm in %{mpms}; do
  ./${mpm}/httpd -l | grep -v ${mpm} > ${mpm}.mods
  if ! diff -u prefork.mods ${mpm}.mods; then
    : Different modules built into httpd binaries, will not proceed
    exit 1
  fi
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE NOTICE

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/httpd/conf/mime.types
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-manual.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-mpm.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-vhosts.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-manual.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-mpm.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-vhosts.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/httpd.conf

%config %{_sysconfdir}/logrotate.d/httpd
%config %{_sysconfdir}/rc.d/init.d/httpd
%config %{_sysconfdir}/rc.d/init.d/htcacheclean

%{_sbindir}/ab
%{_sbindir}/htcacheclean
%{_sbindir}/htdbm
%{_sbindir}/htdigest
%{_sbindir}/htpasswd
%{_sbindir}/logresolve
%{_sbindir}/httpd
%{_sbindir}/httpd.worker
%{_sbindir}/httpd.event
%{_sbindir}/httxt2dbm
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%attr(4510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
# everything but mod_ssl.so:
%{_libdir}/httpd/modules/mod_[a-r]*.so
%{_libdir}/httpd/modules/mod_s[petu]*.so
%{_libdir}/httpd/modules/mod_[t-z]*.so

%dir %{contentdir}
%dir %{contentdir}/cgi-bin
%dir %{contentdir}/html
%dir %{contentdir}/icons
%dir %{contentdir}/error
%dir %{contentdir}/error/include
%{contentdir}/icons/*
%{contentdir}/error/README
%config(noreplace) %{contentdir}/error/*.var
%config(noreplace) %{contentdir}/error/include/*.html

%attr(0700,root,root) %dir %{_localstatedir}/log/httpd

%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/cache-root

%{_mandir}/man1/*
%{_mandir}/man8/ab*
%{_mandir}/man8/rotatelogs*
%{_mandir}/man8/logresolve*
%{_mandir}/man8/suexec*
%{_mandir}/man8/apachectl.8*
%{_mandir}/man8/httpd.8*
%{_mandir}/man8/htcacheclean.8*

%files manual
%defattr(-,root,root)
%{contentdir}/manual
%{contentdir}/error/README

%files -n mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/mod_ssl
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.sem

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_sbindir}/apxs
%{_sbindir}/checkgid
%{_sbindir}/dbmmanage
%{_sbindir}/envvars*
%{_mandir}/man8/apxs.8*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/instdso.sh
%{_libdir}/httpd/build/config.nice
%{_libdir}/httpd/build/mkdir.sh

