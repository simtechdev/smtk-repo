# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary: Powerful interactive shell
Name: zsh
Version: 5.0.2
Release: 3%{?dist}
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
Source0: http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRequires: coreutils sed ncurses-devel libcap-devel
BuildRequires: texinfo tetex texi2html gawk /bin/hostname
Requires(post): /sbin/install-info grep
Requires(preun): /sbin/install-info
Requires(postun): coreutils grep

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format
Group: System Environment/Shells

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep

%setup -q

%build
%define _bindir /bin
# Avoid stripping...
export LDFLAGS=""
%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp  --enable-maildir-support

make all html

%check
# Run the testsuite
# the completion tests hang on s390 and s390x
  ( cd Test
    mkdir skipped
%ifarch s390 s390x ppc ppc64
    mv Y*.ztst skipped
%endif
%ifarch s390 s390x ppc64
    # FIXME: This is a real failure, Debian apparently just don't test.
    # RHBZ: 460043
    mv D02glob.ztst skipped
%endif
    # FIXME: This hangs in mock
    # Running test: Test loading of all compiled modules
    mv V01zmodload.ztst skipped
    true )
  ZTST_verbose=1 make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall install.info \
  fndir=$RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions \
  sitefndir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions \
  scriptdir=$RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/scripts \
  sitescriptdir=$RPM_BUILD_ROOT%{_datadir}/zsh/scripts

rm -f ${RPM_BUILD_ROOT}%{_bindir}/zsh-%{version}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/skel

# This is just here to shut up rpmlint, and is very annoying.
# Note that we can't chmod everything as then rpmlint will complain about
# those without a she-bang line.
for i in checkmail harden run-help zcalc zkbd; do
    sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
      ${RPM_BUILD_ROOT}%{_datadir}/zsh/*/functions/$i
    chmod +x ${RPM_BUILD_ROOT}%{_datadir}/zsh/*/functions/$i
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/zsh" > %{_sysconfdir}/shells
else
    grep -q "^%{_bindir}/zsh$" %{_sysconfdir}/shells || echo "%{_bindir}/zsh" >> %{_sysconfdir}/shells
fi

if [ -f %{_infodir}/zsh.info.gz ]; then
# This is needed so that --excludedocs works.
/sbin/install-info %{_infodir}/zsh.info.gz %{_infodir}/dir \
  --entry="* zsh: (zsh).      An enhanced bourne shell."
fi

:

%preun
if [ "$1" = 0 ] ; then
    if [ -f %{_infodir}/zsh.info.gz ]; then
    # This is needed so that --excludedocs works.
    /sbin/install-info --delete %{_infodir}/zsh.info.gz %{_infodir}/dir \
      --entry="* zsh: (zsh).      An enhanced bourne shell."
    fi
fi
:

%postun
if [ "$1" = 0 ] ; then
    if [ -f %{_sysconfdir}/shells ] ; then
        TmpFile=`%{_bindir}/mktemp /tmp/.zshrpmXXXXXX`
        grep -v '^%{_bindir}/zsh$' %{_sysconfdir}/shells > $TmpFile
        cp -f $TmpFile %{_sysconfdir}/shells
        rm -f $TmpFile
    fi
fi

%files
%defattr(-,root,root)
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide zshprompt.pl
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/zsh
%{_libdir}/zsh
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
* Mon Apr 15 2013 James Antill <james@fedoraproject.org> - 5.0.2-3
- Fix the changelog dates.
- Fix the texi itemx bug.
- Resolves: bug#927863

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-1
- Update to new upstream version: Zsh 5.0.2

* Wed Nov 21 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.0-1
- Update to new upstream version: Zsh 5.0.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 04 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.17-1
- Update to new upstream version: Zsh 4.3.17

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.15-1
- Update to new upstream version: Zsh 4.3.15

* Sat Dec 17 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.14-2
- change the License field to MIT (RHBZ#768548)

* Sat Dec 10 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.14-1
- Update to new upstream version: Zsh 4.3.14

* Sat Dec 03 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.13-1
- Update to new upstream version: Zsh 4.3.13

* Sat Aug 13 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.12-1
- Update to new upstream version: Zsh 4.3.12

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Christopher Ailon <caillon@redhat.com> - 4.3.11-1
- Rebase to upstream version 4.3.11

* Tue Dec 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 4.3.10-6
- Rebuild for FTBFS https://bugzilla.redhat.com/show_bug.cgi?id=631197
- Remove deprecated PreReq, the packages aren't needed at runtime and they're
  already in Requires(post,preun,etc): lines.

* Mon Mar 22 2010 James Antill <james@fedoraproject.org> - 4.3.10-5
- Add pathmunge to our /etc/zshrc, for profile.d compat.
- Resolves: bug#548960

* Fri Aug  7 2009 James Antill <james@fedoraproject.org> - 4.3.10-4
- Allow --excludedocs command to work!
- Resolves: bug#515986

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 James Antill <james@fedoraproject.org> - 4.3.10-1
- Import new upstream 4.3.10

* Wed Jun 10 2009 Karsten Hopp <karsten@redhat.com> 4.3.9-4.1
- skip D02glob test on s390, too

* Mon Mar  2 2009 James Antill <james@fedoraproject.org> - 4.3.9-4
- Remove D02glob testcase on ppc/ppc64, and hope noone cares

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
