################################################################################

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

################################################################################

Summary:              Simple app for automatization of everything
Name:                 sloth-ci
Version:              2.0.2
Release:              0%{?dist}
URL:                  http://sloth-ci.com
License:              MIT
Group:                Development/Libraries

Source:               https://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.zip

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch:            noarch

%if 0%{?rhel} == 6
Requires:             python-CherryPy
Requires:             python-routes
Requires:             PyYAML
Requires:             python-requests
Requires:             python-cliar
Requires:             python-colorama
Requires:             python-tabulate
%endif

################################################################################

%description
Sloth CI builds docs, runs tests, and deploys to servers when you push to 
GitHub or Bitbucket. The goal is to give you the easiest way to automatize 
things, with no memory overhead or overcomplicated setup. 

Installing, configuring, and running Sloth CI takes about two minutes, 
then you control it remotely via protected web API or command line interface.

################################################################################

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
%{python_sitelib}/*
%{_bindir}/sci
%{_bindir}/%{name}

########################################################################################

%changelog
* Wed Feb 24 2016 Gleb Goncharov <yum@gongled.ru> - 2.0.2-0
- Initial build

