## About

Spec files and patches for SIMTECH repository. It works on CentOS/RHEL 6.x/7.x.

[![asciicast](https://asciinema.org/a/43720.png)](https://asciinema.org/a/43720)

#### Installation

###### CentOS/RHEL 6.x

```
sudo yum install -y https://release.yum.smtk.us/smtk-release-6.noarch.rpm
```

###### CentOS/RHEL 7.x

```
sudo yum install -y https://release.yum.smtk.us/smtk-release-7.noarch.rpm
```

#### RPMLint status

We use Travis CI to perform spec checking automatically via `rpmlint`.

| Repository | Status |
|------------|--------|
| Stable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=master)](https://travis-ci.org/simtechdev/smtk-repo) |
| Unstable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=develop)](https://travis-ci.org/simtechdev/smtk-repo) |

#### License

[MIT](https://github.com/simtechdev/smtk-repo/blob/master/LICENSE)

