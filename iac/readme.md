# Vagrant Ubuntu VM

This Vagrantfile sets up an Ubuntu 20.10 (Groovy Gorilla) virtual machine using Vagrant and VMware Desktop.
The VM is configured with 2 GB of RAM and 2 CPU cores.

Additionally, the VM is set up with the GNOME desktop environment and xrdp to allow remote desktop connections.

## Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads)
- VMware Desktop and utilities ( https://developer.hashicorp.com/vagrant/docs/providers/vmware/installation )
- A remote desktop client like [Microsoft Remote Desktop](https://www.microsoft.com/en-us/p/microsoft-remote-desktop) or [Remmina](https://remmina.org/)

## Getting Started

1. Copy the Vagrantfile into a new directory.
2. Open a terminal or command prompt and navigate to the directory containing the Vagrantfile.
3. Run `vagrant up` to start the virtual machine. This command will download the `generic/ubuntu2010` base box if it's not already on your system.
It might take a few minutes to complete.

## VM Configuration

The VM is configured with the following settings:

- Name: AvocadoVM
- Memory: 2 GB
- CPU cores: 2
- Remote Desktop Protocol (RDP) port: Host port 3389 forwarded to guest port 3389

Additionally, a shell script is used to provision the VM, installing the following packages:

- `software-properties-common`
- Ansible (via the official PPA)
- GNOME desktop environment (ubuntu-desktop)
- Python 3 (python3-apt, python3-pip)
- Firefox
- xrdp

This Vagrantfile uses Ansible as the provisioner to run the main playbook located at `provisioning/main.yml`.

Ansible is configured to run in compatibility mode "auto", which means it will try to detect the version of Ansible installed on the host and use the appropriate syntax.

To customize the VM settings, you can edit the Vagrantfile and adjust the values within the `config.vm.provider "vmware_desktop"` block.

## Accessing the VM

After the VM has started, you can access it by running `vagrant ssh` in the terminal. This will open an SSH session to the VM.

### Remote Desktop

Once the VM is up and running, you can connect to it using a remote desktop client by entering `localhost:3389` or `127.0.0.1:3389` as the address.

When prompted, enter the username and password of a valid account on the guest VM.

By default, you can use the "vagrant" user with the password "vagrant" or the custom password you set in the Vagrantfile.

## Stopping and Deleting the VM

To stop the VM without deleting it, run `vagrant halt`. To completely delete the VM and free up disk space, run `vagrant destroy`.

For more information about Vagrant and its available commands, please refer to the [official documentation](https://docs.vagrantup.com).
