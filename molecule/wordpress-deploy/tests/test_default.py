import os

import pytest
import re
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
    cmd = host.run('curl -s ' +
                   ansible_dynamic_vars['local_domain'])

    assert '<title>' + ansible_dynamic_vars['wp_site_title'] in cmd.stdout


def test_db_search_replace(host, ansible_dynamic_vars):

    cmd = host.run('curl -s --location ' +
                   ansible_dynamic_vars['local_domain'] +
                   '/test-page')

    assert ('search-replace test 1: http://' +
            ansible_dynamic_vars['local_domain']) in cmd.stdout

    assert ('search-replace test 2: https://' +
            ansible_dynamic_vars['local_domain']) in cmd.stdout

    assert ('search-replace test 3: http://' +
            ansible_dynamic_vars['local_domain']) in cmd.stdout

    assert ('search-replace test 4: https://' +
            ansible_dynamic_vars['local_domain']) in cmd.stdout


def test_missing_files_redirect_present(host, ansible_dynamic_vars):

    # Check status code for the `is-there.png` file.
    cmd = host.run('curl -s --head ' +
                   ansible_dynamic_vars['local_domain'] +
                   '/wp-content/uploads/is-there.png')

    assert re.match('HTTP.*?200 OK', cmd.stdout)


def test_missing_files_redirect_not_present(host, ansible_dynamic_vars):

    cmd = host.run('curl -s --head ' +
                   ansible_dynamic_vars['local_domain'] +
                   '/wp-content/uploads/not-there.png')

    assert re.match('HTTP.*?302 Found', cmd.stdout)
    assert (ansible_dynamic_vars['prod_domain'] +
            '/wp-content/uploads/not-there.png') in cmd.stdout
