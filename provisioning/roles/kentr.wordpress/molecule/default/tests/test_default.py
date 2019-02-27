import os

import pytest
import stat
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
        ("file=../../defaults/main.yml"
         " name=role_defaults"))["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        ("file=../../vars/main.yml"
         " name=role_vars"))["ansible_facts"]["role_vars"])

    ansible_vars.update(host.ansible(
        "include_vars",
        ("file=../resources/prepare-vars.yml"
         " name=prepare_vars"))["ansible_facts"]["prepare_vars"])

    ansible_vars.update(host.ansible(
        "include_vars",
        ("file=./scenario-vars.yml"
         " name=scenario_vars"))["ansible_facts"]["scenario_vars"])

    return ansible_vars


def test_wp_config_file_exists(host, ansible_role_vars):
    f = host.file(ansible_role_vars['wp_install_dir'] + '/wp-config.php')

    assert f.exists

    # Verify file group.
    assert f.group == ansible_role_vars['wp_core_group']

    # Verify that group has read permission.
    assert bool(f.mode & stat.S_IRGRP)


def test_wp_config_file_contains_salts(host, ansible_role_vars):
    f = host.file(ansible_role_vars['wp_install_dir'] + '/wp-config.php')

    assert f.contains("^define(\s*'AUTH_KEY'")


def test_wp_config_file_contains_db_credentials(host, ansible_role_vars):
    f = host.file(ansible_role_vars['wp_install_dir'] + '/wp-config.php')

    assert f.contains((
        "^define('DB_NAME',\s*'"
        + ansible_role_vars['wp_db_name']
        + "');"
        ))
    assert f.contains((
        "^define('DB_USER',\s*'"
        + ansible_role_vars['wp_db_user']
        + "');"
        ))
    assert f.contains((
        "^define('DB_PASSWORD',\s*'"
        + ansible_role_vars['wp_db_password']
        + "');"
        ))
    assert f.contains((
        "^define('DB_HOST',\s*'"
        + ansible_role_vars['wp_db_host']
        + "');"
        ))


def test_wp_config_file_contains_db_table_prefix(host, ansible_role_vars):
    f = host.file(ansible_role_vars['wp_install_dir'] + '/wp-config.php')

    assert f.contains((
        "^$table_prefix\s*=\s*'"
        + ansible_role_vars['wp_table_prefix']
        + "';"
        ))
