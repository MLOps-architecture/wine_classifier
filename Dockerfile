FROM prefecthq/prefect:latest

COPY . /tmp/wine_classifier
RUN pip install -e /tmp/wine_classifier