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

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global pkgname	phpMyAdmin

# If php-mcrypt is available, it should be preferred. Otherwise the pure
# phpseclib alternative alternative can be used externally or internally.
%global mcrypt	1
%global seclib	0

# Having below mentioned separate projects externally or only internally?
%global gettext	1
%global tcpdf	1

################################################################################

Summary:        Handle the administration of MySQL over the World Wide Web
Name:           phpMyAdmin
Version:        4.5.5
Release:        0%{?dist}
License:        GPLv2+
Group:          Applications/Internet
URL:            http://www.phpmyadmin.net/

Source0:        https://files.phpmyadmin.net/%{pkgname}/%{version}/%{pkgname}-%{version}-all-languages.tar.gz
Source1:        phpMyAdmin-config.inc.php
Source2:        phpMyAdmin.htaccess

%if 0%{?rhel} != 5
Requires:       php(language) >= 5.2.17, php-filter, php-xmlwriter
%else
Requires:       php(api) >= 20090626, php-xml >= 5.2.0
%endif

Requires:       php-bz2, php-ctype, php-curl, php-date, php-gd >= 5.2.0, php-hash, php-iconv
Requires:       php-json, php-libxml, php-mbstring >= 5.2.0, php-mysql >= 5.2.0, php-mysqli, php-pcre
Requires:       php-session, php-simplexml, php-spl, php-zip, php-zlib

%if 0%{?mcrypt}
Requires:       php-mcrypt >= 5.2.0
%else
%if 0%{?seclib}
Requires:       php-phpseclib-crypt-aes
%endif
%endif

%if 0%{?gettext}
Requires:       php-php-gettext
%endif

%if 0%{?tcpdf}
Requires:       php-tcpdf, php-tcpdf-dejavu-sans-fonts
%endif
%if 0%{?rhel} == 5

Provides:       phpMyAdmin = %{version}-%{release}, phpMyAdmin3 = %{version}-%{release}
Obsoletes:      phpMyAdmin3 < %{version}-%{release}
%endif

Provides:       phpmyadmin = %{version}-%{release}

BuildArch:      noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

################################################################################

%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the World Wide Web. Most frequently used operations are supported
by the user interface (managing databases, tables, fields, relations, indexes,
users, permissions), while you still have the ability to directly execute any
SQL statement.

Features include an intuitive web interface, support for most MySQL features
(browse and drop databases, tables, views, fields and indexes, create, copy,
drop, rename and alter databases, tables, fields and indexes, maintenance
server, databases and tables, with proposals on server configuration, execute,
edit and bookmark any SQL-statement, even batch-queries, manage MySQL users
and privileges, manage stored procedures and triggers), import data from CSV
and SQL, export data to various formats: CSV, SQL, XML, PDF, OpenDocument Text
and Spreadsheet, Word, Excel, LATEX and others, administering multiple servers,
creating PDF graphics of your database layout, creating complex queries using
Query-by-example (QBE), searching globally in a database or a subset of it,
transforming stored data into any format using a set of predefined functions,
like displaying BLOB-data as image or download-link and much more...

################################################################################

%prep
%setup -qn %{pkgname}-%{version}-all-languages

sed -e "/'CHANGELOG_FILE'/s@./ChangeLog@%{_pkgdocdir}/ChangeLog@" \
    -e "/'LICENSE_FILE'/s@./LICENSE@%{_pkgdocdir}/LICENSE@" \
    -e "/'CONFIG_DIR'/s@'./'@'%{_sysconfdir}/%{pkgname}/'@" \
    -e "/'SETUP_CONFIG_FILE'/s@./config/config.inc.php@%{_localstatedir}/lib/%{pkgname}/config/config.inc.php@" \
%if 0%{?gettext}
    -e "/'GETTEXT_INC'/s@./libraries/php-gettext/gettext.inc@%{_datadir}/php/gettext/gettext.inc@" \
%endif
%if 0%{?tcpdf}
    -e "/'TCPDF_INC'/s@./libraries/tcpdf/tcpdf.php@%{_datadir}/php/tcpdf/tcpdf.php@" \
%endif
%if 0%{?mcrypt}%{?seclib}
    -e "/'PHPSECLIB_INC_DIR'/s@./libraries/phpseclib@%{_datadir}/pear@" \
%endif
    -i libraries/vendor_config.php

%if 0%{?gettext}
rm -rf libraries/php-gettext/
%endif

%if 0%{?tcpdf}
rm -rf libraries/tcpdf/
%endif

%if 0%{?mcrypt}%{?seclib}
rm -rf libraries/phpseclib/
%endif

rm -rf js/jquery/src/
rm -f js/canvg/flashcanvas.{js,swf}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_datadir}/%{pkgname},%{_sysconfdir}/{httpd/conf.d,%{pkgname}}}/
mkdir -p %{buildroot}%{_localstatedir}/lib/%{pkgname}/{upload,save,config}/
cp -ad * %{buildroot}%{_datadir}/%{pkgname}/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{pkgname}/config.inc.php

rm -f %{buildroot}%{_datadir}/%{pkgname}/{[CDLR]*,*.txt,config.sample.inc.php}
rm -rf %{buildroot}%{_datadir}/%{pkgname}/{doc,examples}/
rm -f doc/html/.buildinfo

mkdir -p %{buildroot}%{_datadir}/%{pkgname}/{doc,examples}/
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/%{pkgname}/examples/

ln -s ../../../..%{_pkgdocdir}/html/ %{buildroot}%{_datadir}/%{pkgname}/doc/html
mv -f config.sample.inc.php examples/

%clean
rm -rf %{buildroot}

%post
sed -e "/'blowfish_secret'/s/MUSTBECHANGEDONINSTALL/$RANDOM$RANDOM$RANDOM$RANDOM/" \
    -i %{_sysconfdir}/%{pkgname}/config.inc.php

################################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog README LICENSE doc/html/ examples/
%{_datadir}/%{pkgname}/
%dir %attr(0755,root,root) %{_sysconfdir}/%{pkgname}/
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/%{pkgname}/config.inc.php
%dir %{_localstatedir}/lib/%{pkgname}/
%dir %attr(0755,root,root) %{_localstatedir}/lib/%{pkgname}/upload/
%dir %attr(0755,root,root) %{_localstatedir}/lib/%{pkgname}/save/
%dir %attr(0755,root,root) %{_localstatedir}/lib/%{pkgname}/config/

################################################################################

%changelog
* Tue Feb 23 2016 Gleb Goncharov <yum@gongled.ru> 4.5.5-0
- Upgrade to 4.5.5

* Sun Feb 07 2016 Gleb Goncharov <yum@gongled.ru> 4.5.4.1-0
- Upgrade to 4.5.4.1

* Wed Dec 30 2015 Gleb Goncharov <yum@gongled.ru> 4.5.3.1-0
- Upgrade to 4.5.3.1

* Sun Aug 02 2015 Gleb Goncharov <yum@gongled.ru> 4.4.12-1
- Minor fixes.

* Sun Aug 02 2015 Gleb Goncharov <yum@gongled.ru> 4.4.12-0
- Upgrade to 4.4.12.0

* Thu May 14 2015 Robert Scheck <robert@fedoraproject.org> 4.0.10.10-1
- Upgrade to 4.0.10.10 (#1221588, #1221580, #1221581)

* Wed Mar 04 2015 Robert Scheck <robert@fedoraproject.org> 4.0.10.9-1
- Upgrade to 4.0.10.9

* Wed Jan 07 2015 Robert Scheck <robert@fedoraproject.org> 4.0.10.8-1
- Upgrade to 4.0.10.8

* Thu Dec 11 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.7-2
- Use %%{pkgname} rather %%{name} in %%post scriptlet (#1173189)

* Thu Dec 04 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.7-1
- Upgrade to 4.0.10.7

* Thu Nov 20 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.6-1
- Upgrade to 4.0.10.6

* Wed Oct 22 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.5-1
- Upgrade to 4.0.10.5 (#1155362)

* Thu Oct 02 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.4-1
- Upgrade to 4.0.10.4 (#1148664)

* Wed Sep 17 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.3-2
- Move rm(1) calls from %%install to %%prep (#1121355 #c10)

* Tue Sep 16 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.3-1
- Upgrade to 4.0.10.3 (#1141635)

* Mon Sep 01 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.2-2
- Corrected wrong permissions of /etc/phpMyAdmin/ directory

* Mon Aug 18 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.2-1
- Upgrade to 4.0.10.2 (#1130865)

* Tue Jul 22 2014 Robert Scheck <robert@fedoraproject.org> 4.0.10.1-1
- Upgrade to 4.0.10.1 (#548260, #959946, #989660, #989668, #993613
  and #1000261, #1067713, #1110877, #1117600, #1117601)
- Switch from HTTP- to cookie-based authentication (for php-fpm)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.5.8.2-2
- Fix paths to changelog and license when doc dir is unversioned (#994036).
- Fix source URL, use xz compressed tarball.

* Wed Oct 09 2013 Paul Wouters <pwouters@redhat.com> - 3.5.8.2-1
- Upgrade to 3.5.8.2 (Various security issues)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Robert Scheck <robert@fedoraproject.org> 3.5.8.1-1
- Upgrade to 3.5.8.1 (#956398, #956401)

* Sat Apr 13 2013 Robert Scheck <robert@fedoraproject.org> 3.5.8-1
- Upgrade to 3.5.8 (#949868)

* Sat Feb 23 2013 Robert Scheck <robert@fedoraproject.org> 3.5.7-1
- Upgrade to 3.5.7 (#912097)

* Sun Feb 10 2013 Robert Scheck <robert@fedoraproject.org> 3.5.6-1
- Upgrade to 3.5.6 (#889450)

* Sun Nov 18 2012 Robert Scheck <robert@fedoraproject.org> 3.5.4-1
- Upgrade to 3.5.4 (#877727)

* Tue Oct 09 2012 Robert Scheck <robert@fedoraproject.org> 3.5.3-1
- Upgrade to 3.5.3

* Wed Aug 15 2012 Robert Scheck <robert@fedoraproject.org> 3.5.2.2-1
- Upgrade to 3.5.2.2 (#845736)

* Sat Aug 11 2012 Robert Scheck <robert@fedoraproject.org> 3.5.2.1-1
- Upgrade to 3.5.2.1 (#845736)

* Mon Jul 30 2012 Robert Scheck <robert@fedoraproject.org> 3.5.2-1
- Upgrade to 3.5.2 (#838310)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Robert Scheck <robert@fedoraproject.org> 3.5.1-1
- Upgrade to 3.5.1 (#819171)

* Sat May 05 2012 Remi Collet <remi@fedoraproject.org> 3.5.0-2
- make configuration compatible apache 2.2 / 2.4

* Sun Apr 08 2012 Robert Scheck <robert@fedoraproject.org> 3.5.0-1
- Upgrade to 3.5.0 (#790782, #795020, #809146)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Robert Scheck <robert@fedoraproject.org> 3.4.9-1
- Upgrade to 3.4.9 (#769818)

* Sun Dec 04 2011 Robert Scheck <robert@fedoraproject.org> 3.4.8-1
- Upgrade to 3.4.8 (#759441)

* Sat Nov 12 2011 Robert Scheck <robert@fedoraproject.org> 3.4.7.1-1
- Upgrade to 3.4.7.1 (#753119)

* Sat Nov 05 2011 Robert Scheck <robert@fedoraproject.org> 3.4.7-1
- Upgrade to 3.4.7 (#746630, #746880)

* Sun Sep 18 2011 Robert Scheck <robert@fedoraproject.org> 3.4.5-1
- Upgrade to 3.4.5 (#733638, #738681, #629214)

* Thu Aug 25 2011 Robert Scheck <robert@fedoraproject.org> 3.4.4-1
- Upgrade to 3.4.4 (#733475, #733477, #733480)

* Tue Jul 26 2011 Robert Scheck <robert@fedoraproject.org> 3.4.3.2-2
- Disabled the warning for missing internal database relation
- Reworked spec file to build phpMyAdmin3 for RHEL 5 (#725885)

* Mon Jul 25 2011 Robert Scheck <robert@fedoraproject.org> 3.4.3.2-1
- Upgrade to 3.4.3.2 (#725377, #725381, #725382, #725383, #725384)

* Wed Jul 06 2011 Robert Scheck <robert@fedoraproject.org> 3.4.3.1-1
- Upgrade to 3.4.3.1 (#718964)

* Mon Jun 13 2011 Robert Scheck <robert@fedoraproject.org> 3.4.2-1
- Upgrade to 3.4.2 (#711743)

* Sun May 29 2011 Robert Scheck <robert@fedoraproject.org> 3.4.1-1
- Upgrade to 3.4.1 (#704171)

* Mon Mar 21 2011 Robert Scheck <robert@fedoraproject.org> 3.3.10-1
- Upstream released 3.3.10 (#661335, #662366, #662367, #689213)

* Sun Feb 13 2011 Robert Scheck <robert@fedoraproject.org> 3.3.9.2-1
- Upstream released 3.3.9.2 (#676172)

* Thu Feb 10 2011 Robert Scheck <robert@fedoraproject.org> 3.3.9.1-1
- Upstream released 3.3.9.1 (#676172)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Robert Scheck <robert@fedoraproject.org> 3.3.9-1
- Upstream released 3.3.9 (#666925)

* Mon Nov 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.8.1-1
- Upstream released 3.3.8.1

* Fri Oct 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.8-1
- Upstream released 3.3.8 (#631748)

* Wed Sep 08 2010 Robert Scheck <robert@fedoraproject.org> 3.3.7-1
- Upstream released 3.3.7 (#631824, #631829)

* Sun Aug 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.6-1
- Upstream released 3.3.6 (#628301)

* Fri Aug 20 2010 Robert Scheck <robert@fedoraproject.org> 3.3.5.1-1
- Upstream released 3.3.5.1 (#625877, #625878)
- Added patch to fix wrong variable check at nopassword (#622428)

* Tue Jul 27 2010 Robert Scheck <robert@fedoraproject.org> 3.3.5-1
- Upstream released 3.3.5 (#618586)

* Tue Jun 29 2010 Robert Scheck <robert@fedoraproject.org> 3.3.4-1
- Upstream released 3.3.4 (#609057)

* Sat Jun 26 2010 Robert Scheck <robert@fedoraproject.org> 3.3.3-1
- Upstream released 3.3.3 (#558322, #589288, #589487)

* Sun Jan 10 2010 Robert Scheck <robert@fedoraproject.org> 3.2.5-1
- Upstream released 3.2.5

* Thu Dec 03 2009 Robert Scheck <robert@fedoraproject.org> 3.2.4-1
- Upstream released 3.2.4 (#540871, #540891)

* Thu Nov 05 2009 Robert Scheck <robert@fedoraproject.org> 3.2.3-1
- Upstream released 3.2.3

* Tue Oct 13 2009 Robert Scheck <robert@fedoraproject.org> 3.2.2.1-1
- Upstream released 3.2.2.1 (#528769)
- Require php-mcrypt for cookie authentication (#526979)

* Sun Sep 13 2009 Robert Scheck <robert@fedoraproject.org> 3.2.2-1
- Upstream released 3.2.2

* Sun Sep 06 2009 Robert Scheck <robert@fedoraproject.org> 3.2.1-2
- Added ::1 for localhost/loopback access (for IPv6 users)

* Mon Aug 10 2009 Robert Scheck <robert@fedoraproject.org> 3.2.1-1
- Upstream released 3.2.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Robert Scheck <robert@fedoraproject.org> 3.2.0.1-1
- Upstream released 3.2.0.1 (#508879)

* Tue Jun 30 2009 Robert Scheck <robert@fedoraproject.org> 3.2.0-1
- Upstream released 3.2.0

* Fri May 15 2009 Robert Scheck <robert@fedoraproject.org> 3.1.5-1
- Upstream released 3.1.5

* Sat Apr 25 2009 Robert Scheck <robert@fedoraproject.org> 3.1.4-1
- Upstream released 3.1.4

* Tue Apr 14 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3.2-1
- Upstream released 3.1.3.2 (#495768)

* Wed Mar 25 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3.1-1
- Upstream released 3.1.3.1 (#492066)

* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3-1
- Upstream released 3.1.3

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 3.1.2-2
- Rebuilt against rpm 4.6

* Tue Jan 20 2009 Robert Scheck <robert@fedoraproject.org> 3.1.2-1
- Upstream released 3.1.2

* Thu Dec 11 2008 Robert Scheck <robert@fedoraproject.org> 3.1.1-1
- Upstream released 3.1.1 (#475954)

* Sat Nov 29 2008 Robert Scheck <robert@fedoraproject.org> 3.1.0-1
- Upstream released 3.1.0
- Replaced LocationMatch with Directory directive (#469451)

* Thu Oct 30 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1.1-1
- Upstream released 3.0.1.1 (#468974)

* Wed Oct 22 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1-1
- Upstream released 3.0.1

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-1
- Upstream released 3.0.0

* Mon Sep 22 2008 Robert Scheck <robert@fedoraproject.org> 2.11.9.2-1
- Upstream released 2.11.9.2 (#463260)

* Tue Sep 16 2008 Robert Scheck <robert@fedoraproject.org> 2.11.9.1-1
- Upstream released 2.11.9.1 (#462430)

* Fri Aug 29 2008 Robert Scheck <robert@fedoraproject.org> 2.11.9-1
- Upstream released 2.11.9

* Mon Jul 28 2008 Robert Scheck <robert@fedoraproject.org> 2.11.8.1-1
- Upstream released 2.11.8.1 (#456637, #456950)

* Mon Jul 28 2008 Robert Scheck <robert@fedoraproject.org> 2.11.8-1
- Upstream released 2.11.8 (#456637)

* Tue Jul 15 2008 Robert Scheck <robert@fedoraproject.org> 2.11.7.1-1
- Upstream released 2.11.7.1 (#455520)

* Mon Jun 23 2008 Robert Scheck <robert@fedoraproject.org> 2.11.7-1
- Upstream released 2.11.7 (#452497)

* Tue Apr 29 2008 Robert Scheck <robert@fedoraproject.org> 2.11.6-1
- Upstream released 2.11.6

* Tue Apr 22 2008 Robert Scheck <robert@fedoraproject.org> 2.11.5.2-1
- Upstream released 2.11.5.2 (#443683)

* Sat Mar 29 2008 Robert Scheck <robert@fedoraproject.org> 2.11.5.1-1
- Upstream released 2.11.5.1

* Mon Mar 03 2008 Robert Scheck <robert@fedoraproject.org> 2.11.5-1
- Upstream released 2.11.5

* Sun Jan 13 2008 Robert Scheck <robert@fedoraproject.org> 2.11.4-1
- Upstream released 2.11.4
- Corrected mod_security example in configuration file (#427119)

* Sun Dec 09 2007 Robert Scheck <robert@fedoraproject.org> 2.11.3-1
- Upstream released 2.11.3
- Removed the RPM scriptlets doing httpd restarts (#227025)
- Patched an information disclosure known as CVE-2007-0095 (#221694)
- Provide virtual phpmyadmin package and a httpd alias (#231431)

* Wed Nov 21 2007 Robert Scheck <robert@fedoraproject.org> 2.11.2.2-1
- Upstream released 2.11.2.2 (#393771)

* Tue Nov 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.2.1-1
- Upstream released new version

* Mon Oct 29 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.2-1
* upstream released new version

* Mon Oct 22 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.1.2-1
* upstream released new version

* Thu Sep 06 2007 Mike McGrath <mmcgrath@redhat.com> 2.11.0-1
- Upstream released new version
- Altered sources file as required
- Added proper license

* Mon Jul 23 2007 Mike McGrath <mmcgrath@redhat.com> 2.10.3-1
- Upstream released new version

* Sat Mar 10 2007 Mike McGrath <mmcgrath@redhat.com> 2.10.0.2-3
- Switched to the actual all-languages, not just utf-8

* Sun Mar 04 2007 Mike McGrath <mmcgrath@redhat.com> 2.10.0.2-1
- Upstream released new version

* Sat Jan 20 2007 Mike McGrath <imlinux@gmail.com> 2.9.2-1
- Upstream released new version

* Fri Dec 08 2006 Mike McGrath <imlinux@gmail.com> 2.9.1.1-2
- Fixed bug in spec file

* Fri Dec 08 2006 Mike McGrath <imlinux@gmail.com> 2.9.1.1-1
- Upstream released new version

* Wed Nov 15 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-3alpha
- Added dist tag

* Wed Nov 15 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-2alpha
- Fixed 215159

* Fri Nov 10 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-1alpha
- Added alpha tag since this is a release candidate

* Tue Nov 07 2006 Mike McGrath <imlinux@gmail.com> 2.9.1-1
- Upstream released new version

* Wed Oct 04 2006 Mike McGrath <imlinux@gmail.com> 2.9.0.2-1
- Upstream released new version

* Thu Jul 06 2006 Mike McGrath <imlinux@gmail.com> 2.8.2-2
- Fixed a typo in the Apache config

* Mon Jul 03 2006 Mike McGrath <imlinux@gmail.com> 2.8.2-1
- Upstream released 2.8.2
- Added more restrictive directives to httpd/conf.d/phpMyAdmin.conf
- removed htaccess file from the libraries dir
- Specific versions for various requires

* Sat May 13 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.4-1
- Upstream released 2.8.0.4
- Added requires php, instead of requires httpd, now using webserver

* Sun May 07 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.3-2
- Added mysql-php and php-mbstring as a requires

* Fri Apr 07 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.3-1
- Fixed XSS vulnerability: PMASA-2006-1
- It was possible to conduct an XSS attack with a direct call to some scripts
- under the themes directory.

* Tue Apr 04 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.2-3
- Made config files actually configs
- Moved doc files to the doc dir

* Tue Apr 04 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.2-2
- Moved everything to %{_datadir}
- Moved config file to /etc/
- Used description from phpMyAdmin project info

* Mon Apr 03 2006 Mike McGrath <imlinux@gmail.com> 2.8.0.2-1
- Initial Spec file creation for Fedora
