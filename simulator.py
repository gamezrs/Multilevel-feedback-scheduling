# Imports
import sys
import argparse

# Variables

TIME = 0
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
            task = line.split(" ")

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
    while not is_every_queue_empty():
        TIME += 1

        for task in tasks: # Loop through tasks
            if task[2] == TIME: # Check if the current task arrives now
                QUEUES[0].append(task) # Add the new task to the end of the queue with the highest priority

        for queue_id, queue in enumerate(QUEUES): # Loop through all queues
            if len(queue) > 0: # Check for the first not empty queue
                quantum = QUANTUM[queue_id] # Get the quantum of the queue
                task = queue[0] # Get the first task in the queue

                if not task[3]: # Check if the task has run in the current quantum
                    task[3] = 0 # Set the used time of the current quantum to zero

                task[1] -= 1 # decrease the remaining needed CPU time
                task[3] += 1 # increase the time used in the current quantum

                if task[1] == 0: # Check if the task has finished
                    queue.pop(0) # Remove the task from the queue

                if task[3] == quantum: # Check if the task has used up his time in the current quantum
                    move_task_to_end_of_queue(queue) # Move task to the end of the current queue
                
                break # Abort the Loop and start from the beginning, a time unit has passed



def is_every_queue_empty():
    for queue in QUEUES:
        if len(queue) > 0:
            return False
    
    return True


def move_task_to_end_of_queue(queue: list):
    task = queue.pop(0)
    del task[3]
    queue.append(task)


def get_next_scheduled_task():
    """
    Returns the next scheduled task
    """
    pass

# Main method

def main(args):
    queues = args.queues
    quantum = args.quantum
    
    for i in range(queues):
        QUEUES.append([])

    QUANTUM = quantum

    PROCESS_LIST_FILE = args.processlistfile
    LOG_FILE = args.logfile
    OUTPUT_FILE_FORMAT = args.outputformat
    OUTPUT_FILE = args.outputfile

    tasks = import_tasks_from_file(PROCESS_LIST_FILE)



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