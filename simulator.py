# Imports
import sys
import argparse

# Variables

PROCESS_TIME = 2

QUEUES: list[list] = []
QUANTUM: list[int] = []
PROCESS_LIST_FILE = ""
LOG_FILE = ""
OUTPUT_FILE_FORMAT = ""
OUTPUT_FILE = ""

# Logic

def import_tasks_from_file(filepath: str):
    """
    Imports tasks from file and returns them as a list
    """
    tasks = []

    with open(filepath) as file:
        for line in file.readlines():
            task_line = line.split(" ")
            task = [
                task_line[0],
                int(task_line[1]),
                int(task_line[2])
            ]

            if len(task) == 3:
                tasks.append(task)
    
    return tasks


def schedule_tasks(tasks: list):
    """
    Loads task list into queues
    """
    pass

def start_queue_processing():
    """
    Initializes the queue
    """
    pass

def process_queues(tasks: list):
    """
    Processes the queues until every task is finished
    """
    TIME = 0

    while not is_every_queue_empty() or len(tasks) > 0: # Run as long as the queues are not empty and tasks will arrive at some point
        TIME += 1 # Increase the current time
        add_log(f"Time {TIME}:")

        for task in reversed(tasks): # Loop through tasks but in reverse to prevent index skipping when a task is removed from the list
            if task[2] == TIME: # Check if the current task arrives now
                QUEUES[0].append(task) # Add the new task to the end of the queue with the highest priority
                tasks.remove(task) # Remove the task from tasks that will arrive at some point
                add_log(f"  New Task: {task[0]}")

        for queue_id, queue in enumerate(QUEUES): # Loop through all queues
            if len(queue) > 0: # Check for the first not empty queue
                quantum = QUANTUM[queue_id] # Get the quantum of the queue
                task = queue[0] # Get the first task in the queue

                if len(task) == 3: # Check if the task has run in the current quantum
                    task.append(0) # Set the used time of the current quantum to zero

                task[1] -= 1 # decrease the remaining needed CPU time
                task[3] += 1 # increase the time used in the current quantum

                if task[1] == 0: # Check if the task has finished
                    queue.pop(0) # Remove the task from the queue
                    add_log(f"  Task {task[0]} in Queue {queue_id} has finished!")
                    break # Abort the Loop and start from the beginning, this task has finished

                if task[3] == quantum: # Check if the task has used up his time in the current quantum
                    move_task_to_end_of_queue(queue_id) # Move task to the end of the current queue
                    add_log(f"  Task {task[0]} in Queue {queue_id} has exceeded the time quantum, moving it to the end of the queue!")
                
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

    task = queue.pop(0) # Remove the first task from the queue
    if len(task) == 4: # Check if the task still has a time quantum
        del task[3] # Remove the time quantum
    next_queue.append(task) # Readd the task to the end of the next queue


def get_next_scheduled_task():
    """
    Returns the next scheduled task
    """
    pass


def add_log(text: str):
    """
    Adding log entries to console and log file
    """
    print(text)

    if LOG_FILE == "":
        return

    with open(LOG_FILE, "+a") as file:
        file.write(text)

# Main method

def main(args):
    queues = args.queues
    quantum = args.quantum
    
    for i in range(queues):
        QUEUES.append([])

    global QUANTUM
    QUANTUM = quantum

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