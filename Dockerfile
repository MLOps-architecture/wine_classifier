FROM drtools/drtools:latest
USER root

# Add docker so controller is able to access host docker engine
# you might want to move this command to a separate Dockerfile
# to keep image size minimal
RUN apk --update add docker


# Copy over requirements and install them
COPY requirements.txt /home/drtools/requirements.txt
RUN pip install -r /home/drtools/requirements.txt && \
    rm /home/drtools/requirements.txt

# Copy over repository and install
COPY . /home/drtools/awesome_ml
RUN pip install --no-deps -e /home/drtools/awesome_ml

# Copy configurations into place if needed

COPY conf/dask-config.yml /home/drtools/.dask/config.yml
COPY conf/luigi-logging.cfg /etc/luigi/luigi-logging.cfg
COPY conf/luigi.cfg /etc/luigi/client.cfg

RUN chown -R drtools:drtools /home/drtools/.dask
USER drtools