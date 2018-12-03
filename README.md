# About

Spec files and patches for SIMTECH repository.

  * [Installation](#installation)
  * [Supported OS](#supported-os)
  * [RPMLint Status](#rpmlint-status)
  * [Credits](#credits)
  * [License](#license)

## Installation

If you want to install RPM package repository to your system, please follow these steps:

1. Install ESSENTIAL KAOS repository

    ```
    [sudo] yum -y install http://release.yum.kaos.io/x86_64/kaos-repo-7.1-0.el6.noarch.rpm
    ```

2. Install package for YUM repository

    ```
    [sudo] yum -y install https://release.yum.smtk.us/smtk-release-6.noarch.rpm
    ```

## Supported OS

We support only these platforms and architectures:

* CentOS / RHEL 6.x ([x86_64](https://release.yum.smtk.us/6/x86_64/repoview/), [SRPMS](https://release.yum.smtk.us/6/SRPMS/repoview/))
* CentOS / RHEL 7.x ([x86_64](https://release.yum.smtk.us/7/x86_64/repoview/), [SRPMS](https://release.yum.smtk.us/7/SRPMS/repoview/))

## RPMLint status

| Repository | Status |
|------------|--------|
| Stable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=master)](https://travis-ci.org/simtechdev/smtk-repo) |
| Unstable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=develop)](https://travis-ci.org/simtechdev/smtk-repo) |

## Credits

* Many thanks [Anton Novojilov](https://github.com/andyone) for helping us maintain repository.

## License

MIT

