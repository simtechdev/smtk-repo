##########################################################################

%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

%define fmconfig          %{_sysconfdir}/yum/pluginconf.d/fastestmirror.conf

##########################################################################

Summary:         Simtech repository
Name:            smtk-repo
Version:         1.0
Release:         0%{?dist}
License:         MIT
Vendor:          Simtech
Group:           Development/Tools
URL:             https://simtechdev.com

Source0:         %{name}-%{version}.tar.gz

BuildArch:       noarch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        yum-plugin-priorities

Provides:        %{name} = %{version}-%{release}

%description
This package contains yum repo file for access to Simtech repository.

##########################################################################

%prep
%setup -qn %{name}-%{version}
%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -dm 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -dm 755 %{buildroot}%{_loc_datarootdir}/smtk-repo
install -dm 755 %{buildroot}%{_loc_datarootdir}/smtk-repo/release
install -dm 755 %{buildroot}%{_loc_datarootdir}/smtk-repo/testing

install -pm 644 *.repo \
                %{buildroot}%{_sysconfdir}/yum.repos.d/

install -pm 644 RPM-GPG-KEY-SIMTECH \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -pm 664 mirrors/release/* \
                %{buildroot}%{_loc_datarootdir}/smtk-repo/release/

install -pm 664 mirrors/testing/* \
                %{buildroot}%{_loc_datarootdir}/smtk-repo/testing/

%post
if [[ -f %{fmconfig} ]] ; then
  if [[ -z `grep 'smtk' %{fmconfig}` ]] ; then
    sed -i 's/^exclude.*/\0, smtk/g' %{fmconfig}
    sed -i 's/^#exclude.*/exclude=smtk/g' %{fmconfig}
  fi
fi

%clean
rm -rf %{buildroot}

##########################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*
%{_loc_datarootdir}/smtk-repo/*

##########################################################################

%changelog
* Fri Apr 15 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.0-0
- Initial build.

