## About

Spec files and patches for SIMTECH repository. It works on CentOS/RHEL 6.x/7.x.

  * [Installation](#installation)
  * [RPMLint Status](#rpmlint-status)
  * [License](#license)

[![asciicast](https://asciinema.org/a/43720.png)](https://asciinema.org/a/43720)

#### Installation

1. Install EPEL repository

    ```
    [sudo] yum -y install epel-release
    ```

2. Install ESSENTIAL KAOS public repository

    ```
    [sudo] yum -y install http://release.yum.kaos.io/x86_64/kaos-repo-7.0-0.el6.noarch.rpm
    ```

3. Install SIMTECH public repository

    ```
    [sudo] yum -y install https://release.yum.smtk.us/smtk-release-6.noarch.rpm 
    ```

#### RPMLint status

| Repository | Status |
|------------|--------|
| Stable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=master)](https://travis-ci.org/simtechdev/smtk-repo) |
| Unstable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=develop)](https://travis-ci.org/simtechdev/smtk-repo) |

#### License

MIT

