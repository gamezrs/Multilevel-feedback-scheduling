# Imports
import sys
import argparse

# Variables

QUEUES = []
QUANTUM = []
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


def schedule_tasks(tasks: dict):
    """
    Loads task dict into queues
    """
    pass

def start_queue_processing():
    """
    Initializes the queue
    """
    pass

def process_queues():
    """
    Processes the queues until every task is finished
    """

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