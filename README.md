## About

Spec files and patches for SIMTECH repository.

  * [Installation](#installation)
  * [Supported OS](#supported-os)
  * [RPMLint Status](#rpmlint-status)
  * [License](#license)

#### Installation

1. Install [EPEL repository](https://fedoraproject.org/wiki/EPEL)

    ```
    [sudo] yum -y install epel-release
    ```

2. Install [ESSENTIAL KAOS public repository](https://yum.kaos.io)

    ```
    [sudo] yum -y install http://release.yum.kaos.io/x86_64/kaos-repo-7.0-0.el6.noarch.rpm
    ```

3. Install [SIMTECH repository](https://release.yum.smtk.us)

    ```
    [sudo] yum -y install https://release.yum.smtk.us/smtk-release-6.noarch.rpm 
    ```

#### Supported OS

* CentOS/RedHat/Scientific Linux 6.x
* CentOS/RedHat/Scientific Linux 7.x

#### RPMLint status

| Repository | Status |
|------------|--------|
| Stable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=master)](https://travis-ci.org/simtechdev/smtk-repo) |
| Unstable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=develop)](https://travis-ci.org/simtechdev/smtk-repo) |

#### License

MIT

