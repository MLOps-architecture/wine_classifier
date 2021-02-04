import pytest
from click.testing import CliRunner
from drtools.utils.testing import tmp_root_dir

from awesome_ml.data.dataset import read_and_dump_using_dask
from awesome_ml.structure import PATH


def test_dataset_cli():
    with tmp_root_dir(filter=lambda p: p.name == 'clickstream.csv'):
        read_and_dump_using_dask()
        assert PATH['CS_OUT'].exists()