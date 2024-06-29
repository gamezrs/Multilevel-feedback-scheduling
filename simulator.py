# Imports
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Task Class

class Task:
    def __init__(self, name, runtime, arrivaltime):
        self.name = name # Name of the task
        self.needed_runtime = runtime # Runtime from the task file
        self.remaining_runtime = runtime # Remaining runtime, will be decreased by the scheduler
        self.arrivaltime = arrivaltime # Arrivaltime from the task file

        self.waittime = 0 # Waittime, will be increased by the scheduler
        self.real_runtime = 0 # The time that the task had the CPU, will be increased by the scheduler
        self.quantum = 0 # The time used in the current quantum, will be increased by the scheduler

        self.quantum_exceedings = [] # All the times, that the task exceeded the time quantum
        self.finishtime = 0 # The timepoint where the task has finished

# Logic

def import_tasks_from_file(filepath: str):
    """
    Imports tasks from file and returns them as a list
    """
    tasks: list[Task] = [] # Create a list to holds all imported tasks

    with open(filepath) as file: # Open the tasks file
        for line in file.readlines(): # Loop through all lines in the task file
            task_line = line.split(" ") # Split the line in to a list

            if len(task_line) == 3: # Check if the line has 3 seperate attributes
                task = Task(task_line[0], int(task_line[1]), int(task_line[2])) # Create a new task
                tasks.append(task) # Add the task to the list of all tasks
    
    return tasks # Return the list of tasks


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
    task.quantum_exceedings.append([TIME, queue_id, next_queue]) # Save info about the exceeding of the quantum time

    next_queue.append(task) # Readd the task to the end of the next queue

    add_log(f"  Task {task.name} in Queue {queue_id} has exceeded the time quantum, moving it to the end of the queue!")


def remove_task_from_queue(queue_id: int):
    """
    Removes the first task of a queue when it has finished running
    """
    task = QUEUES[queue_id].pop(0) # Remove the task from the queue
    task.real_runtime = TIME - task.arrivaltime # Calculate the time that the process was running with waiting times
    task.waittime = task.real_runtime - task.needed_runtime # Calculate the time the process was waiting for the CPU
    task.finishtime = TIME # Save the time when the process finished
    FINISHED_TASKS.append(task) # Add it to the list with finished tasks
    add_log(f"  Task {task.name} in Queue {queue_id} has finished!")


def add_log(text: str):
    """
    Adding log entries to console and log file
    """
    print(text) # Log to the console

    with open(LOG_FILE, "+a") as file: # Open the log file
        file.write(text + "\n") # Write to the log file


def output_simulation():
    """
    Saves the output of the simulation to a text file
    """
    text = ""

    average_real_runtime = 0
    average_waittime = 0

    for task in FINISHED_TASKS: # Loop through all finished tasks
        average_real_runtime += task.real_runtime # Add the runtime of the task to the summed runtime
        average_waittime += task.waittime # Add the waittime of the task to the summed waittime

        text = text + f"{task.name} finished after running for {task.real_runtime}s with a waiting time of {task.waittime}s\n" # Create the text line for the current task
    
    average_real_runtime = average_real_runtime / len(FINISHED_TASKS) # Divide the summed runtime by the amount of tasks to get the average runtime
    average_waittime = average_waittime / len(FINISHED_TASKS) # Divide the summed waittime by the amount of tasks to get the average waittime

    text = text + f"\n\nAverage runtime: {average_real_runtime}s\nAverage waittime: {average_waittime}s" # Create the text line for the average runtime and average waittime

    with open(OUTPUT_FILE, "+w") as file: # Open the output file
        file.write(text) # Write to the output file


def output_gantt_chart():
    """
    Saves the output of the simulation to a gantt chart
    """
    data = [] # Create a list to hold the necessary data of the tasks

    for task in FINISHED_TASKS: # Loop through all finished tasks
        data.append(dict(task=task.name, start=task.arrivaltime, runtime=task.real_runtime)) # Add the necessary data from the task to the data list

    dataframe = pd.DataFrame(data) # Create a panda dataframe

    plt.barh(y=dataframe['task'], left=dataframe['start'], width=dataframe['runtime']) # Create a gantt chart with the runtime of the tasks
    plt.savefig(OUTPUT_IMAGE) # Save the gantt chart to a png file

# Main method

def main(args):
    global TIME
    global FINISHED_TASKS
    global QUEUES
    global QUANTUM
    global PROCESS_LIST_FILE
    global LOG_FILE
    global OUTPUT_FILE
    global OUTPUT_IMAGE

    TIME = 0
    FINISHED_TASKS = []
    QUEUES = []
    
    for i in range(args.queues): # Add the defined amount of queues
        QUEUES.append([])
    
    QUANTUM = args.quantum
    PROCESS_LIST_FILE = args.processlistfile
    LOG_FILE = args.logfile
    OUTPUT_FILE = args.outputfile
    OUTPUT_IMAGE = args.outputimage

    if len(args.quantum) < args.queues: # Check if there are less quantums then there are queues
        print("Not every queue has a quantum") # print an error message
        return # Abort the program

    tasks = import_tasks_from_file(PROCESS_LIST_FILE) # Import the Tasks

    process_queues(tasks) # Process the tasks
    output_simulation() # Output the simulation to a text file
    output_gantt_chart() # Output a gantt chart to a png file


# Entrypoint

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--queues", help="amount of queues", required=True, type=int)
    parser.add_argument("--quantum", help="time quantum of queue in seconds, seperated by whitespace", required=True, type=int, nargs="+")
    parser.add_argument("--processlistfile", help="path to the process list file for import", required=True, type=str)
    parser.add_argument("--logfile", help="path to the log file", required=True, type=str)
    parser.add_argument("--outputfile", help="path to the output file of the simulation", required=True, type=str)
    parser.add_argument("--outputimage", help="path to the output png image of the simulation", required=True, type=str)

    args = parser.parse_args()

    main(args)