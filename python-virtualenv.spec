%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-virtualenv
Version:        1.10.1
Release:        0%{?dist}
Summary:        Tool to create isolated Python environments

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/virtualenv
Source0:        http://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       python-setuptools, python2-devel

%if 0%{?fedora}
BuildRequires:  python-sphinx
%endif


%description
virtualenv is a tool to create isolated Python environments. virtualenv
is a successor to workingenv, and an extension of virtual-python. It is
written by Ian Bicking, and sponsored by the Open Planning Project. It is
licensed under an MIT-style permissive license.


%prep
%setup -q -n virtualenv-%{version}
%{__sed} -i -e "1s|#!/usr/bin/env python||" virtualenv.py 

%build
# Build code
%{__python} setup.py build

# Build docs on Fedora
%if 0%{?fedora} > 0
%{__python} setup.py build_sphinx
%endif


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
rm -f build/sphinx/html/.buildinfo


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/*rst PKG-INFO AUTHORS.txt LICENSE.txt
# Include sphinx docs on Fedora
%if 0%{?fedora} > 0
%doc build/sphinx/*
%endif
# For noarch packages: sitelib
%{python_sitelib}/*
%attr(755,root,root) %{_bindir}/virtualenv*


%changelog
* Wed Mar 09 2016 Gleb Goncharov <yum@gongled.ru> - 1.10.1-0
- Initial build.

