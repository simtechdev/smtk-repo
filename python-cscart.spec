########################################################################################

%define package_name      pycscart

########################################################################################

Summary:        Python client for interacting with CS-Cart API
Name:           python-cscart
Version:        1.0.3
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://pypi.python.org/pypi/pycscart

Source:         https://github.com/gongled/%{package_name}/archive/v%{version}.tar.gz

BuildRequires:  python-requests python-devel python-setuptools

Requires:       python-requests python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Python library and RESTful API client for CS-Cart shopping cart software. It allows
interact with a store and manipulate products, categories, orders and so forth.

########################################################################################

%prep
%setup -q -n %{package_name}-%{version}

%clean
rm -rf %{buildroot}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

########################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/*

########################################################################################

%changelog
* Sun Dec 11 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.0.3-0
- Updated to the latest release. 

* Thu Nov 24 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.0.2-0
- Initial build
