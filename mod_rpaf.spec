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
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -dm 755 %{buildroot}/usr/lib64/httpd/modules
%{make_install}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGES
%{_libdir}/httpd/modules/mod_rpaf.so


%changelog
* Wed Mar 09 2016 Gleb Goncharov <yum@gongled.ru> - 0.6-0
- Initial build.

