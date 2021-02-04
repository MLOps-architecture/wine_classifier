from logging import getLogger

import luigi
import datetime as dt
from drtools.utils.task import DockerTask
from .structure import PATH

class Example(DockerTask):

    @property
    def command(self):
        return ['python', '-m', 'awesome_ml.data.dataset']

    @property
    def name(self):
        return 'test-template-container'

    def requires(self):
        return ClientUpload()

    def output(self):
        return luigi.LocalTarget(str(PATH['CS_OUT']))


class Debug(DockerTask):

    @property
    def command(self):
        return ['sleep', '24h']

    @property
    def name(self):
        return 'debug-container'

    def output(self):
        return luigi.LocalTarget(str(PATH['CS_OUT']))


class ClientUpload(luigi.ExternalTask):

    def output(self):
        return luigi.LocalTarget(str(PATH['CS_IN']))
