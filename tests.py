import pytest

from main import confirm_action


@pytest.mark.parametrize('confirmation, correct', [
    ('Y', True), ('y', True), ('N', False), ('n', False), ('whatever', False),
])
def test_confirm_action(confirmation, correct, mocker):
    mocker.patch('builtins.input', return_value=confirmation)

    assert confirm_action() is correct
