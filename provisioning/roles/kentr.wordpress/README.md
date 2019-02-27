# Ansible Role: WordPress

[![Build Status](https://travis-ci.org/kentr/ansible-role-wordpress.svg?branch=master)](https://travis-ci.org/kentr/ansible-role-wordpress)

Ansible role that installs and configures WordPress, forked from https://github.com/chusiang/wordpress.ansible.role.

Features include:
- Installation of any WordPress version to specified directory
- Configuration of wp-config.php
- Fetch random salts for wp-config.php (https://api.wordpress.org/secret-key/1.1/salt/)

## Installation

Using `git`:
```shell
$ git clone https://github.com/kentr/wordpress.ansible.role.git
```

## Requirements & Dependencies
- Ansible 2.7 or higher
- Curl

## Variables

```yaml
wp_version: 4.0
wp_install_dir: '/var/sites/awesome_wordpress_site'
wp_db_name: 'wordpress'
wp_db_user: 'wordpress'
wp_db_password: 'wordpress'
wp_db_host: 'localhost'
wp_db_charset: 'utf8'
wp_db_collate: ''
wp_table_prefix: 'wp_'
wp_debug: false
wp_debug_log: true
wp_debug_display: false

wp_add_siteurl_to_wp_config: False

wp_install_site: False
wp_admin_user: 'admin'
wp_admin_password: ''
wp_admin_email: ''
wp_site_title: 'WordPress'
wp_domain: "wordpress.test"

wp_install_dummy_data: False

wp_fs_method: 'direct'
wp_lang: ''

wp_mysql_enable: true
wp_mysql_db_create: false
wp_mysql_db_create_users: false
wp_mysql_site_restore_saved_db: false
wp_backup_local_path: "{{ playbook_dir }}/_private/backup"
# Local path to database dump file.
# File must be gzipped.
wp_database_backup: "{{ wp_backup_local_path }}/{{ wp_site_name }}.sql.gz"
wp_site_name: "{{ wp_apache_hostname | default('example') }}"

# Set this to 'true' and specify a Git repository if you want to deploy WordPress
# to your server from an existing repository.
wp_deploy: false
wp_deploy_clone_depth: 20
# Should the clone be a single-branch repo?
wp_deploy_clone_single_branch: False
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
  - kentr.wordpress
```

## Testing
```shell
$ git clone https://github.com/kentr/wordpress.ansible.role.git
$ cd wordpress.ansible.role
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
