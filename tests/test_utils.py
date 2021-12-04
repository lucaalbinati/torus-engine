import pytest
from utils import replace_in_string

@pytest.mark.parametrize("original_string,index,character,expected_new_string",
    [
        ("hello", 0, 'y', "yello"),
        ("hello", 4, '!', "hell!")
    ]
)
def test_replace_in_string_correct(original_string, index, character, expected_new_string):
    new_string = replace_in_string(original_string, index, character)
    assert new_string == expected_new_string

@pytest.mark.parametrize("original_string,index,character",
    [
        ("hello", -1, 'y'),
        ("too long", 20, 'a')
    ]
)
def test_replace_in_string_incorrect_index(original_string, index, character):
    with pytest.raises(Exception):
        new_string = replace_in_string(original_string, index, character)

@pytest.mark.parametrize("original_string,index,character",
    [
        ("hello", 4, "world")
    ]
)
def test_replace_in_string_incorrect_character(original_string, index, character):
    with pytest.raises(Exception):
        new_string = replace_in_string(original_string, index, character)
