# Imports
import sys
import argparse

# Task Class

class Task:
    def __init__(self, name, runtime, arrivaltime):
        self.name = name
        self.needed_runtime = runtime
        self.remaining_runtime = runtime
        self.arrivaltime = arrivaltime

        self.waittime = 0
        self.real_runtime = 0
        self.quantum = 0

# Logic

def import_tasks_from_file(filepath: str):
    """
    Imports tasks from file and returns them as a list
    """
    tasks: list[Task] = []

    with open(filepath) as file:
        for line in file.readlines():
            task_line = line.split(" ")

            if len(task_line) == 3:
                task = Task(task_line[0], int(task_line[1]), int(task_line[2]))
                tasks.append(task)
    
    return tasks


def process_queues(tasks: list):
    """
    Processes the queues until every task is finished
    """
    global TIME

    while not is_every_queue_empty() or len(tasks) > 0: # Run as long as the queues are not empty and tasks will arrive at some point
        TIME += 1 # Increase the current time
        add_log(f"Time {TIME}:")

        for task in reversed(tasks): # Loop through tasks but in reverse to prevent index skipping when a task is removed from the list
            if task.arrivaltime == TIME: # Check if the current task arrives now
                QUEUES[0].append(task) # Add the new task to the end of the queue with the highest priority
                tasks.remove(task) # Remove the task from tasks that will arrive at some point
                add_log(f"  New Task: {task.name}")

        for queue_id, queue in enumerate(QUEUES): # Loop through all queues
            if len(queue) > 0: # Check for the first not empty queue
                quantum = QUANTUM[queue_id] # Get the quantum of the queue
                task = queue[0] # Get the first task in the queue

                task.remaining_runtime -= 1 # decrease the remaining needed CPU time
                task.quantum += 1 # increase the time used in the current quantum

                if task.remaining_runtime == 0: # Check if the task has finished
                    remove_task_from_queue(queue_id) # Remove the task from the queue
                    break # Abort the Loop and start from the beginning, this task has finished

                if task.quantum == quantum: # Check if the task has used up his time in the current quantum
                    move_task_to_end_of_queue(queue_id) # Move task to the end of the current queue
                    break # Abort the Loop and start from the beginning, the time quantum has been reached
                
                break # Abort the Loop and start from the beginning, a time unit has passed


def is_every_queue_empty():
    """
    Checks whether or not every queue is empty
    """
    for queue in QUEUES: # Loop through all queues
        if len(queue) > 0: # Check if a non empty queue is found
            return False # return false because not every queue is empty
    
    return True # No queue has a task in them, every queue is empty


def move_task_to_end_of_queue(queue_id: int):
    """
    Moves the first task of a queue to a lower priority queue if there is one, readds it to the end of the current queue if there is no lower priority queue
    """
    queue = QUEUES[queue_id] # Get the queue that the task is from

    if len(QUEUES) == queue_id + 1: # Check if the current queue is the one with the lowest priority
        next_queue = QUEUES[queue_id] # Get the current queue, as there is no lower priority queue
    else: # There is a lower priority queue
        next_queue = QUEUES[queue_id + 1] # Get the next lowest priority queue

    task = queue.pop(0) # Remove the first task from the queu
    task.quantum = 0 # Remove the time quantum

    next_queue.append(task) # Readd the task to the end of the next queue

    add_log(f"  Task {task.name} in Queue {queue_id} has exceeded the time quantum, moving it to the end of the queue!")


def remove_task_from_queue(queue_id: int):
    """
    Removes the first task of a queue when it has finished running
    """
    task = QUEUES[queue_id].pop(0) # Remove the task from the queue
    task.real_runtime = TIME - task.arrivaltime # Calculate the time that the process was running with waiting times
    task.waittime = task.real_runtime - task.needed_runtime # Calculate the time the process was waiting for the CPU
    FINISHED_TASKS.append(task) # Add it to the list with finished tasks
    add_log(f"  Task {task.name} in Queue {queue_id} has finished!")


def add_log(text: str):
    """
    Adding log entries to console and log file
    """
    print(text)

    if LOG_FILE == "":
        return

    with open(LOG_FILE, "+a") as file:
        file.write(text + "\n")

# Main method

def main(args):
    global TIME
    global FINISHED_TASKS
    global QUEUES
    global QUANTUM
    global PROCESS_LIST_FILE
    global LOG_FILE
    global OUTPUT_FILE_FORMAT
    global OUTPUT_FILE

    TIME = 0
    FINISHED_TASKS = []
    QUEUES = []
    
    for i in range(args.queues):
        QUEUES.append([])
    
    QUANTUM = args.quantum
    PROCESS_LIST_FILE = args.processlistfile
    LOG_FILE = args.logfile
    OUTPUT_FILE_FORMAT = args.outputformat
    OUTPUT_FILE = args.outputfile

    tasks = import_tasks_from_file(PROCESS_LIST_FILE)

    process_queues(tasks)


# Entrypoint

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--queues", help="amount of queues", type=int)
    parser.add_argument("--quantum", help="time quantum of queue in seconds, seperated by whitespace", type=int, nargs="+")
    parser.add_argument("--processlistfile", help="path to the process list file for import")
    parser.add_argument("--logfile", help="path to the log file")
    parser.add_argument("--outputformat", help="output format (text, image)")
    parser.add_argument("--outputfile", help="path to the output file of the simulation")

    args = parser.parse_args()

    main(args)