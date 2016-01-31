################################################################################

%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%define php_inidir     %{_sysconfdir}/php.d
%define php_incldir    %{_includedir}/php
%define php_ztsincldir %{_includedir}/php-zts
%define php_extdir     %{_libdir}/php/modules

%define php_core_api   20131106
%define php_zend_api   20131226

%define basepkg        php56
%define pecl_name      igbinary

%define with_zts       0%{?__ztsphp:1}

################################################################################

Summary:          Replacement for the standard PHP serializer
Name:             %{basepkg}-pecl-%{pecl_name}
Version:          1.2.1
Release:          0%{?dist}
License:          BSD
Group:            System Environment/Libraries

URL:              http://pecl.php.net/package/igbinary

Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:          %{pecl_name}.ini

BuildRoot:        %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:    %{basepkg}-devel >= 5.2.0
BuildRequires:    %{basepkg}-pecl-apcu-devel >= 3.1.7

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}

Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
Provides:         php-pecl(%{pecl_name}) = %{version}
Provides:         php-pecl-igbinary = %{version}
Provides:         php-pecl-igbinary%{?_isa} = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif

################################################################################

%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.

################################################################################

%package devel
Summary:       Igbinary developer files (header)
Group:         Development/Libraries
Requires:      %{basepkg}-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
Requires:      php-devel
Provides:      php-pecl-igbinary-devel = %{version}
Provides:      php-pecl-igbinary-devel%{?_isa} = %{version}

%description devel
These are the files needed to compile programs using Igbinary

################################################################################

%prep
%setup -q -c

%if %{with_zts}
cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts
%endif

%build
pushd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif

%install
%{__rm} -rf %{buildroot}

make install -C %{pecl_name}-%{version} \
     INSTALL_ROOT=%{buildroot}


install -m 755 -d %{buildroot}%{php_inidir}
install -m 644 -D %{SOURCE1} %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
make install -C %{pecl_name}-%{version}-zts \
     INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}%{php_ztsinidir}
install -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%check

%if 0%{?with_tests}
pushd %{pecl_name}-%{version}
%{__php} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

ln -s %{php_extdir}/apcu.so modules/

TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=apcu.so -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
%{__ztsphp} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

ln -s %{php_ztsextdir}/apcu.so modules/

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=apcu.so -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php
popd
%endif
%endif

%clean
rm -rf %{buildroot}

%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/COPYING
%doc %{pecl_name}-%{version}/CREDITS
%doc %{pecl_name}-%{version}/NEWS
%doc %{pecl_name}-%{version}/README.md
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
* Sun Jan 17 2016 Gleb Goncharov <yum@gongled.me> - 1.2.1-0
- Initial build

