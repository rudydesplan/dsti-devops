# Ansible Playbook for Flask API Deployment

This Ansible playbook sets up and deploys a Flask API application on an Ubuntu-based virtual machine using Gunicorn.

## Getting Started

### Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### Directory Structure

In your project directory (where the Vagrantfile is located), create a new directory named `provisioning`:

mkdir provisioning

### Copy the Ansible Playbook

Inside the `provisioning` directory, copy the `main.yml` file. This file will contain the Ansible playbook that describes the tasks to be executed on the VM.

### Update the Vagrantfile

Update your Vagrantfile to use Ansible as a provisioner. Add the following lines before the `end` keyword:

```ruby
config.vm.provision "ansible" do |ansible|
  ansible.playbook = "provisioning/main.yml"
  ansible.compatibility_mode = "auto"
end
```

### Synced Folder (Optional)
Set up a synced folder in your Vagrantfile to share your application files between your host machine and the VM. Add the following line in the Vagrantfile before the `end` keyword:

```ruby
config.vm.synced_folder "path/to/your/app", "/vagrant"
```

Replace `path/to/your/app` with the relative or absolute path to your application files on your host machine.

### Playbook Tasks
The Ansible Playbook performs the following tasks on the virtual machine:

1.Update the package list.

2.Install Python, pip, and git.

3.Clone the Flask API repository from GitHub.

4.Install dependencies from `requirements.txt`.

5.Install Gunicorn.

6.Start the Flask application using Gunicorn.

7.Install `httplib2` for Ansible uri module.

8.Check the health of the Flask API.

9.Display health check results.

### Deployment
To deploy the Flask API, run `vagrant up` from your project directory. This will start the virtual machine and execute the Ansible Playbook tasks.

After deployment, you can access the Flask API on your virtual machine at `http://0.0.0.0:5000`.

To view the health check results, log into the virtual machine using `vagrant ssh` and inspect the Ansible output.
