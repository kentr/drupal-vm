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

# For drush aliases on the remote machine, items in `installations` that have an
# `environment` property matching this list will be created as "local" aliases.
# SSH options will be ignored.
#
# This is useful when the remote node being provisioned by Ansible is actually a
# `local` dev environment.
# On that remote node, a drush alias for `local` will be created without
# SSH options, so that the alias acts on the machine.
drush_aliases_remote_skip_ssh:
  - local

# Enable dated sql-dump result file.
drush_enable_dated_result_file: True

drush_alias_file_prefix: "{{ inventory_hostname }}"

# SSH options passed to Drush.
# This string will be enclosed by single quotes in the PHP Drush alias file.
drush_ssh_options: "-o PasswordAuthentication=no -o LogLevel=quiet"


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
