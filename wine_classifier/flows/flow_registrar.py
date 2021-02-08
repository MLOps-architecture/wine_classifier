import click
from wine_classifier import config
from prefect import Parameter, Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GitHub, Local
import mlflow

from wine_classifier.pipelines.train_pipeline import fetch_data, train_model
from wine_classifier.pipelines.deployment_pipeline import deploy_model


mlflow.set_tracking_uri("http://mlflow.datarevenue.com:5000")

FLOW_GITHUB_STORAGE = GitHub(
    repo="datarevenue-berlin/wine_classifier",
    path="wine_classifier/flows/flow_registrar.py",
)


def wine_classifier_train_pipeline():
    custom_confs = {
        "run_config": KubernetesRun(
            image="drtools/prefect:wine-classifier-3", labels=["stage"]
        ),
        "storage": FLOW_GITHUB_STORAGE,
    }
    with Flow("wine-classifier-train-pipeline", **custom_confs,) as flow:
        in_alpha = Parameter("in_alpha", default=0.5)
        in_l1_ratio = Parameter("in_l1_ratio", default=0.5)

        data = fetch_data()
        train_model(
            data, mlflow_experiment_id=1, in_alpha=in_alpha, in_l1_ratio=in_l1_ratio
        )

    flow.register(project_name="mlops-demo")


def model_deployment_pipeline():

    custom_confs = {
        "run_config": KubernetesRun(
            image="drtools/prefect:wine-classifier-3",
            # labels=[environment],
            service_account_name="prefect-deployment-sa",
        ),
        "storage": FLOW_GITHUB_STORAGE
    }

    with Flow("model-deployment-pipeline", **custom_confs,) as flow:
        model_uri = Parameter("model_uri", default=config["model"]["modelUri"])
        environment = Parameter("environment", default=config["model"]["environment"])

        deploy_model(model_uri=model_uri, namespace=environment)

    flow.register(project_name="mlops-demo")


def github_flow():

    import prefect

    @prefect.task
    def github_storage_task(model, namespace):
        logger = prefect.context.get("logger")
        logger.info(model)
        logger.info(namespace)

    custom_confs = {
        "run_config": KubernetesRun(
            image="drtools/prefect:wine-classifier-3",
            # labels=[environment],
        ),
        "storage": FLOW_GITHUB_STORAGE
    }

    with Flow("github", **custom_confs,) as flow:
        model_uri = Parameter("model_uri", default=config["model"]["modelUri"])
        environment = Parameter("environment", default=config["model"]["environment"])

        github_storage_task(model=model_uri, namespace=environment)

    flow.register(project_name="mlops-demo")


@click.group()
def cli():
    pass


@cli.command(name="register-train-pipeline")
def register_train_pipeline_cli(*args, **kwargs):
    wine_classifier_train_pipeline(*args, **kwargs)


@cli.command(name="register-model-deployment")
def deploy_model_cli(*args, **kwargs):
    model_deployment_pipeline(*args, **kwargs)


@cli.command(name="github")
def deploy_model_cli(*args, **kwargs):
    github_flow(*args, **kwargs)


@cli.command(name="register-all-flows")
def deploy_model_cli():
    model_deployment_pipeline()
    wine_classifier_train_pipeline()


if __name__ == "__main__":
    cli()
