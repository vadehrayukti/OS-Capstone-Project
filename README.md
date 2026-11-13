# OS-Capstone-Project
 A Python-based Operating System simulator implementing CPU scheduling, memory management, deadlock avoidance, and disk scheduling algorithms with performance comparisons, visualizations, and automated testing.

## Author- YUKTI VADEHRA (2401010128)
# OS Resource Management Simulator
## 1. Project Overview

The OS Resource Management Simulator demonstrates important Operating System concepts through the implementation of CPU scheduling, memory allocation, deadlock management, and disk scheduling algorithms.

The application provides a menu-driven interface where users can execute individual algorithms, compare their performance, and generate result files and graphical reports.

## 2. Modules and Algorithms

### CPU Scheduling
- First Come First Serve (FCFS)
- Shortest Job First (SJF – Non-Preemptive)
- Round Robin (RR)

Performance metrics:
- Completion Time (CT)
- Turnaround Time (TAT)
- Waiting Time (WT)
- Response Time (RT)
- Average scheduling metrics

### Memory Management
- First Fit
- Best Fit
- Worst Fit

Performance metric:
- Internal Fragmentation

### Deadlock Management
- Banker's Algorithm
- Safe and Unsafe State Detection
- Safe Sequence Generation
- Need Matrix Calculation

### Disk Scheduling
- First Come First Serve (FCFS)
- Shortest Seek Time First (SSTF)
- SCAN

Performance metric:
- Total Head Movement

## 3. Technologies Used

- Python
- Bash Scripting
- Matplotlib
- Pytest
- JSON and CSV

## 4. Project Structure

```text
OS-Resource-Management-Simulator/
│
├── src/
│   ├── main.py
│   ├── cpu_scheduling.py
│   ├── memory_management.py
│   ├── deadlock_management.py
│   ├── disk_scheduling.py
│   └── reporting.py
│
├── scripts/
│   ├── run.sh
│   └── test.sh
│
├── data/
│   └── sample_input.json
│
├── tests/
│   ├── conftest.py
│   ├── test_cpu.py
│   ├── test_memory.py
│   ├── test_deadlock.py
│   └── test_disk.py
│
├── outputs/
│   ├── results/
│   └── logs/
│
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

## 5. Installation and Requirements

### Prerequisites
- Python 3.x
- pip
- Git Bash (for running the Bash scripts on Windows)

### Install Dependencies

Clone or download the project and navigate to its root directory.

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 6. Running the Application

Using Git Bash:

```bash
bash scripts/run.sh
```

Alternatively, run directly using Python:

```bash
python src/main.py
```

The application displays a main menu with four modules:

1. CPU Scheduling
2. Memory Management
3. Deadlock Management
4. Disk Scheduling

Users can select individual algorithms or choose the comparison option where available.

## 7. Input Data

Sample input is provided in:

```text
data/sample_input.json
```

The JSON file contains:
- Process arrival and burst times
- CPU scheduling time quantum
- Memory block sizes and process sizes
- Available, allocated, and maximum resources
- Disk requests, initial head position, disk size, and SCAN direction

The sample input can be modified to experiment with different scenarios.

## 8. Performance Analysis and Outputs

The simulator generates comparison tables and graphical reports for:

- CPU scheduling algorithms
- Memory allocation algorithms
- Disk scheduling algorithms

Generated outputs are stored in:

```text
outputs/results/
```

The application also saves individual algorithm results in JSON format and maintains an application log in:

```text
outputs/logs/application.log
```

## 9. Testing

The project uses Pytest for automated testing.

Run the test suite using:

```bash
bash scripts/test.sh
```

Alternatively:

```bash
python -m pytest -v
```

### Test Summary

| Module | Tests |
|---|---:|
| CPU Scheduling | 7 |
| Deadlock Management | 7 |
| Disk Scheduling | 9 |
| Memory Management | 8 |
| **Total** | **31** |

**Test Result: 31 Passed, 0 Failed**

## 10. Project Objectives

- Understand and implement fundamental Operating System resource-management algorithms.
- Compare algorithm performance using relevant metrics.
- Demonstrate safe-state detection using Banker's Algorithm.
- Integrate Python modules with Bash scripts.
- Generate graphical and tabular performance reports.
- Validate implementations through automated testing.

## 11. Limitations

- The application is a simulation and does not modify actual Operating System resource allocation.
- Input data is provided through a JSON file.
- Memory allocation uses fixed-size partitions.
- The application provides a command-line interface rather than a graphical interface.

## 12. Conclusion

The OS Resource Management Simulator provides a practical demonstration of important Operating System resource-management concepts. By implementing and comparing multiple algorithms, the project helps illustrate their working principles, performance characteristics, and practical differences.

The project combines modular Python programming, Bash scripting, graphical reporting, and automated testing into a single integrated application.
