"""Test fixtures."""

import os
import shutil
import tempfile

import pytest

_HERE = os.path.dirname(__file__)
TEST_SAMPLE_DATASET = os.path.join(_HERE, "data", "sample_data")
SAMPLE_SMART_TOOLS = os.path.join(_HERE, "sample_smart_tools")

shasum_smart_tool = os.path.join(SAMPLE_SMART_TOOLS, "shasum.py")
shasum_smart_import_tool = os.path.join(SAMPLE_SMART_TOOLS, "shasum_import.py")


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
