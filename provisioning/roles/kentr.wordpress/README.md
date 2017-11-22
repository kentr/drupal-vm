# Ansible Role: WordPress
[![Build Status](https://travis-ci.org/darthwade/ansible-role-wordpress.png)](https://travis-ci.org/darthwade/ansible-role-wordpress)
[![Gittip](http://img.shields.io/gittip/darthwade.svg)](https://www.gittip.com/darthwade/)
[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=darthwade&url=https://github.com/darthwade/ansible-role-wordpress&title=Ansible Role: WordPress&language=&tags=github&category=software)

Ansible role that installs and configures WordPress.

Features include:
- Installation of any WordPress version to specified directory
- Configuration of wp-config.php
- Fetch random salts for wp-config.php (https://api.wordpress.org/secret-key/1.1/salt/)

## Installation

Using `ansible-galaxy`:
```shell
$ ansible-galaxy install darthwade.wordpress
```

Using `arm` ([Ansible Role Manager](https://github.com/mirskytech/ansible-role-manager/)):
```shell
$ arm install darthwade.wordpress
```

Using `git`:
```shell
$ git clone https://github.com/darthwade/ansible-role-wordpress.git
```

## Requirements & Dependencies
- Ansible 1.4 or higher
- Curl

## Variables
Here is a list of all the default variables for this role, which are also available in `defaults/main.yml`.

```yaml
---

wp_version: 4.0
# TODO: https://wordpress.org/download/release-archive/
# wp_sha256sum: 8543e31d7c0a1b15f73dbb20f9161845f3d2bb8de3d7aef371cf32bba41747ee
wp_install_dir: '/var/sites/awesome_wordpress_site'
wp_db_name: 'database_name_here'
wp_db_user: 'username_here'
wp_db_password: 'password_here'
wp_db_host: 'localhost'
wp_db_charset: 'utf8'
wp_db_collate: ''
wp_table_prefix: 'wp_'
wp_debug: false

wp_install_site: False
wp_admin_user: 'admin'
wp_admin_password: ''
wp_admin_email: ''
wp_site_title: 'My Great WordPress Site'

wp_fs_method: 'direct'
wp_lang: ''

wp_mysql_enable: true
wp_mysql_db_create: true
wp_mysql_site_restore_saved_db: false
wp_backup_local_path: "{{ playbook_dir }}/_private/backup"
wp_database_backup: "{{ wp_backup_local_path }}/{{ wp_site_name }}.sql"
wp_site_name: "{{ wp_apache_hostname | default('example') }}"

# Set this to 'true' and specify a Git repository if you want to deploy WordPress
# to your server from an existing repository.
wp_deploy: false
wp_deploy_repo: ""
wp_deploy_version: master
wp_deploy_update: true
wp_deploy_dir: "{{ wp_install_dir }}"
wp_deploy_accept_hostkey: no

wp_core_owner: "{{ ansible_ssh_user | default(ansible_env.SUDO_USER, true) | default(ansible_env.USER, true) | default(ansible_user_id) }}"
wp_core_group: "{{ ansible_ssh_user | default(ansible_env.SUDO_USER, true) | default(ansible_env.USER, true) | default(ansible_user_id) }}"

workspace: /tmp
```

## Example playbook
```yaml
- hosts: all
  vars:
    wp_version: 4.0
    wp_install_dir: '/var/sites/awesome_wordpress_site'
    wp_db_name: 'database_name_here'
    wp_db_user: 'username_here'
    wp_db_password: 'password_here'
    wp_db_host: 'localhost'
  roles:
  - darthwade.wordpress
```

## Testing
```shell
$ git clone https://github.com/darthwade/ansible-role-wordpress.git
$ cd ansible-role-wordpress
$ vagrant up
```

## Contributing
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests and examples for any new or changed functionality.

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## License

Licensed under the MIT License. See the LICENSE file for details.

Copyright (c) 2014 [Vadym Petrychenko](http://petrychenko.com/)
