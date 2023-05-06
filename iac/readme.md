# Vagrant Ubuntu VM

This Vagrantfile sets up an Ubuntu 20.04 LTS (Focal Fossa) virtual machine using Vagrant and VirtualBox.
The VM is configured with 8 GB of RAM and 4 CPU cores.

Additionally, the VM is set up with the Xfce desktop environment and xrdp to allow remote desktop connections.

## Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- - A remote desktop client like [Microsoft Remote Desktop](https://www.microsoft.com/en-us/p/microsoft-remote-desktop) or [Remmina](https://remmina.org/)

## Getting Started

1. Copy the Vagrantfile into a new directory.
2. Open a terminal or command prompt and navigate to the directory containing the Vagrantfile.
3. Run `vagrant up` to start the virtual machine. This command will download the `ubuntu/jammy64` base box if it's not already on your system. It might take a few minutes to complete.

## VM Configuration

The VM is configured with the following settings:

- Name: UbuntuVM
- Memory: 8 GB
- CPU cores: 4
- Remote Desktop Protocol (RDP) port: Host port 3389 forwarded to guest port 3389

Additionally, a shell script is used to provision the VM, installing the following packages:

- `software-properties-common`
- Ansible (via the official PPA)
- Xfce desktop environment (`xfce4`, `xfce4-goodies`)
- xrdp

This Vagrantfile uses Ansible as the provisioner to run the main playbook located at `provisioning/main.yml`.

Ansible is configured to run in compatibility mode "auto", which means it will try to detect the version of Ansible installed on the host and use the appropriate syntax.

To customize the VM settings, you can edit the Vagrantfile and adjust the values within the `config.vm.provider "virtualbox"` block.

## Accessing the VM

After the VM has started, you can access it by running `vagrant ssh` in the terminal. This will open an SSH session to the VM.

### Remote Desktop

Once the VM is up and running, you can connect to it using a remote desktop client by entering `localhost:3389` or `127.0.0.1:3389` as the address.

When prompted, enter the username and password of a valid account on the guest VM.

By default, you can use the "vagrant" user with the password "vagrant" or the custom password you set in the Vagrantfile.

## Stopping and Deleting the VM

To stop the VM without deleting it, run `vagrant halt`. To completely delete the VM and free up disk space, run `vagrant destroy`.

For more information about Vagrant and its available commands, please refer to the [official documentation](https://docs.vagrantup.com).
