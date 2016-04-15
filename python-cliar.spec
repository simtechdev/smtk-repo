########################################################################################

%define package_name      cliar

########################################################################################

Summary:        Tools for command-line interfaces with minimum code
Name:           python-cliar
Version:        1.1.4
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://pypi.python.org/pypi/cliar

Source:         https://pypi.python.org/packages/source/c/%{package_name}/%{package_name}-%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Cliar is designed to help you create CLIs quickly and with as little code as possible.

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
%{python_sitelib}/*

########################################################################################

%changelog
* Wed Feb 24 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.1.4-0
- Initial build

