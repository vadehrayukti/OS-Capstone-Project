
import pytest

from memory_management import first_fit, best_fit, worst_fit


@pytest.fixture
def sample_memory():
    blocks = [100, 500, 200, 300, 600]
    processes = [212, 417, 112, 426]

    return blocks, processes


def test_first_fit(sample_memory):
    blocks, processes = sample_memory

    result = first_fit(blocks, processes)

    assert result["allocated_processes"] == 3
    assert result["unallocated_processes"] == 1


def test_best_fit(sample_memory):
    blocks, processes = sample_memory

    result = best_fit(blocks, processes)

    assert result["allocated_processes"] == 4
    assert result["unallocated_processes"] == 0


def test_worst_fit(sample_memory):
    blocks, processes = sample_memory

    result = worst_fit(blocks, processes)

    assert result["allocated_processes"] == 3


def test_first_fit_allocation_details(sample_memory):
    blocks, processes = sample_memory

    result = first_fit(blocks, processes)

    allocations = result["allocations"]

    assert allocations[0]["block"] == 2
    assert allocations[1]["block"] == 5
    assert allocations[2]["block"] == 3
    assert allocations[3]["status"] == "Not Allocated"


def test_empty_memory_blocks():
    with pytest.raises(ValueError):
        first_fit([], [100, 200])


def test_empty_processes():
    with pytest.raises(ValueError):
        best_fit([100, 200], [])


def test_invalid_memory_block():
    with pytest.raises(ValueError):
        worst_fit([100, -200], [50])


def test_process_larger_than_all_blocks():
    result = first_fit([100, 200], [500])

    assert result["unallocated_processes"] == 1
