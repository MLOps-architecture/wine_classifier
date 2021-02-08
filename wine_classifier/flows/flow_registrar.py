import click
from wine_classifier import config
from prefect import Parameter, Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GitHub, S3
import mlflow

from wine_classifier.pipelines.train_pipeline import fetch_data, train_model
from wine_classifier.pipelines.deployment_pipeline import deploy_model


mlflow.set_tracking_uri("http://mlflow.datarevenue.com:5000")


def wine_classifier_train_pipeline():
    custom_confs = {
        "run_config": KubernetesRun(
            image="drtools/prefect:wine-classifier-3", labels=["stage"]
        ),
        "storage": S3("dr-bucket"),
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
        "storage": S3("dr-bucket")
    }

    with Flow("model-deployment-pipeline", **custom_confs,) as flow:
        model_uri = Parameter("model_uri", default=config["model"]["modelUri"])
        environment = Parameter("environment", default=config["model"]["environment"])

        deploy_model(model_uri=model_uri, namespace=environment)

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


@cli.command(name="register-all-flows")
def deploy_model_cli():
    model_deployment_pipeline()
    wine_classifier_train_pipeline()


if __name__ == "__main__":
    github_flow()
