import sh
import yaml

from utils import microk8s_enable, wait_for_pod_state, microk8s_disable


class TestAddons(object):
    def test_python_demo_nginx(self):
        microk8s_enable("python-hello-k8s")
        wait_for_pod_state("", "default", "running", label="app=python-demo-nginx")
        status = yaml.safe_load(sh.microk8s.status(format="yaml").stdout)
        expected = {"python-hello-k8s": "enabled"}
        microk8s_disable("python-hello-k8s")
