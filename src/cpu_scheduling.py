
"""
CPU Scheduling Module
OS Resource Management Simulator

Algorithms:
1. First Come First Serve (FCFS)
2. Shortest Job First (SJF - Non-preemptive)
3. Round Robin (RR)
"""

from collections import deque


def validate_processes(processes):
    """Validate process input before scheduling."""

    if not processes:
        raise ValueError("Process list cannot be empty.")

    process_ids = set()

    for process in processes:
        required = {"pid", "arrival_time", "burst_time"}

        if not required.issubset(process):
            raise ValueError("Each process must have PID, arrival time and burst time.")

        pid = process["pid"]
        arrival = process["arrival_time"]
        burst = process["burst_time"]

        if pid in process_ids:
            raise ValueError("Process IDs must be unique.")

        if not isinstance(arrival, int) or isinstance(arrival, bool) or arrival < 0:
            raise ValueError("Arrival time must be a non-negative integer.")

        if not isinstance(burst, int) or isinstance(burst, bool) or burst <= 0:
            raise ValueError("Burst time must be a positive integer.")

        process_ids.add(pid)


def calculate_metrics(processes, completion_times, first_start_times):
    """Calculate scheduling performance metrics."""

    results = []

    for process in processes:
        pid = process["pid"]
        arrival = process["arrival_time"]
        burst = process["burst_time"]

        completion = completion_times[pid]
        turnaround = completion - arrival
        waiting = turnaround - burst
        response = first_start_times[pid] - arrival

        results.append({
            "pid": pid,
            "arrival_time": arrival,
            "burst_time": burst,
            "completion_time": completion,
            "turnaround_time": turnaround,
            "waiting_time": waiting,
            "response_time": response
        })

    count = len(results)

    return {
        "process_results": results,
        "average_waiting_time": sum(p["waiting_time"] for p in results) / count,
        "average_turnaround_time": sum(p["turnaround_time"] for p in results) / count,
        "average_response_time": sum(p["response_time"] for p in results) / count
    }


def add_gantt_segment(gantt_chart, pid, start, end):
    """Add a segment and merge consecutive execution of the same process."""

    if start == end:
        return

    if (gantt_chart and
            gantt_chart[-1]["pid"] == pid and
            gantt_chart[-1]["end"] == start):

        gantt_chart[-1]["end"] = end

    else:
        gantt_chart.append({
            "pid": pid,
            "start": start,
            "end": end
        })


# --------------------------------------------------
# 1. FIRST COME FIRST SERVE (FCFS)
# --------------------------------------------------

def fcfs(processes):
    """Execute processes in order of arrival time."""

    validate_processes(processes)

    ordered_processes = sorted(
        processes,
        key=lambda p: p["arrival_time"]
    )

    current_time = 0
    completion_times = {}
    first_start_times = {}
    gantt_chart = []

    for process in ordered_processes:

        pid = process["pid"]
        arrival = process["arrival_time"]
        burst = process["burst_time"]

        # Handle CPU idle time
        if current_time < arrival:
            add_gantt_segment(gantt_chart, "IDLE", current_time, arrival)
            current_time = arrival

        first_start_times[pid] = current_time

        current_time += burst
        completion_times[pid] = current_time

        add_gantt_segment(
            gantt_chart, pid, first_start_times[pid], current_time
        )

    metrics = calculate_metrics(
        ordered_processes, completion_times, first_start_times
    )

    return {
        "algorithm": "FCFS",
        **metrics,
        "gantt_chart": gantt_chart
    }


# --------------------------------------------------
# 2. SHORTEST JOB FIRST (SJF - NON-PREEMPTIVE)
# --------------------------------------------------

def sjf(processes):
    """Execute the shortest available process first."""

    validate_processes(processes)

    remaining_processes = list(enumerate(processes))

    current_time = 0
    completed = 0

    completion_times = {}
    first_start_times = {}
    gantt_chart = []

    while completed < len(processes):

        # Find processes that have already arrived
        available_processes = [
            (index, process)
            for index, process in remaining_processes
            if process["arrival_time"] <= current_time
        ]

        # If no process is available, move to next arrival
        if not available_processes:

            next_arrival = min(
                process["arrival_time"]
                for _, process in remaining_processes
            )

            add_gantt_segment(
                gantt_chart, "IDLE", current_time, next_arrival
            )

            current_time = next_arrival
            continue

        # Select the process with the shortest burst time
        index, selected_process = min(
            available_processes,
            key=lambda item: (
                item[1]["burst_time"],
                item[1]["arrival_time"],
                item[0]
            )
        )

        pid = selected_process["pid"]
        burst = selected_process["burst_time"]

        first_start_times[pid] = current_time

        current_time += burst
        completion_times[pid] = current_time

        add_gantt_segment(
            gantt_chart,
            pid,
            first_start_times[pid],
            current_time
        )

        remaining_processes.remove((index, selected_process))
        completed += 1

    metrics = calculate_metrics(
        processes, completion_times, first_start_times
    )

    return {
        "algorithm": "SJF (Non-preemptive)",
        **metrics,
        "gantt_chart": gantt_chart
    }


# --------------------------------------------------
# 3. ROUND ROBIN (RR)
# --------------------------------------------------

def round_robin(processes, time_quantum):
    """Execute processes using the Round Robin scheduling algorithm."""

    validate_processes(processes)

    if (not isinstance(time_quantum, int) or
            isinstance(time_quantum, bool) or
            time_quantum <= 0):
        raise ValueError("Time quantum must be a positive integer.")

    ordered_processes = sorted(
        processes,
        key=lambda p: p["arrival_time"]
    )

    remaining_burst = {
        p["pid"]: p["burst_time"] for p in processes
    }

    completion_times = {}
    first_start_times = {}
    gantt_chart = []

    ready_queue = deque()

    current_time = 0
    next_process = 0
    completed = 0
    total_processes = len(processes)

    while completed < total_processes:

        # Add all processes that have arrived
        while (next_process < total_processes and
               ordered_processes[next_process]["arrival_time"] <= current_time):

            ready_queue.append(ordered_processes[next_process]["pid"])
            next_process += 1

        # Handle CPU idle time
        if not ready_queue:

            next_arrival = ordered_processes[next_process]["arrival_time"]

            add_gantt_segment(
                gantt_chart, "IDLE", current_time, next_arrival
            )

            current_time = next_arrival
            continue

        pid = ready_queue.popleft()

        if pid not in first_start_times:
            first_start_times[pid] = current_time

        execution_time = min(
            time_quantum, remaining_burst[pid]
        )

        start_time = current_time
        current_time += execution_time

        remaining_burst[pid] -= execution_time

        add_gantt_segment(
            gantt_chart, pid, start_time, current_time
        )

        # Add newly arrived processes to the ready queue
        while (next_process < total_processes and
               ordered_processes[next_process]["arrival_time"] <= current_time):

            ready_queue.append(ordered_processes[next_process]["pid"])
            next_process += 1

        # Check whether the process has completed
        if remaining_burst[pid] == 0:

            completion_times[pid] = current_time
            completed += 1

        else:
            ready_queue.append(pid)

    metrics = calculate_metrics(
        processes, completion_times, first_start_times
    )

    return {
        "algorithm": "Round Robin",
        "time_quantum": time_quantum,
        **metrics,
        "gantt_chart": gantt_chart
    }
