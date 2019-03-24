import os

import pytest
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Define fixture for dynamic ansible role variables.
@pytest.fixture
def ansible_role_vars(host):

    # Include variables from ansible variable files.
    # Paths are relative to the scenario directory.
    # `test_test_variable_files` is declared in `base-config.yml`,
    # under the `all` group.
    vars_files = host.ansible.get_variables()['test_variable_files']

    for file in vars_files:
        host.ansible(
            "include_vars",
            "file=" + file)

    return host.ansible.get_variables()


def test_installed_site_home_page_title(host, ansible_role_vars):

    # Test both that the home page loads at all, and that
    # it contains the configured site title.
    cmd = host.run('curl -s ' +
                   ansible_role_vars['local_domain'])

    assert '<title>' + ansible_role_vars['wp_site_title'] in cmd.stdout


def test_db_search_replace(host, ansible_role_vars):

    cmd = host.run('curl -s --location ' +
                   ansible_role_vars['local_domain'] +
                   '/test-page')

    assert ('search-replace test 1: http://' +
            ansible_role_vars['local_domain']) in cmd.stdout

    assert ('search-replace test 2: https://' +
            ansible_role_vars['local_domain']) in cmd.stdout

    assert ('search-replace test 3: http://' +
            ansible_role_vars['local_domain']) in cmd.stdout

    assert ('search-replace test 4: https://' +
            ansible_role_vars['local_domain']) in cmd.stdout


def test_missing_files_redirect_present(host, ansible_role_vars):

    # Check status code for the `is-there.png` file.
    cmd = host.run('curl -s --head ' +
                   ansible_role_vars['local_domain'] +
                   '/wp-content/uploads/is-there.png')

    assert re.match('HTTP.*?200 OK', cmd.stdout)


def test_missing_files_redirect_not_present(host, ansible_role_vars):

    cmd = host.run('curl -s --head ' +
                   ansible_role_vars['local_domain'] +
                   '/wp-content/uploads/not-there.png')

    assert re.match('HTTP.*?302 Found', cmd.stdout)
    assert (ansible_role_vars['prod_domain'] +
            '/wp-content/uploads/not-there.png') in cmd.stdout
