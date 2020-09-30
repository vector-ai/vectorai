"""Testing the base
"""
import os
import pytest
from vectorai.models import *
from appdirs import *


def test_start_utils_mixin():
    utils_func = EmbedMixin()
    assert True


def check():
    """Dummy function"""
    return 1


def test_save_function():
    """Test adding an embedding function"""
    mixin = EmbedMixin("test", "test")
    index_name = "test"
    vector_name = "test"
    mixin.save_function(index_name, vector_name, check)
    assert True


def test_load_function():
    """Test loading of the function"""
    mixin = EmbedMixin("test", "test")
    assert mixin.load_function("test", "test") == check


def test_load_function_keyerror():
    """Test loading of the function"""
    with pytest.raises(KeyError):
        mixin = EmbedMixin("test", "test")
        assert mixin.load_function("test", "check") != check


@pytest.mark.xfail
def test_save_string_input():
    """Testing for string input. This should fail.
    """
    string_input = "def function"
    with pytest.raises(AssertionError):
        mixin = EmbedMixin("test", "test")
        mixin.save_function("test", "new", string_input)
