Server Account Setup
=========

General setup for hosting accounts.

Requirements
------------

Assumes that the account exists.

Role Variables
--------------

# Text for begin / end markers in ~/.bash_profile
bash_profile_marker_text: "ANSIBLE MANAGED BLOCK: Standard .bash_profile"

# Full path to git-core installation directory on server.
git_core_dir: /usr/local/share/git-core

# Full path to existing git-completion shell script.
# This will be used in `.bash_profile` to enable git completion.
git_completion_path: "{{ git_core_dir }}/contrib/completion/git-completion.bash"

# Full path to existing git-prompt.sh.
# This will be used in `.bash_profile` to enable git prompt.
git_prompt_dir: "{{ git_core_dir }}/contrib/completion/git-prompt.sh"

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
