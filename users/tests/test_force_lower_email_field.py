import pytest

from users.models import ForceLowerEmailField


@pytest.mark.parametrize(
    'value,lowered_value',
    (
        ('Abc123@test.com', 'abc123@test.com'),
        ('abc123@Test.com', 'abc123@test.com'),
        ('ALL_CAPS@TEST.COM', 'all_caps@test.com'),
        ('no_caps@test.com', 'no_caps@test.com'),
    ),
)
def test_force_lower_field(value, lowered_value):

    field = ForceLowerEmailField()

    assert field.get_prep_value(value) == lowered_value
