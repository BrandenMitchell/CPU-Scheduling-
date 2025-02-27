#Branden Mitchell
#CPU Scheduling hw



#----------------the code marked by these lines was coded by Proffessor Dr.Adu Baffour and given to his students to use in document "shortest_remaining_time_algorithm.ipynb" in Modeule 3----------------------------------------#
# Process class to represent a single process
class Process:
  
  def __init__(self, pid, arrival_time, burst_time, priority):
    self.pid = pid # unique process id
    self.arrival_time = arrival_time # time at which the process arrives
    self.burst_time = burst_time # total cpu time required by the process
    self.priority = priority # priority of the process
    self.completion_time = 0
    self.turnaround_time = 0
    self.waiting_time = 0
    self.remaining_time = burst_time


  def calculate_turnaround_time(self):
    self.turnaround_time = self.completion_time - self.arrival_time

  def calculate_waiting_time(self):
    self.waiting_time = self.turnaround_time - self.burst_time


# Implement the SJF funciton
def shortest_job_first(processes_data):
  
  # Convert the input data into Process objects
  # Sort them by Burst time since it executes the smallest burst time first 
  processes = [Process(*p) for p in processes_data]
  
  total_turnaround_time = 0
  total_waiting_time = 0
  curr_time = 0
  avg_turnaround_time = 0
  avg_waiting_time = 0
  completed_processes = 0
  ready_queue = []

  while completed_processes < len(processes):
    for process in processes:
       if process.arrival_time <= curr_time and process not in ready_queue and process.completion_time ==0 :
          ready_queue.append(process)
    if ready_queue:
      #sort ready queue on burst time bc sjf algo
      ready_queue.sort(key =lambda x : x.burst_time)
      #grab first process in queue
      curr_process = ready_queue.pop(0)
      #calc start time 
      start_time = max(curr_time, curr_process.arrival_time)
      #calc completion time 
      curr_process.completion_time = start_time + curr_process.burst_time
      #update current time
      curr_time = curr_process.completion_time
      #calc turnaround time 
      curr_process.calculate_turnaround_time()
      curr_process.calculate_waiting_time()
      
      # increment the turnaround and waiting totals
      total_turnaround_time += curr_process.turnaround_time
      total_waiting_time += curr_process.waiting_time
      completed_processes += 1
    else:
       #no processes are ready so increment time
       curr_time += 1

    
  #calc avg turnaround and waiting times
  avg_turnaround_time = total_turnaround_time / len(processes)
  avg_waiting_time = total_waiting_time / len(processes)

  print("Shortest Job First Algorithm: \n")
  #print process information 
  for process in processes:
      print(f"Process {process.pid}: Arrival Time = {process.arrival_time}, "
            f"Burst Time = {process.burst_time}, Completion Time = {process.completion_time}, "
            f"Turnaround Time = {process.turnaround_time}, Waiting Time = {process.waiting_time}")
  
  #print turnaround and waiting time averages 
  
  print(f"\nAverage Turnaround Time: {avg_turnaround_time}")

  print(f"Average Waiting Time: {avg_waiting_time}")
  print("-------------------------------------")




# Implement the SRT function
def shortest_remaining_time(processes_data):

  # Convert the input data into Process objects
  # Sort them by arrival time
  processes = [Process(*p) for p in processes_data]
  processes.sort(key=lambda x: x.arrival_time)

  # Initialize scheduling variables
  current_time = 0 # Track current time in simulation
  completed_processes = [] # Store processes that have finished running
  ready_queue = [] # Store processes that have arrived but not completed
  gantt_chart = [] # Store the execution timeline

  # check and add any newly arrived process to the ready queue
  def update_ready_queue():
    for process in processes:
      if(process.arrival_time <= current_time and
         process not in ready_queue and
         process not in completed_processes):
        ready_queue.append(process)

  # Find out when the next process will arrive
  def get_next_arrival_time():
    # get all processes that are in the ready queue
    # who's arrival time is in the future
    future_arrivals = [p.arrival_time for p in processes
                       if p.arrival_time > current_time and
                       p not in completed_processes]

    # return the earliest arrival time, or infinity if no more arrivals
    return min(future_arrivals) if future_arrivals else float('inf')


  # Main scheduling loop - continue until all processes are completed
  while len(completed_processes) < len(processes):

    # Step 1: Update the ready queue with any newly arrived process
    update_ready_queue()

    # Step 2: Handle case when no processes are ready to execute
    if not ready_queue:
      # Find the next process arrival time
      next_arrival = get_next_arrival_time()
      if current_time < next_arrival:
        # System will be idle
        gantt_chart.append(['IDLE'])
        current_time = next_arrival
      continue

    # Step 3: Select the process with the shortest remaining time
    # If tie, we will use arrival time as the arbitration rule
    current_process = min(ready_queue,
                          key=lambda p: (p.remaining_time, p.arrival_time))

    # Step 4: Calculate the time slice
    next_arrival = get_next_arrival_time()
    time_slice = min(
        current_process.remaining_time,
        next_arrival - current_time
    )

    # Step 5: Execute processes for the calculated time slice
    start_time = current_time # record the start time
    current_time += time_slice # advance the system clock
    current_process.remaining_time -= time_slice # update remaining time

    # update Gantt chart
    if not gantt_chart or gantt_chart[-1][0] != current_process.pid:
      # start a new entry if different process or first entry
      gantt_chart.append([current_process.pid, start_time, current_time])
    else:
      # update end time of current entry if same process
      gantt_chart[-1][2] = current_time

    # Step 6: Check if process has completed
    if current_process.remaining_time == 0:
      # update completion metrics
      current_process.completion_time = current_time

      # Turnaround time = completion time - arrival
      current_process.turnaround_time = (current_process.completion_time -
                                         current_process.arrival_time)

      # waiting time
      current_process.waiting_time = (current_process.turnaround_time -
                                      current_process.burst_time)

      # terminate the process
      # move it from the ready queue to the completed queue
      completed_processes.append(current_process)
      ready_queue.remove(current_process)

  return completed_processes, gantt_chart



def print_results(completed_processes, gantt_chart):
    """Print formatted scheduling results and metrics."""
    # Print Gantt chart showing execution order
    print("\nProcess Execution Order (Gantt Chart):")
    print("-" * 50)
    for entry in gantt_chart:
        if entry[0] == "IDLE":
            # Show idle time periods
            print(f"IDLE: {entry[1]} -> {entry[2]}")
        else:
            # Show process execution periods
            print(f"P{entry[0]}: {entry[1]} -> {entry[2]}")

    # Print detailed process metrics
    print("\nProcess Scheduling Details:")
    print("-" * 65)
    print("PID  Arrival  Burst  Completion  Turnaround  Waiting")
    print("-" * 65)

    # Print metrics for each process, sorted by PID
    for p in sorted(completed_processes, key=lambda x: x.pid):
        print(f"{p.pid:<5}{p.arrival_time:<9}{p.burst_time:<7}"
              f"{p.completion_time:<12}{p.turnaround_time:<12}"
              f"{p.waiting_time}")

    # Calculate and print average metrics
    avg_turnaround = sum(p.turnaround_time for p in completed_processes) / len(completed_processes)
    avg_waiting = sum(p.waiting_time for p in completed_processes) / len(completed_processes)

    print("-" * 65)
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")

#----------------the code marked by these lines was coded by Proffessor Dr.Adu Baffour and given to his students to use, From document "shortest_remaining_time_algorithm.ipynb" in Modeule 3----------------------------------------#


processes = [[1, 0, 3, 1],
             [2, 2, 6, 1],
             [3, 4, 4, 1],
             [4, 6, 5, 1],
             [5, 8, 2, 1]]


completed_processes, gantt_chart = shortest_remaining_time(processes)

shortest_job_first(processes)
print_results(completed_processes, gantt_chart)



