########################################################################################

%define package_name      certifi

########################################################################################

Summary:        Python package for providing Mozilla's CA Bundle.
Name:           python-certifi
Version:        2016.09.26
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://pypi.python.org/pypi/certifi

Source:         https://github.com/certifi/python-%{package_name}/archive/%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

Requires:       python-requests python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Certifi is a carefully curated collection of Root Certificates for validating the 
trustworthiness of SSL certificates while verifying the identity of TLS hosts. 
It has been extracted from the Requests project.

########################################################################################

%prep
%setup -q -n %{name}-%{version}

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
%doc LICENSE
%{python_sitelib}/*

########################################################################################

%changelog
* Tue Nov 29 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2016.9.26-0
- Initial build
