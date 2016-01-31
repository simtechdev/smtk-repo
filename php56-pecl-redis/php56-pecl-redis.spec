################################################################################

%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%define php_inidir     %{_sysconfdir}/php.d
%define php_incldir    %{_includedir}/php
%define php_ztsincldir %{_includedir}/php-zts
%define php_extdir     %{_libdir}/php/modules

%define php_core_api   20131106
%define php_zend_api   20131226

%define basepkg        php56
%define pecl_name      redis

%define with_zts       0%{?__ztsphp:1}

################################################################################

Summary:          Extension for communicating with the Redis key-value store
Name:             %{basepkg}-pecl-%{pecl_name}
Version:          2.2.7
Release:          0%{?dist}
License:          PHP
Group:            Development/Languages
URL:              http://pecl.php.net/package/%{pecl_name}

Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:          https://github.com/nicolasff/phpredis/archive/%{version}.tar.gz
Source2:          %{pecl_name}.ini

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:    %{basepkg}-devel
BuildRequires:    %{basepkg}-pecl-igbinary-devel

Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
Requires:         php-pecl-igbinary%{?_isa}

Provides:         php-redis = %{version}-%{release}
Provides:         php-redis%{?_isa} = %{version}-%{release}
Provides:         php-pecl(%{pecl_name}) = %{version}
Provides:         php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:         php-pecl-%{pecl_name} = %{version}-%{release}
Provides:         php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif

################################################################################

%description
The php-redis extension provides an API for communicating
with the Redis key-value store.

This Redis client implements most of the latest Redis API.
As method only only works when also implemented on the server side,
some doesn't work with an old redis server version.

################################################################################

%prep
%setup -q -c -a 1

mv %{pecl_name}-%{version} nts
mv phpredis-%{version}/tests nts/tests

extver=$(sed -n '/#define PHP_REDIS_VERSION/{s/.* "//;s/".*$//;p}' nts/php_redis.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
cp -pr nts zts
%endif


%build
pushd nts
%{_bindir}/phpize
%configure \
  --enable-redis \
  --enable-redis-session \
  --enable-redis-igbinary \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

%if %{with_zts}
pushd zts
%{_bindir}/zts-phpize
%configure \
  --enable-redis \
  --enable-redis-session \
  --enable-redis-igbinary \
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif


%install
%{__rm} -rf %{buildroot}
make -C nts install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}%{php_inidir}/
install -m 644 -D %{SOURCE2} %{buildroot}%{php_inidir}/

%if %{with_zts}
make -C zts install INSTALL_ROOT=%{buildroot}
install -m 755 -d %{buildroot}%{php_ztsinidir}/
install -D -m 644 %{SOURCE2} %{buildroot}%{php_ztsinidir}/
%endif

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%check


%clean
%{__rm} -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%{pecl_xmldir}/%{name}.xml

%{php_extdir}/%{pecl_name}.so
%config(noreplace) %{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif

################################################################################

%changelog
* Fri Jan 22 2016 Gleb Goncharov <yum@gongled.me> - 2.2.7-0
- Initial build. 
