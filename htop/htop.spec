###############################################################################

Summary:              Interactive process viewer
Name:                 htop
Version:              1.0.3
Release:              0%{?dist}
License:              GPL
Group:                Applications/System
URL:                  http://htop.sourceforge.net/

Source:               http://hisham.hm/htop/releases/%{version}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:        gcc >= 3.0 ncurses-devel

###############################################################################

%description
htop is an interactive process viewer for Linux.

###############################################################################

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{make_install}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%doc %{_mandir}/man1/htop.1*
%{_bindir}/htop
%{_datadir}/applications/htop.desktop
%{_datadir}/pixmaps/htop.png

###############################################################################

%changelog
* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.0.3-0
- Updated to version 1.0.3

* Fri Feb  1 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Updated to version 1.0.2

* Sat Apr 21 2012 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-3
- Updated to release 1.0.1 and rewrited spec by David Hrbáč
