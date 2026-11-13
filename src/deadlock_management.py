
def validate_input(available, allocation, maximum):
    """Validate Banker's Algorithm input."""

    if not available or not allocation or not maximum:
        raise ValueError("Input matrices and available resources cannot be empty.")

    if len(allocation) != len(maximum):
        raise ValueError("Allocation and maximum matrices must have equal rows.")

    resource_count = len(available)

    for row in allocation + maximum:
        if len(row) != resource_count:
            raise ValueError("All matrix rows must have equal columns.")

        for value in row:
            if not isinstance(value, int) or value < 0:
                raise ValueError("Resource values must be non-negative integers.")

    for value in available:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Available resources must be non-negative integers.")

    for process_index in range(len(allocation)):
        for resource_index in range(resource_count):
            if allocation[process_index][resource_index] > maximum[process_index][resource_index]:
                raise ValueError("Allocation cannot exceed maximum requirement.")


def calculate_need(allocation, maximum):
    """Calculate Need = Maximum - Allocation."""

    need = []

    for process_index in range(len(allocation)):
        row = []

        for resource_index in range(len(allocation[process_index])):
            value = (
                maximum[process_index][resource_index]
                - allocation[process_index][resource_index]
            )
            row.append(value)

        need.append(row)

    return need


def bankers_algorithm(available, allocation, maximum):
    """Check whether the system is in a safe state."""

    validate_input(available, allocation, maximum)

    process_count = len(allocation)

    need = calculate_need(allocation, maximum)

    work = available.copy()
    finish = [False] * process_count
    safe_sequence = []

    while len(safe_sequence) < process_count:

        found_process = False

        for process_index in range(process_count):

            if not finish[process_index]:

                can_execute = True

                for resource_index in range(len(available)):
                    if need[process_index][resource_index] > work[resource_index]:
                        can_execute = False
                        break

                if can_execute:

                    # Release the resources held by this process.
                    for resource_index in range(len(available)):
                        work[resource_index] += allocation[process_index][resource_index]

                    finish[process_index] = True
                    safe_sequence.append(f"P{process_index}")

                    found_process = True

        if not found_process:
            break

    is_safe = all(finish)

    return {
        "need_matrix": need,
        "final_available": work,
        "is_safe": is_safe,
        "state": "Safe State" if is_safe else "Unsafe State",
        "safe_sequence": safe_sequence if is_safe else None
    }
