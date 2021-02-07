from prefect import Parameter, Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import S3
import mlflow

from wine_classifier.train_pipeline import fetch_data, train_model

mlflow.set_tracking_uri("http://mlflow.datarevenue.com:5000")

def wine_classifier_train_pipeline():
    custom_confs = {
        "run_config": KubernetesRun(
            image="drtools/prefect:wine-classifier-2", 
            labels=["stage"]
        ),   
        "storage": S3(bucket="dr-prefect"),

    } 
    with Flow("wine-classifier-train-pipeline", **custom_confs, ) as flow:
        in_alpha = Parameter("in_alpha", default=0.5)
        in_l1_ratio = Parameter("in_l1_ratio", default=0.5)

        data = fetch_data()
        train_model(data, mlflow_experiment_id=1, in_alpha=in_alpha, in_l1_ratio=in_l1_ratio)


    flow.register(project_name="mlops-demo")


if __name__ == "__main__":
    main()

