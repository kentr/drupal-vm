Setup WP-CLI
============

Performs misc WP-CLI setup tasks for multiple installations on a host.

* Creates aliases on host and remote machines.

Requirements
------------

WP-CLI installed on remote machine.

Role Variables
--------------

# Enable insertion of local and remote WP-CLI aliases.
# Values are taken from inventory values for host.
wp_aliases_remote: True
wp_aliases_local: True

wp_alias_prefix: "{{ inventory_hostname }}"

# Destination directory for SQL dump files.
wp_sql_dump_dir: "/tmp"

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: kentr.setup-wp-cli, installations: list_of_installations }

License
-------

BSD 3-Clause

Author Information
------------------

Kent Richards, https://kentrichards.net
