In your project directory (where the Vagrantfile is located), create a new directory named provisioning:

Inside the provisioning directory, copy the file named main.yml. 
This file will contain the Ansible playbook that describes the tasks to be executed on the VM:

Update your Vagrantfile to use Ansible as a provisioner. 
Add the following lines before the end keyword:

config.vm.provision "ansible" do |ansible|
  ansible.playbook = "provisioning/main.yml"
  ansible.compatibility_mode = "auto"
end

(Optional) Set up a synced folder in your Vagrantfile to share your application files between your host machine and the VM. 
Add the following line in the varant file before the end keyword:

config.vm.synced_folder "path/to/your/app", "/vagrant"

Replace path/to/your/app with the relative or absolute path to your application files on your host machine.
