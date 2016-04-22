###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

###############################################################################

%define service_user         %{name}
%define service_group        %{name}
%define service_name         %{name}
%define service_home         %{_cachedir}/%{service_name}

%define open_ssl_ver         1.0.2g

%define lua_module_ver       0.10.2
%define mh_module_ver        0.29

###############################################################################

Summary:              Rocket-fast web server
Name:                 nginx
Epoch:                1
Version:              1.9.15
Release:              0%{?dist}
License:              2-clause BSD-like license
Group:                System Environment/Daemons
Vendor:               Nginx / Google / CloudFlare
URL:                  http://gongled.ru/

Source0:              http://nginx.org/download/%{name}-%{version}.tar.gz
Source1:              %{name}.logrotate
Source2:              %{name}.init
Source3:              %{name}.sysconfig
Source4:              %{name}.conf
Source5:              upstream.conf

Source10:             error-40X.conf
Source11:             error-50X.conf

Source20:             ssl.conf
Source21:             common.conf
Source22:             fastcgi_params.conf
Source23:             fastcgi_params_ssl.conf
Source24:             proxy_params.conf
Source25:             proxy_params_ssl.conf

Source40:             %{name}-index.html
Source41:             %{name}-401.html
Source42:             %{name}-403.html
Source43:             %{name}-404.html
Source44:             %{name}-502.html
Source45:             %{name}-50X.html
Source46:             %{name}-maintenance.html

Source60:             http://www.openssl.org/source/openssl-%{open_ssl_ver}.tar.gz
Source61:             https://github.com/openresty/headers-more-nginx-module/archive/v%{mh_module_ver}.tar.gz
Source62:             https://github.com/chaoslawful/lua-nginx-module/archive/v%{lua_module_ver}.tar.gz

Patch0:               %{name}.patch
Patch1:               mime.patch
Patch2:               %{name}-autoindex-length.patch

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             initscripts >= 8.36 openssl zlib
Requires:             gd libXpm libxslt
%if 0%{?rhel} <= 6
Requires:             libluajit
%endif
%if 0%{?rhel} == 7
Requires:             luajit
%endif
Requires:             kaosv

BuildRequires:        make gcc-c++ zlib-devel pcre-devel perl
BuildRequires:        openssl-devel make
%if 0%{?rhel} <= 6
BuildRequires:        libluajit-devel
%endif
%if 0%{?rhel} == 7
BuildRequires:        luajit-devel
%endif

Requires(pre):        shadow-utils
Requires(post):       chkconfig

###############################################################################

%description
Rocket-fast performance webserver based on Nginx code, with some optimizations
and improvements.

###############################################################################

%package debug

Summary:           Debug version of nginx
Group:             System Environment/Daemons
Requires:          %{name} >= %{version}

%description debug
Not stripped version of nginx with the debugging log support

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__tar} xzvf %{SOURCE60}
%{__tar} xzvf %{SOURCE61}
%{__tar} xzvf %{SOURCE62}

# Renaming and moving docs
%{__mv} CHANGES    NGINX-CHANGES
%{__mv} CHANGES.ru NGINX-CHANGES.ru
%{__mv} LICENSE    NGINX-LICENSE
%{__mv} README     NGINX-README

%{__mv} lua-nginx-module-%{lua_module_ver}/README.markdown ./LUAMODULE-README.markdown
%{__mv} lua-nginx-module-%{lua_module_ver}/Changes         ./LUAMODULE-CHANGES

./configure \
        --prefix=%{_sysconfdir}/%{name} \
        --sbin-path=%{_sbindir}/%{name} \
        --conf-path=%{_sysconfdir}/%{name}/%{name}.conf \
        --error-log-path=%{_logdir}/%{name}/error.log \
        --http-log-path=%{_logdir}/%{name}/access.log \
        --pid-path=%{_rundir}/%{name}.pid \
        --lock-path=%{_rundir}/%{name}.lock \
        --http-client-body-temp-path=%{service_home}/client_temp \
        --http-proxy-temp-path=%{service_home}/proxy_temp \
        --http-fastcgi-temp-path=%{service_home}/fastcgi_temp \
        --http-uwsgi-temp-path=%{service_home}/uwsgi_temp \
        --http-scgi-temp-path=%{service_home}/scgi_temp \
        --user=%{service_user} \
        --group=%{service_group} \
        %{?_with_http_random_index_module} \
        %{?_with_http_xslt_module} \
        %{?_with_http_flv_module} \
        --with-http_v2_module \
        --with-http_gunzip_module \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gzip_static_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        --with-openssl-opt=no-krb5 \
        --with-openssl=openssl-%{open_ssl_ver} \
        --with-threads \
        --add-module=headers-more-nginx-module-%{mh_module_ver} \
        --add-module=lua-nginx-module-%{lua_module_ver} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
%{__make} %{?_smp_mflags}

%{__mv} %{_builddir}/%{name}-%{version}/objs/%{name} \
        %{_builddir}/%{name}-%{version}/objs/%{name}.debug

./configure \
        --prefix=%{_sysconfdir}/%{name} \
        --sbin-path=%{_sbindir}/%{name} \
        --conf-path=%{_sysconfdir}/%{name}/%{name}.conf \
        --error-log-path=%{_logdir}/%{name}/error.log \
        --http-log-path=%{_logdir}/%{name}/access.log \
        --pid-path=%{_rundir}/%{name}.pid \
        --lock-path=%{_rundir}/%{name}.lock \
        --http-client-body-temp-path=%{service_home}/client_temp \
        --http-proxy-temp-path=%{service_home}/proxy_temp \
        --http-fastcgi-temp-path=%{service_home}/fastcgi_temp \
        --http-uwsgi-temp-path=%{service_home}/uwsgi_temp \
        --http-scgi-temp-path=%{service_home}/scgi_temp \
        --user=%{service_user} \
        --group=%{service_group} \
        %{?_with_http_random_index_module} \
        %{?_with_http_xslt_module} \
        %{?_with_http_flv_module} \
        --with-http_v2_module \
        --with-http_gunzip_module \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_mp4_module \
        --with-http_gzip_static_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-openssl-opt=no-krb5 \
        --with-openssl=openssl-%{open_ssl_ver} \
        --with-threads \
        --add-module=headers-more-nginx-module-%{mh_module_ver} \
        --add-module=lua-nginx-module-%{lua_module_ver} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_datadir}/%{name}

%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/nginx.conf
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/*.default
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/fastcgi.conf
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/fastcgi_params
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/scgi_params
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/uwsgi_params

%{__rm} -rf %{buildroot}%{_sysconfdir}/%{name}/html

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/conf.d
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/vhost.d

install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{_rundir}/%{name}
install -dm 755 %{buildroot}%{_cachedir}/%{name}
install -dm 755 %{buildroot}%{_datadir}/%{name}/html

# Install html pages
install -pm 644 %{SOURCE40} \
                 %{buildroot}%{_datadir}/%{name}/html/index.html
install -pm 644 %{SOURCE41} \
                 %{buildroot}%{_datadir}/%{name}/html/401.html
install -pm 644 %{SOURCE42} \
                 %{buildroot}%{_datadir}/%{name}/html/403.html
install -pm 644 %{SOURCE43} \
                 %{buildroot}%{_datadir}/%{name}/html/404.html
install -pm 644 %{SOURCE44} \
                 %{buildroot}%{_datadir}/%{name}/html/502.html
install -pm 644 %{SOURCE45} \
                 %{buildroot}%{_datadir}/%{name}/html/50X.html
install -pm 644 %{SOURCE46} \
                 %{buildroot}%{_datadir}/%{name}/html/maintenance.html

ln -sf %{_datadir}/%{name}/html \
       %{buildroot}%{_sysconfdir}/%{name}/html

# Install SYSV init stuff
install -dm 755 %{buildroot}%{_initrddir}

install -pm 755 %{SOURCE2} \
                %{buildroot}%{_initrddir}/%{service_name}

# Install log rotation stuff
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d

install -pm 644 %{SOURCE1} \
                %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Directory for extra configs
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/xtra

# Install configs
install -pm 644 %{SOURCE4} \
                %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -pm 644 %{SOURCE5} \
                %{buildroot}%{_sysconfdir}/%{name}

install -pm 644 %{SOURCE10} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/
install -pm 644 %{SOURCE11} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/

install -pm 644 %{SOURCE20} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/
install -pm 644 %{SOURCE21} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/
install -pm 644 %{SOURCE22} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/
install -pm 644 %{SOURCE23} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/
install -pm 644 %{SOURCE24} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/
install -pm 644 %{SOURCE25} \
                %{buildroot}%{_sysconfdir}/%{name}/xtra/

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE3} \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -pm 644 %{_builddir}/nginx-%{version}/objs/%{name}.debug \
                %{buildroot}%{_sbindir}/%{name}.debug

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/ssl

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} -s /sbin/nologin -d %{service_home} %{service_user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add %{name}

  if [[ -d %{_logdir}/%{name} ]] ; then
    if [[ ! -e %{_logdir}/%{name}/access.log ]]; then
      touch %{_logdir}/%{name}/access.log
      %{__chmod} 640 %{_logdir}/%{name}/access.log
      %{__chown} %{service_user}: %{_logdir}/%{name}/access.log
    fi

    if [[ ! -e %{_logdir}/%{name}/error.log ]] ; then
      touch %{_logdir}/%{name}/error.log
      %{__chmod} 640 %{_logdir}/%{name}/error.log
      %{__chown} %{service_user}: %{_logdir}/%{name}/error.log
    fi
  fi
fi

# Increasing bucket size for x64
%ifarch %ix86
  sed -i 's/{BUCKET_SIZE}/32/g' \
         %{_sysconfdir}/%{name}/%{name}.conf &>/dev/null || :
  sed -i 's/{BUCKET_SIZE}/32/g' \
         %{_sysconfdir}/%{name}/%{name}.conf.rpmnew &>/dev/null || :
%else
  sed -i 's/{BUCKET_SIZE}/64/g' \
         %{_sysconfdir}/%{name}/%{name}.conf &>/dev/null || :
  sed -i 's/{BUCKET_SIZE}/64/g' \
         %{_sysconfdir}/%{name}/%{name}.conf.rpmnew &>/dev/null || :
%endif

###############################################################################

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{service_name} stop > /dev/null 2>&1
  %{__chkconfig} --del %{service_name}
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__service} %{service_name} upgrade &>/dev/null || :
fi

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc NGINX-CHANGES NGINX-CHANGES.ru NGINX-LICENSE NGINX-README
%doc LUAMODULE-README.markdown LUAMODULE-CHANGES

%{_sbindir}/%{name}

%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_sysconfdir}/%{name}/vhost.d
%dir %{_logdir}/nginx

%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/upstream.conf
%config(noreplace) %{_sysconfdir}/%{name}/xtra/fastcgi_*.conf
%config(noreplace) %{_sysconfdir}/%{name}/xtra/proxy_*.conf
%config %{_sysconfdir}/%{name}/xtra/error-*.conf
%config %{_sysconfdir}/%{name}/xtra/common.conf
%config %{_sysconfdir}/%{name}/xtra/ssl.conf

%config %{_sysconfdir}/%{name}/mime.types
%config %{_sysconfdir}/%{name}/koi-utf
%config %{_sysconfdir}/%{name}/koi-win
%config %{_sysconfdir}/%{name}/win-utf

%{_sysconfdir}/%{name}/html
%{_sysconfdir}/%{name}/ssl

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{service_name}

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/html
%{_datadir}/%{name}/html/*

%attr(0755,%{service_user},%{service_group}) %dir %{_cachedir}/%{name}
%attr(0755,%{service_user},%{service_group}) %dir %{_logdir}/%{name}

%files debug
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/%{name}.debug

###############################################################################

%changelog
* Thu Apr 21 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.15-0
- Nginx updated to 1.9.15

* Fri Apr 08 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.14-0
- Nginx updated to 1.9.14

* Tue Mar 01 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.10-2
- OpenSSL updated to 1.0.2g

* Wed Feb 17 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.10-1
- Dependencies updated to latest versions

* Wed Jan 27 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.10-0
- Nginx updated to 1.9.10

* Sun Dec 13 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.9-0
- Nginx updated to 1.9.9

* Fri Dec 04 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.7-0
- Nginx updated to 1.9.7

* Thu Nov 19 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.6-1
- Increase autoindex dir length.

* Mon Nov 16 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.6-0
- Nginx updated to 1.9.6

* Sun Aug 02 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.3-1
- Add additional configurations and preferences.

* Sun Aug 02 2015 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.9.3-0
- Nginx updated to 1.9.3
