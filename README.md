## Your repository

A MicroK8s addons repository should have a comprehensive description of the addons collection it includes. The current template repository contains two addons:

  * bash-hello-k8s, a demo addon implemented in bash
  * python-hello-k8s, a python based demo addon

The purpose of the addons should be clearly stated. In this demo repository our goal is to demonstrate how addons are structured so as to can guide you in your first steps as an addons author.


### How to use an addons repository

#### Adding repositories
3rd party addons repositories are supported on MicroK8s v1.24 and onwards. To add a repository on an already installed MicroK8s you have to use the `microk8s addons repo` command and provide a user friendly repo name, the path to the repository and optionally a branch within the repository. For example:
```
microk8s addons repo add demo https://github.com/canonical/microk8s-addons-repo-template --reference main
```

As long as you have a local copy of a repository and that repository is also a git one in can also be added to a MicroK8s installation with:
```
microk8s.addons repo add demo ./microk8s-addons-repo-template
```

#### Enabling/disabling addons

The addons of all repositories are shown in `microk8s status` along with the repo they came from. `microk8s enable` and `microk8s disable` are used to enable and disable the addons respectively. The repo name can be used to disambiguate between addons with the same name. For example:

```
microk8s enable demo/bash-hello-k8s
```

#### Refreshing repositories

Adding a repository to MicroK8s (via `mcirok8s addons repo add`) creates a copy of the repository under `$SNAP_COMMON/addons` (typically under `/var/snap/microk8s/common/addons/`). Authorized users are able to edit the addons to match their need. In case the upstream repository changes and you need to pull in any updates with:
```
microk8s addons repo update <repo_name>
```

#### Removing repositories

Removing repositories is done with:
```
microk8s addons repo remove <repo_name>
```


### Repository structure

An addons repository has the following structure:

```
addons.yaml         Authoritative list of addons included in this repository. See format below.
addons/
    <addon1>/
        enable      Executable script that runs when enabling the addon
        disable     Executable script that runs when disabling the addon
    <addon2>/
        enable
        disable
    ...
```

At the root of the addons repository the `addons.yaml` file lists all the addons included. This file is of the following format:

```yaml
microk8s-addons:
  # A short description for the addons in this repository.
  description: Core addons of the MicroK8s project

  # Revision number. Increment when there are important changes.
  revision: 1

  # List of addons.
  addons:
    - name: addon1
      description: My awesome addon

      # Addon version.
      version: "1.0.0"

      # Test to check that addon has been enabled. This may be:
      # - A path to a file. For example, "${SNAP_DATA}/var/lock/myaddon.enabled"
      # - A Kubernetes resource, in the form `resourceType/resourceName`, just
      #   as it would appear in the output of the `kubectl get all -A` command.
      #   For example, "deployment.apps/registry".
      #
      # The addon is assumed to be enabled when the specified file or Kubernetes
      # resource exists.
      check_status: "deployment.apps/addon1"

      # List of architectures supported by this addon.
      # MicroK8s supports "amd64", "arm64" and "s390x".
      supported_architectures:
        - amd64
        - arm64
        - s390x

    - name: addon2
      description: My second awesome addon, supported for amd64 only
      version: "1.0.0"
      check_status: "pod/addon2"
      supported_architectures:
        - amd64
```

## Adding new addons

See [`HACKING.md`](./HACKING.md) for instructions on how to develop custom MicroK8s addons.
