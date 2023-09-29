"""Tests for aml_utils module."""

import os

from aml_utils.config import get_root_path, retrieve_config


def test_config_root_path():
    """
    Test get_root_path function in config submodule.

    Checks that the path retrieved points to the right place.
    """
    root_path = get_root_path()
    files_root = os.listdir(root_path)
    assert 'azure-pipelines' in files_root
    assert 'configuration' in files_root
    assert 'mlops' in files_root
    assert 'src' in files_root
    assert 'LICENSE' in files_root


def test_retrieve_config():
    """Test retrieve_config function in config submodule."""
    config = retrieve_config()
    assert isinstance(config, dict)
    assert len(config) > 0
