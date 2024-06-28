# Imports
import sys
import argparse

# Variables

QUEUES = []

# Logic

def import_tasks_from_file(filepath: str):
    """
    Imports tasks from file
    """
    pass

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
    pass

# Entrypoint

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-queues", help="amount of queues")
    parser.add_argument("-quantum", help="time quantum of queue in seconds, seperated by whitespace")
    parser.add_argument("-processlistfile", help="path to the process list file for import")
    parser.add_argument("-logfile", help="path to the log file")
    parser.add_argument("-outputformat", help="output format (text, image)")
    parser.add_argument("-outputfile", help="path to the output file of the simulation")

    args = parser.parse_args()

    main(args)