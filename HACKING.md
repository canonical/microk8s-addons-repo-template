# Develop a new MicroK8s addon

This document describes the process of developing a new addon for MicroK8s. As an example, we will create a simple addon `python-hello-k8s`, which creates a simple nginx deployment on our cluster.

## Overview

- [Develop a new MicroK8s addon](#develop-a-new-microk8s-addon)
  - [Overview](#overview)
  - [Develop addon](#develop-addon)
    - [1. Add entry in `addons.yaml`](#1-add-entry-in-addonsyaml)
    - [2. Write the `enable` script](#2-write-the-enable-script)
    - [3. Write the `disable` script](#3-write-disable-script)
    - [4. Write unit tests](#4-write-unit-tests)
  - [Use the addon](#use-addon)


## Develop addon

### 1. Add entry in `addons.yaml`

Edit [`addons.yaml`](./addons.yaml) in the root of this repository and add an entry for your new addon. See the expected format and the list of supported fields in [`README.md`](./README.md).

For our `python-hello-k8s` addon, would look like this:

```yaml
microk8s-addons:
  addons:
    - name: "python-hello-k8s"
      description: "Demo addon implemented in python"
      version: "1.0.0"
      check_status: "deployment.apps/python-demo-nginx"
      supported_architectures:
        - arm64
        - amd64
        - s390x
```

### 2. Write the `enable` script

The `enable` script is called when running `microk8s enable python-hello-k8s`.

Create an empty directory `addons/python-hello-k8s`, then create `addons/python-hello-k8s/enable`. The `enable` script can be written in either Python or Bash, and even supports command-line arguments. It is highly recommended to avoid Bash if any non-trivial amount of work is required for your addon.

For our simple addon, we only need to create a deployment with `nginx`. We will support an optional command-line parameter `--replicas`, which will allow users to configure the number of replicas when enabling the addon.

In the example below, we use [Click](https://click.palletsprojects.com/en/8.0.x/) for simplicity.

```python
#!/usr/bin/env python3
# addons/python-hello-k8s/enable

import os
import subprocess

import click

KUBECTL = os.path.expandvars("$SNAP/microk8s-kubectl.wrapper")

@click.command()
@click.option("--replicas", required=False, default=3, type=int)
def main(replicas):
    click.echo("Enabling python-hello-k8s")
    subprocess.check_call([
        KUBECTL, "create", "deploy", "python-demo-nginx", "--image", "nginx", "--replicas", str(replicas),
    ])
    click.echo("Enabled python-hello-k8s")

if __name__ == "__main__":
    main()
```

Make sure that the script is executable:

```bash
chmod +x ./addons/python-demo-nginx/enable
```

### 3. Write the `disable` script

The `disable` script is called when running `microk8s disable python-demo-nginx`.

```python
import click
import os
import subprocess

KUBECTL = os.path.expandvars("$SNAP/microk8s-kubectl.wrapper")

@click.command()
def main():
    click.echo("Disabling python-demo-nginx")
    subprocess.check_call([
        KUBECTL, "delete", "deploy", "python-demo-nginx"
    ])
    click.echo("Disabled python-demo-nginx")

if __name__ == "__main__":
    main()
```

Like previously, make sure the script is executable:

```bash
chmod +x ./addons/python-demo-nginx/disable
```

### 4. Write unit tests

Testing the `python-hello-k8s` addon is found in the `tests/test-addons.py` file. With the help of a few helper functions in `tests/utils.py` we are able to 
  - enable the addon 
  - wait for the nginx pods to come online
  - the status of the addon
  - disable the addon

```python
import sh
import yaml

from utils import (
    microk8s_enable,
    wait_for_pod_state,
    microk8s_disable,
)

class TestAddons(object):
    def test_python_demo_nginx(self):
        microk8s_enable("python-hello-k8s")
        wait_for_pod_state("", "default", "running", label="app=python-demo-nginx")
        status = yaml.safe_load(sh.microk8s.status(format="yaml").stdout)
        expected = {"python-hello-k8s": "enabled"}
        microk8s_disable("python-hello-k8s")
```

To triggering the tests is with `pytest` and have to be called after the repository is added in a MicroK8s cluster:
```
$ pytest -s ./tests/test-addons.py 
====================== test session starts ========================================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/jackal/workspace/microk8s-addons-repo-template
collected 1 item                                                                                                                                                                                                                                                              

tests/test-addons.py Infer repository demo for addon python-hello-k8s
Infer repository demo for addon python-hello-k8s
.

====================== 1 passed in 12.42s =========================================
jackal@aurora:~/workspace/microk8s-addons-repo-template$ 
```



## Use the addon

Install MicroK8s, then add the repository using `mcirok8s addons repo` as shown in the [README.md](./README.md).

Then, enable the addon with:

```bash
# simple ...
microk8s enable python-hello-k8s
# ... or, with command-line arguments
microk8s enable python-hello-k8s --replicas 5
```

You can check the status of the addon with the `microk8s status` command:

```bash
microk8s status --addon python-hello-k8s
```

And disable the addon:

```bash
microk8s disable python-hello-k8s
```
