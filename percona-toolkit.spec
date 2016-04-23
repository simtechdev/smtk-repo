###############################################################################

Summary:            Advanced MySQL and system command-line tools
Name:               percona-toolkit
Version:            2.2.17
Release:            0%{?dist}
Group:              Applications/Databases
License:            GPLv2
URL:                http://www.percona.com/software/percona-toolkit/

Source0:            https://github.com/percona/%{name}/archive/%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:          noarch

BuildRequires:      perl perl-ExtUtils-MakeMaker

Requires:           perl(DBI) >= 1.13 perl(DBD::mysql) >= 1.0 perl(Time::HiRes)
Requires:           perl(IO::Socket::SSL) perl(Digest::MD5) perl(Term::ReadKey)

AutoReq:            no

###############################################################################

%description
Percona Toolkit is a collection of advanced command-line tools used by
Percona (http://www.percona.com/) support staff to perform a variety of
MySQL and system tasks that are too difficult or complex to perform manually.

These tools are ideal alternatives to private or "one-off" scripts because
they are professionally developed, formally tested, and fully documented.
They are also fully self-contained, so installation is quick and easy and
no libraries are installed.

Percona Toolkit is developed and supported by Percona.  For more
information and other free, open-source software developed by Percona,
visit http://www.percona.com/software/.

###############################################################################

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
find %{buildroot} -type f -name 'percona-toolkit.pod' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING INSTALL README Changelog
%{_bindir}/*
%{_datadir}/perl5/*
%{_mandir}/man1/*.1*

###############################################################################

%changelog
* Sat Apr 23 2016 Gleb Goncharov <yum@gongled.ru> - 2.2.7-0
- Initial build

