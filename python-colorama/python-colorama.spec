########################################################################################

%define package_name      colorama

########################################################################################

Summary:        Cross-platform colored terminal text.
Name:           python-colorama
Version:        0.3.6
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://pypi.python.org/pypi/colorama

Source:         https://pypi.python.org/packages/source/c/colorama/colorama-%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Makes ANSI escape character sequences (for producing colored terminal text and cursor 
positioning) work under MS Windows. ANSI escape character sequences have long been used 
to produce colored terminal text and cursor positioning on Unix and Macs. 

Colorama makes this work on Windows, too, by wrapping stdout, stripping ANSI sequences 
it finds (which would appear as gobbledygook in the output), and converting them into 
the appropriate win32 calls to modify the state of the terminal. 

On other platforms, Colorama does nothing.

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
* Wed Feb 24 2016 Gleb Goncharov <yum@gongled.ru> - 0.3.6-0
- Initial build

