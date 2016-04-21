## About

Spec files and patches for SIMTECH repository. It works on CentOS/RHEL 6.x/7.x.

#### Installation

###### CentOS/RHEL 6.x

```
sudo yum install -y https://release.yum.smtk.st/smtk-release-6.noarch.rpm
```

###### CentOS/RHEL 7.x

```
sudo yum install -y https://release.yum.smtk.st/smtk-release-7.noarch.rpm
```

#### Usage

###### Quick start

1. Install the repository and install dependencies.

    ```
    sudo yum -y install rpmbuilder
    ```

2. Clone the repository, switch into the workspace and run building process.

    ```
    rpmbuilder name.spec -V -1 -di
    ```

Done. It works.

###### Advanced (using TerraFarm)

1. Install the repository and install dependencies.

    ```
    sudo yum -y install golang rpmbuilder terraform
    ```

2. Install [TerraFarm](https://github.com/essentialkaos/terrafarm), configure it properly and launch VMs.

    ```
    terrafarm create
    ```

    Be patient, it takes from 5 to 10 minutes.

3. Clone the repository, switch into the workspace and run building process.

    ```
    rpmbuilder name.spec -V -1 -di -r ~/build.nodes.list
    ```

If you were completed all steps correctly, `rpmbuilder` will test your spec file, 
connect to the build farm via SSH, install a necessary software, build packages and then 
download them into your machine.

#### Status

We use Travis CI to perform spec checking automatically via `rpmlint`.

| Repository | Status |
|------------|--------|
| Stable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=master)](https://travis-ci.org/simtechdev/smtk-repo) |
| Unstable | [![Build Status](https://travis-ci.org/simtechdev/smtk-repo.svg?branch=develop)](https://travis-ci.org/simtechdev/smtk-repo) |

#### License

[MIT](https://github.com/simtechdev/smtk-repo/blob/master/LICENSE)

