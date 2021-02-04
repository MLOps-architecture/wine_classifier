from logging import getLogger

import click
import pandas as pd
from dask import delayed
from distributed import Client

from ..structure import PATH


@click.command()
def cli():
    log = getLogger(__name__)
    c = Client('dask-scheduler:8786')
    log.info('Connected to scheduler')
    read_and_dump_using_dask()


def read_and_dump_using_dask():
    log = getLogger(__name__)

    log.debug('Reading data from: %s' % PATH['CS_IN'])
    df = delayed(pd.read_csv)(str(PATH['CS_IN'])).compute()

    log.info('Clickstream loaded:\n{}'.format(str(df)))
    log.debug('Saving clickstream to: %s' % PATH['CS_IN'])

    df.to_pickle(str(PATH['CS_OUT']))


if __name__ == '__main__':
    cli()
