Name:           mod_rpaf
Version:        0.8.4 
Release:        0%{?dist}
Summary:        Reverse proxy add forward module for Apache

Group:          System Environment/Daemons
License:        ASL 1.0
URL:            http://stderr.net/apache/rpaf/
Source0:        https://github.com/gnif/%{name}/archive/v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
Requires:       httpd

%description
Reverse proxy add forward module for Apache


%prep
%setup -q

%build
make

%install
install -dm 755 %{buildroot}/usr/lib64/httpd/modules
%{make_install}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES
%{_libdir}/httpd/modules/mod_rpaf.so



%changelog
* Sun Aug 23 2009 Frolov Denis <d.frolov81 at mail.ru> 0.6-2
- Add path patch

* Mon May 27 2008 Frolov Denis <d.frolov81 at mail.ru> 0.6-1
- Initial build for Red Hat Club Repository
