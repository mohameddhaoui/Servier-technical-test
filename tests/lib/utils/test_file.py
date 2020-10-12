import pytest
import pdb

YAML_LOAD_TEST_RETURN = "yaml_loaded"
SCOPE = "function"


@pytest.fixture(scope=SCOPE)
def fxt_yaml_import(mocker):
    from lib.utils.file import load_yaml

    yaml_module = mocker.MagicMock()
    mocker.patch.object(yaml_module, "load", return_value=YAML_LOAD_TEST_RETURN)
    mocker.patch("lib.utils.file.yaml", yaml_module)


@pytest.fixture(scope=SCOPE)
def fxt_builtin_open_import(mocker):
    from unittest.mock import mock_open

    mocker.patch("lib.utils.file.open", mock_open(read_data="data"))


def test_load_yaml(fxt_yaml_import, fxt_builtin_open_import):
    from lib.utils.file import load_yaml

    my_path = "this is a test path"
    res = load_yaml(my_path)
    assert res == YAML_LOAD_TEST_RETURN
