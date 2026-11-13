
import pytest

from disk_scheduling import fcfs, sstf, scan


@pytest.fixture
def sample_disk():
    requests = [82, 170, 43, 140, 24, 16, 190]
    head = 50
    disk_size = 200

    return requests, head, disk_size


def test_fcfs_total_movement(sample_disk):
    requests, head, disk_size = sample_disk

    result = fcfs(requests, head, disk_size)

    assert result["total_head_movement"] == 642


def test_sstf_total_movement(sample_disk):
    requests, head, disk_size = sample_disk

    result = sstf(requests, head, disk_size)

    assert result["total_head_movement"] == 208


def test_scan_total_movement(sample_disk):
    requests, head, disk_size = sample_disk

    result = scan(requests, head, disk_size, "right")

    assert result["total_head_movement"] == 332


def test_fcfs_request_order(sample_disk):
    requests, head, disk_size = sample_disk

    result = fcfs(requests, head, disk_size)

    assert result["seek_sequence"] == requests


def test_invalid_head_position():
    with pytest.raises(ValueError):
        fcfs([10, 20], 200, 200)


def test_invalid_disk_request():
    with pytest.raises(ValueError):
        sstf([10, 250], 50, 200)


def test_invalid_disk_size():
    with pytest.raises(ValueError):
        scan([10, 20], 5, 0)


def test_invalid_scan_direction(sample_disk):
    requests, head, disk_size = sample_disk

    with pytest.raises(ValueError):
        scan(requests, head, disk_size, "up")


def test_empty_requests():
    with pytest.raises(ValueError):
        fcfs([], 50, 200)
