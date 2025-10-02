Bastion Provisioner
=========

This Ansible role installs a set of common system packages required to prepare a machine for **Continuous Integration (CI)** tasks.


It is designed specifically to **prepare and configure the machine as a GitHub Actions self-hosted runner**, enabling it to build Docker images, run automated jobs, and support typical CI workloads.

- Building Docker images
- Running automation and testing tasks
- Acting as a **GitHub Actions self-hosted runner**

It installs essential tools like Docker, Git, system utilities, and common build dependencies.


## Packages Installed

By default, the role installs the following packages (configurable in `defaults/main.yml`):

- `docker.io`
- `docker-compose`
- `git`
- `curl`
- `wget`
- `unzip`, `zip`
- `ca-certificates`
- `apt-transport-https`
- `software-properties-common`
- `make`
- `build-essential`
- `python3`
- `jq`
- `lsb-release`

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

The following variables are used in this role. Some are configurable by the user (defined in `defaults/main.yml`), and others are internal to the role (defined in `vars/main.yml`).
### Variable: `ci_common_packages`
- **Defined in**: `defaults/main.yml`
- **Type**: `list`
- **Required**: no
- **Allowed values**:  
  A list of package names (e.g., `docker.io`, `git`, etc.)

### Variable: `github_runner_release_url`
- **Defined in**: `defaults/main.yml`
- **Type**: `string`
- **Required**: yes
- **Allowed values**:  
  Release url to get the github runner binary

### Variable: `github_runner_user_name`
- **Defined in**: `defaults/main.yml`
- **Type**: `string`
- **Required**: no
- **Allowed values**:  
  User name that github software will use while it is executed

### Variable: `github_runner_group_name`
- **Defined in**: `defaults/main.yml`
- **Type**: `string`
- **Required**: no
- **Allowed values**:  
  Group name that github software will use while it is executed

### Variable: `github_personal_access_token`
- **Defined in**: `defaults/main.yml`
- **Type**: `string`
- **Required**: yes
- **Allowed values**:  
  Github personal acces token to link the runner with the desired repo.Must be defined via vault
  

### Variable: `github_repo_url`
- **Defined in**: `defaults/main.yml`
- **Type**: `string`
- **Required**: yes
- **Allowed values**:  
  Github repo url to link the worker with

### Variable: `github_runner_name`
- **Defined in**: `defaults/main.yml`
- **Type**: `string`
- **Required**: yes
- **Allowed values**:  
  Github runner name to assign the bastion

### Variable: `github_runner_labels`
- **Defined in**: `defaults/main.yml`
- **Type**: `list`
- **Required**: yes
- **Allowed values**:  
  Github labels to add to the runner

### Variable: `ci_common_packages`
- **Defined in**: `vars/main.yml`
- **Type**: `list`
- **Allowed values**: List of package names (e.g., `docker.io`, `git`, etc.)
- **Default value**:
  ```yaml
  ci_common_packages:
    - docker.io
    - docker-compose
    - git
    - curl
    - wget
    - unzip
    - zip
    - ca-certificates
    - apt-transport-https
    - software-properties-common
    - make
    - build-essential
    - python3
    - python3-pip
    - jq
    - lsb-release

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
