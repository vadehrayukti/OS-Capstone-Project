
import json
import os

from cpu_scheduling import fcfs, sjf, round_robin
from memory_management import first_fit, best_fit, worst_fit
from deadlock_management import bankers_algorithm
from disk_scheduling import fcfs as disk_fcfs
from disk_scheduling import sstf, scan

from reporting import (
    setup_logging,
    save_result,
    save_comparison_chart,
    save_comparison_csv,
    display_comparison_table
)


def load_sample_data():
    """Load sample input from the JSON file."""

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "data", "sample_input.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)



def display_result(result, module):
    """Display and save algorithm results."""

    print("\n" + "=" * 55)
    print("RESULT")
    print("=" * 55)

    print(json.dumps(result, indent=4))

    algorithm_name = result.get("algorithm", "bankers_algorithm")
    algorithm_name = algorithm_name.lower().replace(" ", "_")

    filename = f"{module}_{algorithm_name}_result.json"

    save_result(filename, result)

    print(f"\nResult saved in outputs/results/{filename}")


def get_cpu_waiting_time(result):
    """Get average waiting time from CPU scheduling results."""

    averages = result.get("averages", {})

    if "waiting_time" in averages:
        return averages["waiting_time"]

    if "average_waiting_time" in averages:
        return averages["average_waiting_time"]

    if "avg_waiting_time" in averages:
        return averages["avg_waiting_time"]

    raise KeyError("Average waiting time not found in CPU results.")


def get_memory_fragmentation(result):
    """Get total internal fragmentation from memory results."""

    if "total_internal_fragmentation" in result:
        return result["total_internal_fragmentation"]

    raise KeyError("Total internal fragmentation not found in memory results.")


def get_disk_movement(result):
    """Get total head movement from disk scheduling results."""

    if "total_head_movement" in result:
        return result["total_head_movement"]

    raise KeyError("Total head movement not found in disk results.")


def compare_cpu_algorithms(processes, quantum):
    """Compare CPU scheduling algorithms using average waiting time."""

    results = [
        fcfs(processes),
        sjf(processes),
        round_robin(processes, quantum)
    ]

    labels = ["FCFS", "SJF", "Round Robin"]
    values = [get_cpu_waiting_time(result) for result in results]

    rows = [
        [label, value]
        for label, value in zip(labels, values)
    ]

    print("\nCPU SCHEDULING COMPARISON")
    display_comparison_table(
        ["Algorithm", "Average Waiting Time"],
        rows
    )

    save_comparison_csv(
        "cpu_comparison.csv",
        ["Algorithm", "Average Waiting Time"],
        rows
    )

    save_comparison_chart(
        "CPU Scheduling Algorithm Comparison",
        labels,
        values,
        "Average Waiting Time",
        "cpu_comparison.png"
    )

    print("\nCPU comparison table and chart saved in outputs/results/")


def compare_memory_algorithms(blocks, processes):
    """Compare memory allocation algorithms using internal fragmentation."""

    results = [
        first_fit(blocks, processes),
        best_fit(blocks, processes),
        worst_fit(blocks, processes)
    ]

    labels = ["First Fit", "Best Fit", "Worst Fit"]
    values = [get_memory_fragmentation(result) for result in results]

    rows = [
        [label, value]
        for label, value in zip(labels, values)
    ]

    print("\nMEMORY MANAGEMENT COMPARISON")
    display_comparison_table(
        ["Algorithm", "Total Internal Fragmentation"],
        rows
    )

    save_comparison_csv(
        "memory_comparison.csv",
        ["Algorithm", "Total Internal Fragmentation"],
        rows
    )

    save_comparison_chart(
        "Memory Allocation Algorithm Comparison",
        labels,
        values,
        "Internal Fragmentation",
        "memory_comparison.png"
    )

    print("\nMemory comparison table and chart saved in outputs/results/")


def compare_disk_algorithms(requests, head, disk_size, direction):
    """Compare disk scheduling algorithms using total head movement."""

    results = [
        disk_fcfs(requests, head, disk_size),
        sstf(requests, head, disk_size),
        scan(requests, head, disk_size, direction)
    ]

    labels = ["FCFS", "SSTF", "SCAN"]
    values = [get_disk_movement(result) for result in results]

    rows = [
        [label, value]
        for label, value in zip(labels, values)
    ]

    print("\nDISK SCHEDULING COMPARISON")
    display_comparison_table(
        ["Algorithm", "Total Head Movement"],
        rows
    )

    save_comparison_csv(
        "disk_comparison.csv",
        ["Algorithm", "Total Head Movement"],
        rows
    )

    save_comparison_chart(
        "Disk Scheduling Algorithm Comparison",
        labels,
        values,
        "Total Head Movement",
        "disk_comparison.png"
    )

    print("\nDisk comparison table and chart saved in outputs/results/")


def cpu_menu(data):
    processes = data["cpu"]["processes"]
    quantum = data["cpu"]["time_quantum"]

    while True:
        print("\n--- CPU SCHEDULING ---")
        print("1. First Come First Serve (FCFS)")
        print("2. Shortest Job First (SJF)")
        print("3. Round Robin")
        print("4. Compare All Algorithms")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_result(fcfs(processes), "cpu")

        elif choice == "2":
            display_result(sjf(processes), "cpu")

        elif choice == "3":
            display_result(round_robin(processes, quantum), "cpu")

        elif choice == "4":
            compare_cpu_algorithms(processes, quantum)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Try again.")


def memory_menu(data):
    blocks = data["memory"]["blocks"]
    processes = data["memory"]["processes"]

    while True:
        print("\n--- MEMORY MANAGEMENT ---")
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")
        print("4. Compare All Algorithms")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_result(first_fit(blocks, processes), "memory")

        elif choice == "2":
            display_result(best_fit(blocks, processes), "memory")

        elif choice == "3":
            display_result(worst_fit(blocks, processes), "memory")

        elif choice == "4":
            compare_memory_algorithms(blocks, processes)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Try again.")


def deadlock_menu(data):
    deadlock = data["deadlock"]

    print("\n--- DEADLOCK MANAGEMENT ---")

    result = bankers_algorithm(
        deadlock["available"],
        deadlock["allocation"],
        deadlock["maximum"]
    )

    display_result(result, "deadlock")


def disk_menu(data):
    disk = data["disk"]

    requests = disk["requests"]
    head = disk["head"]
    disk_size = disk["disk_size"]
    direction = disk["direction"]

    while True:
        print("\n--- DISK SCHEDULING ---")
        print("1. FCFS")
        print("2. SSTF")
        print("3. SCAN")
        print("4. Compare All Algorithms")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_result(disk_fcfs(requests, head, disk_size), "disk")

        elif choice == "2":
            display_result(sstf(requests, head, disk_size), "disk")

        elif choice == "3":
            display_result(
                scan(requests, head, disk_size, direction),
                "disk"
            )

        elif choice == "4":
            compare_disk_algorithms(
                requests, head, disk_size, direction
            )

        elif choice == "0":
            break

        else:
            print("Invalid choice. Try again.")


def main():
    setup_logging()

    try:
        data = load_sample_data()

        while True:
            print("\n" + "=" * 55)
            print("       OS RESOURCE MANAGEMENT SIMULATOR")
            print("=" * 55)

            print("1. CPU Scheduling")
            print("2. Memory Management")
            print("3. Deadlock Management")
            print("4. Disk Scheduling")
            print("0. Exit")

            choice = input("\nEnter your choice: ")

            try:
                if choice == "1":
                    cpu_menu(data)

                elif choice == "2":
                    memory_menu(data)

                elif choice == "3":
                    deadlock_menu(data)

                elif choice == "4":
                    disk_menu(data)

                elif choice == "0":
                    print("\nThank you for using the simulator!")
                    break

                else:
                    print("\nInvalid choice. Please try again.")

            except (ValueError, KeyError, TypeError) as error:
                print(f"\nError: {error}")

    except FileNotFoundError:
        print("Error: Sample input file was not found.")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format in sample input file.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
