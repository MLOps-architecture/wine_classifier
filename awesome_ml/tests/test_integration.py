import os
import luigi
import pytest
from awesome_ml.task import Example
from drtools.utils.testing import clean_root_dir


pytestmark = pytest.mark.skipif(
    os.environ.get('TEST_INTEGRATION', 'false') == 'false',
    reason="Set TEST_INTEGRATION=true to execute integration tests")


@pytest.fixture(autouse=True)
def clean_root():
    with clean_root_dir():
        yield


def test_integration():
    task = Example()
    success = luigi.build([task], scheduler_host='localhost')
    assert success
