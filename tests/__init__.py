"""Test fixtures."""

import os
import shutil
import tempfile

import pytest

_HERE = os.path.dirname(__file__)
TEST_SAMPLE_DATASET = os.path.join(_HERE, "data", "sample_data")
CWL_TOOL_WRAPPERS = os.path.join(_HERE, "cwl_tool_wrappers")

shasum_cwl_tool_wrapper = os.path.join(CWL_TOOL_WRAPPERS, 'shasum.cwl')
sha1sum_cwl_tool_wrapper = os.path.join(CWL_TOOL_WRAPPERS, 'sha1sum.cwl')


@pytest.fixture
def chdir_fixture(request):
    d = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(d)

    @request.addfinalizer
    def teardown():
        os.chdir(curdir)
        shutil.rmtree(d)


@pytest.fixture
def tmp_dir_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def local_tmp_dir_fixture(request):
    d = tempfile.mkdtemp(dir=_HERE)

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d
