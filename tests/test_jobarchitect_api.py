"""Test the jobarchitect package."""


def test_version_is_string():
    import jobarchitect
    assert isinstance(jobarchitect.__version__, str)
