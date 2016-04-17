################################################################################

%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%define php_inidir     %{_sysconfdir}/php.d
%define php_incldir    %{_includedir}/php
%define php_ztsincldir %{_includedir}/php-zts
%define php_extdir     %{_libdir}/php/modules

%define php_core_api   20131106
%define php_zend_api   20131226

%define basepkg        php56
%define pecl_name      apcu

%define with_zts       0%{?__ztsphp:1}

################################################################################

Summary:          APCu - APC User Cache
Name:             %{basepkg}-pecl-%{pecl_name}
Version:          4.0.10
Release:          0%{?dist}
License:          PHP
Group:            Development/Languages
URL:              http://pecl.php.net/package/APCu

Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:          %{pecl_name}.ini

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root

Conflicts:        php-mmcache, php-eaccelerator

BuildRequires:    %{basepkg}-devel >= 5.1.0, httpd-devel, %{basepkg}-pear

Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}

Provides:         php-pecl(%{pecl_name}) = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}

################################################################################

%description
APCu is userland caching: APC stripped of opcode caching in preparation for the
deployment of Zend Optimizer+ as the primary solution to opcode caching in
future versions of PHP

################################################################################

%package devel
Summary:          APCu developer files (header)
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         php-devel
Provides:         php-pecl-apc-devel = %{version}-%{release}

%description devel
These are the files needed to compile programs using APCu.

################################################################################

%prep
%setup -q -c

%if %{with_zts}
cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts
%endif

%build
pushd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --enable-apcu-mmap --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure --enable-apcu-mmap --with-php-config=%{_bindir}/zts-php-config
%{__make} %{?_smp_mflags}
popd
%endif

%install
%{__rm} -rf %{buildroot}

pushd %{pecl_name}-%{version}
%{__make} install INSTALL_ROOT=%{buildroot}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
%{__make} install INSTALL_ROOT=%{buildroot}
popd
%endif

install -m 755 -d %{buildroot}%{php_inidir}
install -m 755 -d %{buildroot}%{pecl_xmldir}

install -m 644 %{SOURCE1} %{buildroot}%{php_inidir}
install -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
install -m 755 -d %{buildroot}%{php_ztsinidir}
install -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}
%endif

%check

%if 0%{?with_tests}
pushd %{pecl_name}-%{version}
TEST_PHP_EXECUTABLE=$(which php) php run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=%{pecl_name}.so
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
TEST_PHP_EXECUTABLE=$(which zts-php) zts-php run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=%{pecl_name}.so
popd
%endif

%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
%endif
%endif

%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%doc %{pecl_name}-%{version}/{TECHNOTES.txt,LICENSE,NOTICE,apc.php,INSTALL}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif

%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif

################################################################################

%changelog
* Sun Jan 17 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 4.0.10-0
- Initial build

