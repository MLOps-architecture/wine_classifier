import yaml
import prefect
from prefect import task
from kubernetes import client, config

seldon_deployment = """
    apiVersion: machinelearning.seldon.io/v1alpha2
    kind: SeldonDeployment
    metadata:
      name: wines-classifier
    spec:
      predictors:
      - graph:
          children: []
          implementation: MLFLOW_SERVER
          modelUri: dummy
          name: wines-classifier
        name: model-a
        replicas: 1
        traffic: 100
        componentSpecs:
        - spec:
            # We are setting high failureThreshold as installing conda dependencies
            # can take long time and we want to avoid k8s killing the container prematurely
            containers:
            - name: wines-classifier
              livenessProbe:
                initialDelaySeconds: 60
                failureThreshold: 100
                periodSeconds: 5
                successThreshold: 1
                httpGet:
                  path: /health/ping
                  port: http
                  scheme: HTTP
              readinessProbe:
                initialDelaySeconds: 60
                failureThreshold: 100
                periodSeconds: 5
                successThreshold: 1
                httpGet:
                  path: /health/ping
                  port: http
                  scheme: HTTP

"""

CUSTOM_RESOURCE_INFO = dict(
    group="machinelearning.seldon.io", version="v1alpha2", plural="seldondeployments",
)


@task
def deploy_model(model_uri: str, namespace: str = "default"):
    logger = prefect.context.get("logger")

    logger.info(f"Deploying model {model_uri} to enviroment {namespace}")

    config.load_incluster_config()
    custom_api = client.CustomObjectsApi()

    dep = yaml.safe_load(seldon_deployment)
    dep["spec"]["predictors"][0]["graph"]["modelUri"] = model_uri

    try:
        resp = custom_api.create_namespaced_custom_object(
            **CUSTOM_RESOURCE_INFO, namespace=namespace, body=dep,
        )

        logger.info("Deployment created. status='%s'" % resp["status"]["state"])
    except:
        logger.info("Updating existing model")
        existent_deployment = custom_api.get_namespaced_custom_object(
            **CUSTOM_RESOURCE_INFO, namespace=namespace, name=dep["metadata"]["name"],
        )
        existent_deployment["spec"]["predictors"][0]["graph"]["modelUri"] = model_uri

        resp = custom_api.replace_namespaced_custom_object(
            **CUSTOM_RESOURCE_INFO,
            namespace=namespace,
            name=existent_deployment["metadata"]["name"],
            body=existent_deployment,
        )

    # TODO: wait to become available

