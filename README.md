## About

Spec files and patches for GONGLED repository. It works on CentOS/RHEL 6.x.

## Quick start

Run this command on your system via root:

```
yum install -y https://release.yum.gongled.me/6/x86_64/gongled-repo-6.8-0.el6.noarch.rpm
```

## Manual installation

Import GPG public key:
```
wget -O https://raw.githubusercontent.com/gongled/gongled-repo/master/gongled-repo/RPM-GPG-KEY-GONGLED /etc/pki/rpm-gpg/RPM-GPG-KEY-GONGLED
```
Add 'testing' and 'release' repository:
```
wget -O https://raw.githubusercontent.com/gongled/gongled-repo/master/gongled-repo/gongled-testing.repo /etc/yum.repos.d/gongled-testing.repo
wget -O https://raw.githubusercontent.com/gongled/gongled-repo/master/gongled-repo/gongled-release.repo /etc/yum.repos.d/gongled-release.repo
```
Done.

## License

MIT License

