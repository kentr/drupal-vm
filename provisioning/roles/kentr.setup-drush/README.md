Setup Drush
=========

Performs misc drush setup tasks for multiple installations on a host.

* Runs `drush init` on remote machine.
* Customizes `~/.drush/drushrc.php` on remote machine.
* Creates aliases on host and remote machines.

Requirements
------------

Drush installed on remote machine.

Role Variables
--------------

# Enable the "common" structure-tables-key.
# See https://raw.githubusercontent.com/drush-ops/drush/master/examples/example.drushrc.php
drush_enable_structure_tables_key_common: True

# Enable insertion of local and remote drush aliases.
# Values are taken from inventory values for host.
drush_aliases_remote: True
drush_aliases_local: True


# Enable dated sql-dump result file.
drush_enable_dated_result_file: True

drush_alias_file_prefix: "{{ inventory_hostname }}"

# SSH options passed to Drush.
# This string will be enclosed by single quotes in the PHP Drush alias file.
drush_ssh_options: "-o PasswordAuthentication=no -o LogLevel=quiet"

# Destination directory for SQL dump files.
drush_sql_dump_dir: "/home/{{ ansible_ssh_user }}/drush-backups/archive-dump"

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: kentr.setup-drush, installations: list_of_installations }

License
-------

BSD 3-Clause

Author Information
------------------

Kent Richards, https://kentrichards.net
