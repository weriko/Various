
class Process:
    def __init__(self, time,priority=99,name=None):
        self.time = time
        self.name=name
        self.priority = priority
        self.wait_time=0
    def __repr__(self):
        if not self.name:
            return f"{self.time} {self.priority}" 
        else:
            return f"{self.name} {self.time} {self.priority}"
            
        
        
class Queue:
    def __init__(self,queue=None,organization="fcfs",quantum=1, name = None, move_process=False, processing_method="linear", move_to_next_queue_on_rr=True, priority = 99, calculate_process_wait_time=True):
        if not queue:
            self.queue = [] #List where processes are stored
        else:
            self.queue=queue
        self.organization= organization #Method to organize the processes (priority, fcfs...)
        self.move_process = move_process #If this is true it moves the process to another queue after finishing
        self.counter = 0 #Counter, to keep track of process in rr
        self.quantum=quantum #Amount of time given by the cpu
        self.name=name 
        self.total_process_time = 0
        self.out_processes = 0
        self.priority = priority
        self.completed_processes = 0
        self.calculate_process_wait_time = calculate_process_wait_time
        self.move_to_next_queue_on_rr = move_to_next_queue_on_rr #if the cpu is using rr on queues, if this is true it will move on to process the next queue, otherwise it will keep processing on this queue
        self.processing_method = processing_method #Way to process the processes (linear, rr...)   
  
    
    def organize(self):
        
        if self.organization=="fcfs":
            
            
            pass
        elif self.organization=="priority":
            self.queue.sort(key=lambda x: x.priority)
            
            
    def process_step(self,**kwargs):
        if self.processing_method =="rr":
            
            
            process= self.queue[self.counter]
            self.total_process_time+=min(self.quantum,process.time)
            process.time-=self.quantum
            
            if process.time<=0:
                
   
                
                if self.counter>=len(self.queue):
                    self.counter=0
                self.queue.pop(self.counter)
                self.out_processes +=1
                self.completed_processes+=1
                
                return None
            else:
                self.counter+=1
            if self.counter>=len(self.queue):
                self.counter=0
                
                
        elif self.processing_method == "linear":
            
            
            process= self.queue[self.counter]
            self.total_process_time+=min(self.quantum,process.time)
            if self.calculate_process_wait_time:
                for i in self.queue:
                    i.wait_time+=min(self.quantum,process.time)
            process.time-=self.quantum
            
            if process.time<=0:
                
   
                
                if self.counter>=len(self.queue):
                    self.counter=0
                self.queue.pop(0)
                self.out_processes +=1
                self.completed_processes+=1
                
                return None
            if kwargs.get("move_process",None):
            
                self.queue.pop(0)
                self.out_processes +=1
                
                return process
    def __repr__(self):
        
        
        if self.name:
            return f"{self.queue} {self.name}"
        else:
            return f"{self.queue}"
        
    def get_info(self):
        try:
            return f"""
{self.name}
Processes that were in the queue -> {self.out_processes} 
Processes that were completed in the queue -> {self.completed_processes}
Total process time -> {self.total_process_time}
Average process time -> {self.total_process_time/self.out_processes}

    """
        except:
            return "Not enough information"
        
        
           
            
        
class CPU:
    def __init__(self,queues_q=0, queues=None,priority="r",processing_method="rr"):
        self.priority=priority #The priority that the cpu will use
        self.queues = []
        self.counter = 0
        self.processing_method = processing_method
        
        if not queues:
            if queues_q:
                for i in range(queues_q):
                    self.queues.append(Queue([]))
        else:
            self.queues=queues
            if self.priority =="priority":
                self.queues.sort(key = lambda x: x.priority)
                print(self.queues)
    def queue_processes(self,processes,queue=0):
        
        
        for process in processes:
            self.queues[queue].queue.append(process)
        self.queues[queue].organize()
        
    def process_rr_step(self):
        
        
        queue = self.queues[self.counter%len(self.queues)]
        
        if queue.move_process:
            if queue.queue :
                process = queue.process_step(move_process=True)
                if process:
                    print(process.time)
                    self.queue_processes([process],queue=(self.counter+1)%len(self.queues))
        else:
            if queue.queue !=[]:
                queue.process_step()
            
        if queue.move_to_next_queue_on_rr or queue.queue==[]:
            self.counter+=1
            
        
    def process(self):
        if self.processing_method=="rr":
            self.process_rr_step()
            
            
    def get_total_ptime(self):
        return sum([x.total_process_time for x in self.queues])
        
        
        
        
cpu = CPU(queues=[Queue(organization="priority",
                        quantum=8, 
                        move_to_next_queue_on_rr=True, 
                        move_process=True, processing_method="linear",
                        name="Queue_0",
                        priority=2),
                  
                  Queue(organization="priority",
                         quantum=16,move_process=True,
                         name="Queue_1",
                         priority=2),
                  
                 Queue(organization="fcfs",
                       quantum=99 ,
                       name="Queue_2",
                       priority=3)],
          )

proccesses_q1= [Process(10,priority=1, name = "P1"),
                Process(15,priority=6, name = "P2"),
                Process(20,priority=2, name = "P3"),
                Process(75,priority=5),
                Process(74,priority=4),
                Process(6,priority=2)  ]


proccesses_q2= [Process(40,priority=1),
                Process(60,priority=7),
                Process(20,priority=2),
                Process(20,priority=5),
                Process(100,priority=2)  ]


proccesses_q3= [Process(5,priority=1),
                Process(15,priority=6),
                Process(6,priority=2)]

cpu.queue_processes(proccesses_q1,queue=0)

cpu.queue_processes(proccesses_q2,queue=1)

cpu.queue_processes(proccesses_q3,queue=2)

for i in range(10):
    print(cpu.queues[0])
    print(cpu.queues[1])
    print(cpu.queues[2])
    print()
    cpu.process()
   
    if i%50==0:
        proccesses_q3= [Process(5,priority=1),
                Process(15,priority=6),
                Process(6,priority=2)]

        cpu.queue_processes(proccesses_q3,queue=0)
        

print(cpu.queues[0].total_process_time)
print(cpu.queues[1].total_process_time)
print(cpu.queues[2].total_process_time)

print(cpu.queues[0].out_processes)
print(cpu.queues[1].out_processes)
print(cpu.queues[2].out_processes)

print(cpu.queues[0].completed_processes)
print(cpu.queues[1].completed_processes)
print(cpu.queues[2].completed_processes)

print(cpu.queues[0].get_info())
print(cpu.queues[1].get_info())
print(cpu.queues[2].get_info())


print(cpu.get_total_ptime())



