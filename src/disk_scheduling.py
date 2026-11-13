
def validate_disk_input(requests, head, disk_size):
    """Validate disk scheduling input."""

    if not isinstance(disk_size, int) or disk_size <= 0:
        raise ValueError("Disk size must be a positive integer.")

    if not isinstance(head, int) or not 0 <= head < disk_size:
        raise ValueError("Initial head position is outside disk limits.")

    if not requests:
        raise ValueError("Disk request list cannot be empty.")

    for request in requests:
        if not isinstance(request, int) or not 0 <= request < disk_size:
            raise ValueError("Disk request is outside disk limits.")


def calculate_result(algorithm, sequence, initial_head):
    """Calculate total and average head movement."""

    total_movement = 0
    current_head = initial_head

    for position in sequence:
        total_movement += abs(position - current_head)
        current_head = position

    return {
        "algorithm": algorithm,
        "initial_head": initial_head,
        "seek_sequence": sequence,
        "total_head_movement": total_movement,
        "average_head_movement": round(
            total_movement / len(sequence), 2
        )
    }


def fcfs(requests, head, disk_size):
    """First Come First Serve disk scheduling."""

    validate_disk_input(requests, head, disk_size)

    sequence = requests.copy()

    return calculate_result("FCFS", sequence, head)


def sstf(requests, head, disk_size):
    """Shortest Seek Time First disk scheduling."""

    validate_disk_input(requests, head, disk_size)

    remaining = requests.copy()
    sequence = []
    current_head = head

    while remaining:

        nearest = min(
            remaining,
            key=lambda request: abs(request - current_head)
        )

        sequence.append(nearest)
        current_head = nearest
        remaining.remove(nearest)

    return calculate_result("SSTF", sequence, head)


def scan(requests, head, disk_size, direction="right"):
    """SCAN (Elevator) disk scheduling."""

    validate_disk_input(requests, head, disk_size)

    if direction not in ("left", "right"):
        raise ValueError("Direction must be 'left' or 'right'.")

    left_requests = sorted(
        [request for request in requests if request < head],
        reverse=True
    )

    right_requests = sorted(
        [request for request in requests if request >= head]
    )

    sequence = []

    if direction == "right":

        sequence.extend(right_requests)

        # Reach the right disk boundary before reversing.
        if head != disk_size - 1:
            sequence.append(disk_size - 1)

        sequence.extend(left_requests)

    else:

        sequence.extend(left_requests)

        # Reach the left disk boundary before reversing.
        if head != 0:
            sequence.append(0)

        sequence.extend(right_requests)

    return calculate_result("SCAN", sequence, head)
