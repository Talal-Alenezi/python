from time import time

def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


# processor has an [id, duration, and value]
@timer_func
def schedule_processes_Exhaustive(processors, time_limit):
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
# END OF Exhaustive

@timer_func
def schedule_processes_Greedy_Value(processes, time_limit):
    """
    Given an array of tuples representing processes with (id, duration, value),
    selects a subset of processes that will maximize the total value while staying
    within the time limit on a single-threaded CPU.
    """
    # sort the processes by decreasing value
    sorted_processes = sorted(processes, key=lambda x: x[2], reverse=True)
    selected_processes = []
    current_time = 0
    
    for process in sorted_processes:
        # check if adding the current process would exceed the time limit
        if current_time + process[1] > time_limit:
            continue
        
        # add the current process to the selected processes
        selected_processes.append(process)
        
        # update the current time
        current_time += process[1]
    
    return selected_processes
# END OF GREEDY BY VALUE

@timer_func
def schedule_processes_greedy_duration(processes, time_limit):
    # Sort the processes by their duration in increasing order
    sorted_processes = sorted(processes, key=lambda x: x[1])
    
    selected_processes = []
    current_time = 0
    
    # Loop through the sorted processes and select the ones that fit within the time limit
    for process in sorted_processes:
        if current_time + process[1] <= time_limit:
            selected_processes.append(process)
            current_time += process[1]
    
    return selected_processes
# END OF GREEDY BY DURATION

@timer_func
def process_selection_dp(processes, time_limit):
    memo = {}

    def dp(i, t):
        if i == 0 or t == 0:
            return 0
        if (i, t) in memo:
            return memo[(i, t)]
        if processes[i-1][1] > t:
            memo[(i, t)] = dp(i-1, t)
            return memo[(i, t)]
        memo[(i, t)] = max(dp(i-1, t), dp(i-1, t-processes[i-1][1]) + processes[i-1][2])
        return memo[(i, t)]

    n = len(processes)
    optimal_value = dp(n, time_limit)
    selected = []
    t = time_limit

    for i in range(n, 0, -1):
        if optimal_value <= 0:
            break
        if optimal_value == dp(i-1, t):
            continue
        else:
            selected.append(processes[i-1])
            optimal_value -= processes[i-1][2]
            t -= processes[i-1][1]

    return selected[::-1]
# END OF DP


p = [(1,3,21), (2,6,24), (3,2,12), (4,4,20)] # THESE ARE THE prosseces THE USER SHOULD INPUT THEM TEHE 
# print(schedule_processes(p,8))

op_p=schedule_processes_Exhaustive(p,8)
print('Solution1: ')
print('Selected processes:',[i[0] for i in op_p])
print('total value is',sum(op_p[2] for op_p in op_p))
print('total duration is',sum(op_p[1] for op_p in op_p))

print('Solution2: ')
op_p=schedule_processes_Greedy_Value(p,8)
print('Selected processes:',[i[0] for i in op_p])
print('Greedy choice is MOST VALUE')
print('total value is',sum(op_p[2] for op_p in op_p))
print('total duration is',sum(op_p[1] for op_p in op_p))

print('Solution 3: ')
op_p=schedule_processes_greedy_duration(p,8)
print('Selected processes:',[i[0] for i in op_p])
print('Greedy choice is LEAST DURATION')
print('total value is',sum(op_p[2] for op_p in op_p))
print('total duration is',sum(op_p[1] for op_p in op_p))

print('Solution 4: ')
op_p=process_selection_dp(p,8)
print('Selected processes:',[i[0] for i in op_p])
print('total value is',sum(op_p[2] for op_p in op_p))
print('total duration is',sum(op_p[1] for op_p in op_p))