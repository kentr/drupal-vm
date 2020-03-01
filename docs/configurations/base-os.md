Drupal VM's configuration is designed to work with RedHat and Debian-compatible operating systems. Therefore, if you switch the `vagrant_box` in `config.yml` to any compatible OS, Drupal VM and all it's configuration should _Just Work™_... but that's not always the case.

Currently-supported OSes are:

  - Ubuntu 18.04 'Bionic' (default)
  - Ubuntu 16.04 'Xenial'
  - RedHat Enterprise Linux / CentOS 8
  - RedHat Enterprise Linux / CentOS 7
  - Debian 10 'Buster'
  - Debian 9 'Stretch'

For certain OSes, there are a couple other caveats and tweaks you may need to perform to get things running smoothly—the main features and latest development is only guaranteed to work with the default OS as configured in `default.config.yml`.

Some other OSes should work, but are not regularly tested with Drupal VM, including Debian 8/Jessie (`debian/jessie64`).

## Ubuntu 18.04 Xenial LTS

Everything should work out of the box with Ubuntu 16.04.

## Ubuntu 16.04 Xenial LTS

Everything should work out of the box with Ubuntu 16.04.

## RedHat Enterprise Linux / CentOS 8

Everything should work out of the box with RHEL 8.

## RedHat Enterprise Linux / CentOS 7

Everything should work out of the box with RHEL 7.

## Debian 10 Buster

Everything should work out of the box with Debian 10.

## Debian 9 Stretch

Everything should work out of the box with Debian 10.
