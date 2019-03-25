import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Define fixture for dynamic ansible role variables.
@pytest.fixture
def ansible_role_vars(host):

    # Include variables from ansible variable files.
    # Paths must be relative to the scenario directory.
    # `test_variable_files` is declared in `base-config.yml`,
    # under the `all` group.
    try:
        vars_files = host.ansible.get_variables()['test_variable_files']
    except KeyError:
        raise KeyError("Could not get ansible variable 'test_variable_files'"
                       " to use in 'include_vars'. Is it defined?")

    # Load variables from `vars_files` into `host`.
    for file in vars_files:
        host.ansible(
            "include_vars",
            "file=" + file
        )

    return host.ansible.get_variables()


def test_installed_site_home_page_title(host, ansible_role_vars):

    # Test both that the home page loads at all, and that
    # it contains the configured site title.
    cmd = host.run('curl -s --location ' +
                   ansible_role_vars['local_domain'])

    assert ('<title>Welcome to ' +
            ansible_role_vars['drupal_site_name']) in cmd.stdout
