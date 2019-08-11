import os

import pytest
import testinfra.utils.ansible_runner
from ansible.utils.vars import combine_vars
from ansible.template import Templar
from ansible.parsing.dataloader import DataLoader

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Define fixture for dynamic ansible role variables.
@pytest.fixture
def ansible_dynamic_vars(host):

    # Include variables from ansible variable files.
    # Paths must be relative to the directory from which the `molecule`
    # command is run.
    # `test_variable_files` is declared in `base-config.yml`, under
    # the `all` group.
    try:
        vars_files = host.ansible.get_variables()['test_variable_files']
    except KeyError:
        raise KeyError("Could not get ansible variable 'test_variable_files'"
                       " to use in 'include_vars'. Is it defined?")

    test_vars = {}

    # Load variables from `vars_files`.
    # Accumulating the variables in this scope might be a hack, but I
    # can't find the updtream change that caused the previous code to
    # stop working.
    for file in vars_files:
        test_vars = combine_vars(test_vars, host.ansible(
            "include_vars",
            "file={}".format(file)
        )['ansible_facts'])

    # Interpolate the variables with the templater.
    # See https://github.com/philpep/testinfra/issues/345#issuecomment-468814489 # noqa: E501
    test_vars["ansible_play_host_all"] = testinfra_hosts
    templar = Templar(loader=DataLoader(), variables=test_vars)

    return templar.template(test_vars, fail_on_undefined=False)


def test_installed_site_home_page_title(host, ansible_dynamic_vars):

    # Test both that the home page loads at all, and that
    # it contains the configured site title.
    cmd = host.run('curl -s --location ' +
                   ansible_dynamic_vars['local_domain'])

    assert ('<title>Welcome to ' +
            ansible_dynamic_vars['drupal_site_name']) in cmd.stdout
