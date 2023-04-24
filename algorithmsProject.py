# [Exhaustive Method]: This solution should implement an algorithm that
#                      tries every possible combination of processes that can fit within the timeline then finds
#                      the combination that results in the maximum value.

# Each processor has an [id, duration, and value] that will be inputed and time limit

def schedule_processes(processors, time_limit):
    """
    Tries every possible combination of processors that can fit within the time limit
    then finds the combination that results in the maximum value.

    Parameters:
    processors (list of tuples): List of processors, each represented as a tuple (id, duration, value).
    time_limit (int): Total time available for scheduling the processors.

    Returns:
    tuple: A tuple containing the selected processors and their total value.
    """
    max_value = 0
    selected_processors = []

    # Try every possible combination of subsets
    for i in range(1, 2**len(processors)):
        subset = [processors[j] for j in range(len(processors)) if (i & (1<<j))]

        # Check if the subset can fit within the time limit
        total_duration = sum(p[1] for p in subset)
        if total_duration <= time_limit:
            # Compute the total value of the subset
            total_value = sum(p[2] for p in subset)
            # Update the selected processors and maximum value if necessary
            if total_value > max_value:
                max_value = total_value
                selected_processors = subset

    return selected_processors#, max_value


p = [(1,3,21), (2,6,24), (3,2,12), (4,4,20)] # THESE ARE THE prosseces THE USER SHOULD INPUT THEM TEHE 
# print(schedule_processes(p,8))
op_p=schedule_processes(p,8)
print('Selected processes:',[i[0] for i in op_p])
print('total value is',sum(op_p[2] for op_p in op_p))
print('total duration is',sum(op_p[1] for op_p in op_p))