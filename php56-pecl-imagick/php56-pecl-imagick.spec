################################################################################

%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%define php_inidir     %{_sysconfdir}/php.d
%define php_incldir    %{_includedir}/php
%define php_ztsincldir %{_includedir}/php-zts
%define php_extdir     %{_libdir}/php/modules

%define php_core_api   20131106
%define php_zend_api   20131226

%define basepkg        php56
%define pecl_name      imagick

%define with_zts       0%{?__ztsphp:1}

################################################################################

Summary:          Provides a wrapper to the ImageMagick library
Name:             %{basepkg}-pecl-%{pecl_name}
Version:          3.3.0
Release:          0%{?dist}
License:          PHP
Group:            Development/Libraries
URL:              http://pecl.php.net/package/%{pecl_name}

Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:          %{pecl_name}.ini

BuildRoot:        %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires:    %{basepkg}-pear >= 1.4.7
BuildRequires:    %{basepkg}-devel >= 5.4.0, ImageMagick-devel >= 6.5.3

Provides:         php-pecl(%{pecl_name}) = %{version}
Provides:         php-pecl-%{pecl_name} = %{version}

Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}

################################################################################

%description
%{pecl_name} is a native php extension to create and modify images using the
ImageMagick API. 

This extension requires ImageMagick version 6.5.3+ and PHP 5.4.0+.

IMPORTANT: Version 2.x API is not compatible with earlier versions.

################################################################################

%package devel
Summary:          Imagick developer files (header)
Group:            Development/Libraries

Requires:         %{name} = %{version}-%{release}
Requires:         %{basepkg}-devel
Provides:         php-pecl-imagick-devel = %{version}-%{release}

%description devel
These are the files needed to compile programs using Imagick.

################################################################################

%prep
%setup -qc -n %{pecl_name}-%{version}

%if %{with_zts}
cp -r %{pecl_name}-%{version}% %{pecl_name}-%{version}-zts
%endif

%build
pushd %{pecl_name}-%{version}
phpize
%configure \
  --with-%{pecl_name} \
  --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}%-zts
zts-phpize
%configure \
  --with-%{pecl_name} \
  --with-php-config=%{_bindir}/zts-php-config
%{__make} %{?_smp_mflags}
popd
%endif

%install
%{__rm} -rf %{buildroot}

pushd %{pecl_name}-%{version}
%{__make} install \
  INSTALL_ROOT=%{buildroot}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
%{__make} install \
  INSTALL_ROOT=%{buildroot}
popd
%endif

install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0755 -d %{buildroot}%{php_inidir}

install -m 0664 %{SOURCE1} %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -m 0664 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

%if %{with_zts}
install -d %{buildroot}%{php_ztsinidir}
install -m 0664 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml
%endif

%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
  %{pecl_uninstall} %{pecl_name}
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}%{?rcver}/examples %{pecl_name}-%{version}%{?rcver}/CREDITS
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif

%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif

################################################################################

%changelog
* Fri Jan 22 2016 Andy Thompson <andy@webtatic.com> - 3.3.0-0
- Initial build. 
