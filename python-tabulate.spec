########################################################################################

%define package_name      tabulate

########################################################################################

Summary:        Pretty-print tabular data
Name:           python-tabulate
Version:        0.7.5
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://pypi.python.org/pypi/tabulate

Source:         https://pypi.python.org/packages/source/t/%{package_name}/%{package_name}-%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Pretty-print tabular data in Python, a library and a command-line utility.

The main use cases of the library are:
* printing small tables without hassle: just one function call,
  formatting is guided by the data itself
* authoring tabular data for lightweight plain-text markup:
  multiple output formats suitable for further editing or transformation
* readable presentation of mixed textual and numeric data:
  smart column alignment, configurable number formatting, alignment by a decimal point

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
%{_bindir}/%{package_name}

########################################################################################

%changelog
* Wed Feb 24 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 0.7.5-0
- Initial build

