import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Define fixture for dynamic ansible role variables.
# @see https://github.com/philpep/testinfra/issues/345#issuecomment-409999558
@pytest.fixture
def ansible_role_vars(host):

    # Include variables from ansible variable files.
    # Paths are relative to the scenario directory.
    ansible_vars = host.ansible(
        "include_vars",
        ("file=../../default.config.yml"
         " name=default_config"))["ansible_facts"]["default_config"]

    ansible_vars.update(host.ansible(
        "include_vars",
        ("file=../../config.yml"
         " name=config"))["ansible_facts"]["config"])

    ansible_vars.update(host.ansible(
        "include_vars",
        ("file=../resources/prepare-vars.yml"
         " name=prepare_vars"))["ansible_facts"]["prepare_vars"])

    ansible_vars.update(host.ansible(
        "include_vars",
        ("file=../../local.config.yml"
         " name=local_config"))["ansible_facts"]["local_config"])

    return ansible_vars


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
