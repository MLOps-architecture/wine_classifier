import prefect
from prefect import task, Flow, Parameter
from prefect.run_configs import KubernetesRun
from prefect.storage import GitHub
import logging

from wine_classifier import config

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


@task
def github_storage_task(model, namespace):
    logger = prefect.context.get("logger")
    logger.info(model)
    logger.info(namespace)


def main():
    custom_confs = {
        "run_config": KubernetesRun(image="drtools/prefect:wine-classifier-4",),
        "storage": GitHub(
            repo="datarevenue-berlin/wine_classifier",
            path="wine_classifier/pipelines/github.py",
        ),
    }
    with Flow("github", **custom_confs,) as flow:
        model_uri = Parameter("model_uri", default=config["model"]["modelUri"])
        environment = Parameter("environment", default=config["model"]["environment"])

        github_storage_task(model=model_uri, namespace=environment)

    flow.register(project_name="mlops-demo")


if __name__ == "__main__":
    main()
