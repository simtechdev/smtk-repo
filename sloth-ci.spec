################################################################################

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

################################################################################

Summary:              Simple app for automatization of everything
Name:                 sloth-ci
Version:              2.0.7
Release:              0%{?dist}
URL:                  http://sloth-ci.com
License:              MIT
Group:                Development/Libraries

Source0:              https://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch:            noarch

Requires:             python-CherryPy
Requires:             python-routes
Requires:             PyYAML
Requires:             python-requests
Requires:             python-cliar
Requires:             python-colorama
Requires:             python-tabulate

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
* Thu Mar 10 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.0.7-0
- Updated to latest version

* Wed Feb 24 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.0.2-0
- Initial build

