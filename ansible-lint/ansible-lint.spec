########################################################################################

Summary:        Ansible linter
Name:           ansible-lint
Version:        3.4.4
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries 
URL:            https://github.com/willthames/ansible-lint

Source:         https://github.com/willthames/%{name}/archive/v%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools libffi-devel

Requires:       ansible

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
ansible-lint checks playbooks for practices and behaviour that could potentially 
be improved.

########################################################################################

%prep
%setup -qn %{name}-%{version}

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
%{_bindir}/%{name}

########################################################################################

%changelog
* Tue Nov 29 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 3.4.4-0
- Updated to latest stable release

* Fri Aug 26 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 3.2.5-0
- Updated to latest stable release

* Thu Jun 23 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 3.0.0-0
- Updated to latest stable release

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- Updated to latest stable release

* Mon May 23 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.6.2-0
- Updated to latest stable release

* Sat Apr 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to latest stable release

* Tue Mar 08 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.3.9-0
- Initial build
