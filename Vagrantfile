# -*- mode: ruby -*-
# vi: set ft=ruby :

require_relative 'lib/drupalvm/vagrant'

# Absolute paths on the host machine.
host_drupalvm_dir = File.dirname(File.expand_path(__FILE__))
host_project_dir = ENV['DRUPALVM_PROJECT_ROOT'] || host_drupalvm_dir
host_config_dir = ENV['DRUPALVM_CONFIG_DIR'] ? "#{host_project_dir}/#{ENV['DRUPALVM_CONFIG_DIR']}" : host_project_dir

# Absolute paths on the guest machine.
guest_project_dir = '/vagrant'
guest_drupalvm_dir = ENV['DRUPALVM_DIR'] ? "/vagrant/#{ENV['DRUPALVM_DIR']}" : guest_project_dir
guest_config_dir = ENV['DRUPALVM_CONFIG_DIR'] ? "/vagrant/#{ENV['DRUPALVM_CONFIG_DIR']}" : guest_project_dir

drupalvm_env = ENV['DRUPALVM_ENV'] || 'vagrant'

default_config_file = "#{host_drupalvm_dir}/default.config.yml"
unless File.exist?(default_config_file)
  raise_message "Configuration file not found! Expected in #{default_config_file}"
end

vconfig = load_config([
  default_config_file,
  "#{host_config_dir}/config.yml",
  "#{host_config_dir}/local.config.yml",
  "#{host_config_dir}/#{drupalvm_env}.config.yml"
])

provisioner = vconfig['force_ansible_local'] ? :ansible_local : vagrant_provisioner
if provisioner == :ansible
  playbook = "#{host_drupalvm_dir}/provisioning/playbook.yml"
  config_dir = host_config_dir
else
  playbook = "#{guest_drupalvm_dir}/provisioning/playbook.yml"
  config_dir = guest_config_dir
end

# Verify version requirements.
require_ansible_version ">= #{vconfig['drupalvm_ansible_version_min']}"
Vagrant.require_version ">= #{vconfig['drupalvm_vagrant_version_min']}"

Vagrant.configure('2') do |config|
  # Set the name of the VM. See: http://stackoverflow.com/a/17864388/100134
  config.vm.define vconfig['vagrant_machine_name']

  # Networking configuration.
  config.vm.hostname = vconfig['vagrant_hostname']
  config.vm.network :private_network,
    ip: vconfig['vagrant_ip'],
    auto_network: vconfig['vagrant_ip'] == '0.0.0.0' && Vagrant.has_plugin?('vagrant-auto_network')

  unless vconfig['vagrant_public_ip'].empty?
    config.vm.network :public_network,
      ip: vconfig['vagrant_public_ip'] != '0.0.0.0' ? vconfig['vagrant_public_ip'] : nil
  end

  # SSH options.
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  # Vagrant box.
  config.vm.box = vconfig['vagrant_box']

  # Display an introduction message after `vagrant up` and `vagrant provision`.
  config.vm.post_up_message = vconfig.fetch('vagrant_post_up_message', get_default_post_up_message(vconfig))

  # If a hostsfile manager plugin is installed, add all server names as aliases.
  aliases = get_vhost_aliases(vconfig) - [config.vm.hostname]
  if Vagrant.has_plugin?('vagrant-hostsupdater')
    config.hostsupdater.aliases = aliases
  elsif Vagrant.has_plugin?('vagrant-hostmanager')
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.aliases = aliases
  end

  # Synced folders.
  vconfig['vagrant_synced_folders'].each do |synced_folder|
    options = {
      type: synced_folder.fetch('type', vconfig['vagrant_synced_folder_default_type']),
      rsync__exclude: synced_folder['excluded_paths'],
      rsync__args: ['--verbose', '--archive', '--delete', '-z', '--copy-links', '--chmod=ugo=rwX'],
      id: synced_folder['id'],
      create: synced_folder.fetch('create', false),
      mount_options: synced_folder.fetch('mount_options', []),
      use_bindfs: synced_folder.fetch('use_bindfs', false)
    }
    synced_folder.fetch('options_override', {}).each do |key, value|
      options[key.to_sym] = value
    end

    # Use vagrant-bindfs plugin if present.
    # See https://github.com/gael-ian/vagrant-bindfs
    if options[:type] == 'nfs' && options[:use_bindfs] && Vagrant.has_plugin?("vagrant-bindfs")
      guest_path = synced_folder['destination']
      host_path = File.expand_path(synced_folder['local_path'])
      config.vm.synced_folder synced_folder['local_path'], "/var/nfs#{host_path}", options
      config.bindfs.bind_folder "/var/nfs#{host_path}", guest_path,
        # These users will see themselves as the owners of all files. PHP `chmod()`
        # is only allowed by the owner of the files, so `www-data` must see itself as
        # the owner.
        # See http://php.net/manual/en/function.chmod.php#refsect1-function.chmod-notes.
        m: 'vagrant,www-data',
        g: 'www-data',
        perms: 'u=rwX:g=rwD',
        o: 'nonempty'
      config.nfs.map_uid = Process.uid
      config.nfs.map_gid = Process.gid
    else
      config.vm.synced_folder synced_folder.fetch('local_path'), synced_folder.fetch('destination'), options
    end
  end

  # Allow override of the default synced folder type.
  config.vm.synced_folder host_project_dir, '/vagrant', type: vconfig['vagrant_synced_folder_default_type']

  config.vm.provision provisioner do |ansible|
    ansible.playbook = playbook
      ansible.extra_vars = {
      config_dir: config_dir,
        drupalvm_env: drupalvm_env
      }
      # See https://www.vagrantup.com/docs/provisioning/ansible_common.html
      ansible.host_vars = {
        "#{vconfig['vagrant_machine_name']}" => {
          "ansible_ssh_extra_args" => "'-o StrictHostKeyChecking=no'",
        }
      }
      ansible.raw_arguments = ENV['DRUPALVM_ANSIBLE_ARGS']
    ansible.tags = ENV['DRUPALVM_ANSIBLE_TAGS']
  end

  # VMware Fusion.
  config.vm.provider :vmware_fusion do |v, override|
    # HGFS kernel module currently doesn't load correctly for native shares.
    override.vm.synced_folder host_project_dir, '/vagrant', type: 'nfs'

    v.gui = vconfig['vagrant_gui']
    v.vmx['memsize'] = vconfig['vagrant_memory']
    v.vmx['numvcpus'] = vconfig['vagrant_cpus']
  end

  # VirtualBox.
  config.vm.provider :virtualbox do |v|
    v.linked_clone = true if Vagrant::VERSION =~ /^1.8/
    v.name = vconfig['vagrant_hostname']
    v.memory = vconfig['vagrant_memory']
    v.cpus = vconfig['vagrant_cpus']
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    v.customize ['modifyvm', :id, '--ioapic', 'on']
    v.gui = vconfig['vagrant_gui']
  end

  # Parallels.
  config.vm.provider :parallels do |p, override|
    override.vm.box = vconfig['vagrant_box']
    p.name = vconfig['vagrant_hostname']
    p.memory = vconfig['vagrant_memory']
    p.cpus = vconfig['vagrant_cpus']
    p.update_guest_tools = true
  end

  # Cache packages and dependencies if vagrant-cachier plugin is present.
  if Vagrant.has_plugin?('vagrant-cachier')
    config.cache.scope = :box
    config.cache.auto_detect = false
    config.cache.enable :apt
    config.cache.enable :generic, {
      # Composer cache bin.
      "composer" => { cache_dir: '/home/vagrant/.composer/cache' },
      # PHP downloads / source files cache bin.
      "php#{vconfig['php_version']}-workspace" => { cache_dir: "/root/php#{vconfig['php_version']}" },
      # Vagrant user generic cache bin.
      "generic" => { cache_dir: '/home/vagrant/.cache' },
    }
    config.cache.synced_folder_opts = {
      type: vconfig['vagrant_synced_folder_default_type']
    }
  end

  # Allow an untracked Vagrantfile to modify the configurations
  [host_config_dir, host_project_dir].uniq.each do |dir|
    eval File.read "#{dir}/Vagrantfile.local" if File.exist?("#{dir}/Vagrantfile.local")
  end
end
