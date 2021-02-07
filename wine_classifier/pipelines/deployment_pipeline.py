import yaml
from os import path
from prefect import task
from kubernetes import client, config


@task()
def deploy_model(model_uri: str, namespace: str = "default"):

    config.load_incluster_config()
    v1 = client.CoreV1Api()

    with open(
        path.join(path.dirname(__file__), "../deployment/seldon-deployment.yaml")
    ) as f:
        dep = yaml.safe_load(f)
        dep["spec"]["predictors"][0]["graph"]["modelUri"] = model_uri

        resp = v1.create_namespaced_deployment(body=dep, namespace=namespace)
        print("Deployment created. status='%s'" % resp.metadata.name)
