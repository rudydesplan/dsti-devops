# Vagrant Ubuntu VM

This Vagrantfile sets up an Ubuntu 20.04 LTS (Focal Fossa) virtual machine using Vagrant and VirtualBox.
The VM is configured with 8 GB of RAM and 4 CPU cores.

## Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Getting Started

1. Copy the Vagrantfile into a new directory.
2. Open a terminal or command prompt and navigate to the directory containing the Vagrantfile.
3. Run `vagrant up` to start the virtual machine. This command will download the `ubuntu/focal64` base box if it's not already on your system. It might take a few minutes to complete.

## VM Configuration

The VM is configured with the following settings:

- Name: UbuntuVM
- Memory: 8 GB
- CPU cores: 4

Additionally, a shell script is used to provision the VM, installing the following packages:

- `software-properties-common`
- Ansible (via the official PPA)

To customize the VM settings, you can edit the Vagrantfile and adjust the values within the `config.vm.provider "virtualbox"` block.

## Accessing the VM

After the VM has started, you can access it by running `vagrant ssh` in the terminal. This will open an SSH session to the VM.

## Stopping and Deleting the VM

To stop the VM without deleting it, run `vagrant halt`. To completely delete the VM and free up disk space, run `vagrant destroy`.

For more information about Vagrant and its available commands, please refer to the [official documentation](https://docs.vagrantup.com).
