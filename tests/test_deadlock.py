
import pytest

from deadlock_management import bankers_algorithm, calculate_need


@pytest.fixture
def safe_input():
    available = [3, 3, 2]

    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    return available, allocation, maximum


def test_bankers_safe_state(safe_input):
    available, allocation, maximum = safe_input

    result = bankers_algorithm(available, allocation, maximum)

    assert result["is_safe"] is True
    assert result["state"] == "Safe State"


def test_bankers_safe_sequence(safe_input):
    available, allocation, maximum = safe_input

    result = bankers_algorithm(available, allocation, maximum)

    assert result["safe_sequence"] is not None
    assert len(result["safe_sequence"]) == 5


def test_need_matrix(safe_input):
    available, allocation, maximum = safe_input

    need = calculate_need(allocation, maximum)

    assert need[0] == [7, 4, 3]
    assert need[1] == [1, 2, 2]


def test_bankers_unsafe_state():
    available = [0, 0]
    allocation = [
        [1, 0],
        [0, 1]
    ]
    maximum = [
        [2, 0],
        [0, 2]
    ]

    result = bankers_algorithm(available, allocation, maximum)

    assert result["is_safe"] is False
    assert result["state"] == "Unsafe State"
    assert result["safe_sequence"] is None


def test_invalid_matrix_dimensions():
    available = [3, 3, 2]
    allocation = [[0, 1]]
    maximum = [[2, 2, 2]]

    with pytest.raises(ValueError):
        bankers_algorithm(available, allocation, maximum)


def test_allocation_exceeds_maximum():
    available = [1, 1]
    allocation = [[2, 0]]
    maximum = [[1, 1]]

    with pytest.raises(ValueError):
        bankers_algorithm(available, allocation, maximum)


def test_empty_input():
    with pytest.raises(ValueError):
        bankers_algorithm([], [], [])
