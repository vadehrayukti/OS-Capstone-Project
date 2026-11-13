
import pytest

from cpu_scheduling import fcfs, sjf, round_robin


@pytest.fixture
def sample_processes():
    return [
        {"pid": "P1", "arrival_time": 0, "burst_time": 5},
        {"pid": "P2", "arrival_time": 1, "burst_time": 3},
        {"pid": "P3", "arrival_time": 2, "burst_time": 8},
        {"pid": "P4", "arrival_time": 3, "burst_time": 2}
    ]


def test_fcfs_average_waiting_time(sample_processes):
    result = fcfs(sample_processes)
    assert result["average_waiting_time"] == 5.75


def test_sjf_returns_all_processes(sample_processes):
    result = sjf(sample_processes)
    assert len(result["process_results"]) == 4


def test_round_robin_returns_all_processes(sample_processes):
    result = round_robin(sample_processes, 2)
    assert len(result["process_results"]) == 4


def test_fcfs_gantt_chart(sample_processes):
    result = fcfs(sample_processes)

    assert result["gantt_chart"][0]["start"] == 0
    assert result["gantt_chart"][-1]["end"] == 18


def test_invalid_empty_processes():
    with pytest.raises(ValueError):
        fcfs([])


def test_invalid_zero_burst_time():
    processes = [
        {"pid": "P1", "arrival_time": 0, "burst_time": 0}
    ]

    with pytest.raises(ValueError):
        fcfs(processes)


def test_invalid_time_quantum(sample_processes):
    with pytest.raises(ValueError):
        round_robin(sample_processes, 0)
