
def validate_memory_input(blocks, processes):
    """Validate memory blocks and process sizes."""

    if not blocks:
        raise ValueError("Memory blocks cannot be empty.")

    if not processes:
        raise ValueError("Process list cannot be empty.")

    for block in blocks:
        if not isinstance(block, int) or block <= 0:
            raise ValueError("Memory block sizes must be positive integers.")

    for process in processes:
        if not isinstance(process, int) or process <= 0:
            raise ValueError("Process sizes must be positive integers.")


def allocate_memory(blocks, processes, strategy):
    """
    Allocate processes to memory blocks using the selected strategy.
    Each block can hold only one process.
    """

    validate_memory_input(blocks, processes)

    if strategy not in ("first_fit", "best_fit", "worst_fit"):
        raise ValueError("Invalid memory allocation strategy.")

    remaining_blocks = blocks.copy()
    allocations = []

    for process_index, process_size in enumerate(processes):

        selected_block = -1

        for block_index, block_size in enumerate(remaining_blocks):

            if block_size >= process_size:

                if strategy == "first_fit":
                    selected_block = block_index
                    break

                elif strategy == "best_fit":
                    if (selected_block == -1 or
                            block_size < remaining_blocks[selected_block]):
                        selected_block = block_index

                elif strategy == "worst_fit":
                    if (selected_block == -1 or
                            block_size > remaining_blocks[selected_block]):
                        selected_block = block_index

        if selected_block != -1:
            allocated_size = remaining_blocks[selected_block]
            internal_fragmentation = allocated_size - process_size

            allocations.append({
                "process": f"P{process_index + 1}",
                "process_size": process_size,
                "block": selected_block + 1,
                "block_size": allocated_size,
                "internal_fragmentation": internal_fragmentation,
                "status": "Allocated"
            })

            # Mark the block as occupied.
            remaining_blocks[selected_block] = 0

        else:
            allocations.append({
                "process": f"P{process_index + 1}",
                "process_size": process_size,
                "block": None,
                "block_size": None,
                "internal_fragmentation": None,
                "status": "Not Allocated"
            })

    allocated_count = sum(
        1 for item in allocations if item["status"] == "Allocated"
    )

    total_fragmentation = sum(
        item["internal_fragmentation"]
        for item in allocations
        if item["internal_fragmentation"] is not None
    )

    return {
        "algorithm": strategy.replace("_", " ").title(),
        "allocations": allocations,
        "total_processes": len(processes),
        "allocated_processes": allocated_count,
        "unallocated_processes": len(processes) - allocated_count,
        "total_internal_fragmentation": total_fragmentation
    }


def first_fit(blocks, processes):
    return allocate_memory(blocks, processes, "first_fit")


def best_fit(blocks, processes):
    return allocate_memory(blocks, processes, "best_fit")


def worst_fit(blocks, processes):
    return allocate_memory(blocks, processes, "worst_fit")
