import sys

#TODO: Actually save processes in memory. queues can just be used as pointers

class Process:
    def __init__(self, instructions= None,priority=99,name=None,parent=None):
        self.parent= parent
        self.priority = priority
        self.instructions = instructions #Instruction is a list of lists which contains the opcodes for the processor to execute. Each list contains the name of the opcode and the arguments/memory adds
        self.finished= False
        pass
    
    
    def operate(self,instruction):
        parent_core = self.parent.parent
        
        parent_core.opcodes[instruction[0]](*instruction[1:]) #Executes the opcode in the core that is parent to this process
       
        
    def step(self):
        try:
            instruction = self.instructions.pop(0)
            self.operate(instruction)
            if self.instructions ==[]:
                self.finished=True
        except Exception as e:
            print(e)
            self.finished=True
        
        
        
        
   
        
        
class Queue:
    def __init__(self,queue=None,organization="fcfs",quantum=1, name = None, move_process=False, processing_method="linear", move_to_next_queue_on_rr=True, priority = 99, calculate_process_wait_time=True, parent=None):
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
        self.parent = parent
        self.priority = priority
        self.current_quantum=0
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
            self.current_quantum+=1
            
            process= self.queue[self.counter%len(self.queue)]
            
            process.step()
            if process.finished:
                
   
                
                if self.counter>=len(self.queue):
                    self.counter=0
                self.queue.pop(self.counter)
                self.out_processes +=1
                self.completed_processes+=1
                
                return None
            else:
                if self.current_quantum %self.quantum ==0:
                    
                    self.counter+=1
            if self.counter>=len(self.queue):
                self.counter=0
                
                
        elif self.processing_method == "linear":
            
            
            process= self.queue[self.counter]
           
            process.step()
           
            
            if process.finished:
                
   
                
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
        
        
           
            
        
class Core:
    def __init__(self,queues_q=0, queues=None,priority="r",processing_method="rr", parent=None):
        self.priority=priority #The priority that the cpu will use
        self.queues = []
        self.counter = 0
        self.processing_method = processing_method
        self.generate_opcodes()
        
        
        if not queues:
            if queues_q:
                for i in range(queues_q):
                    self.queues.append(Queue([],parent=self))
        else:
            self.queues=queues
            if self.priority =="priority":
                self.queues.sort(key = lambda x: x.priority)
            for queue in self.queues:
                queue.parent = self
                
    def generate_opcodes(self):
        
        self.opcodes = {0:None,#idle,
                        1:self.OP_MOV,
    
                        2:self.OP_ADD,
                        3:self.OP_ADC,
                        4:self.OP_SUB,
                        5:self.OP_OR,
                        6:self.OP_AND,
                        7:self.OP_XNOR}#sum op
        
                
                
    def OP_MOV(self,adr,*args):
        if len(args)==1:
            self.parent.memory[adr] = args[0] #SAVES first arg in adr
        else:
          
            self.parent.memory[adr] = self.opcodes[args[0]](*args[1:])  #Saves return of opcode arg0 with arguments *args
             
                
    def OP_ADD(self,x,y):
        
        return self.parent.memory[x] + self.parent.memory[y]
    
    def OP_ADC(self,adr, x,y):
        self.parent.memory[adr] = self.parent.memory[x] + self.parent.memory[y]
        
                
    def OP_SUB(self,x,y):
        return self.parent.memory[x] - self.parent.memory[y]
    def OP_OR(self,x,y):
        
        return bool(self.parent.memory[x]) or bool(self.parent.memory[y]) 
    def OP_AND(self,x,y):
        return bool(self.parent.memory[x]) and bool(self.parent.memory[y])
                                                    
    def OP_XOR(self,x,y):
        return bool(self.parent.memory[x]) != bool(self.parent.memory[y])
    def OP_XNOR(self,x,y):
        return bool(self.parent.memory[x])==bool(self.parent.memory[y])
    
   
                
                
                
                
                
                
                
                
    def queue_processes(self,processes,queue=0):
        
        
        for process in processes:
            process.parent = self.queues[queue]
            self.queues[queue].queue.append(process)  #This queues the process into the queue passed as argument
            
        self.queues[queue].organize()
        
    def process_rr_step(self):
        
        
        queue = self.queues[self.counter%len(self.queues)]
        
        if queue.move_process:
            if queue.queue :
                process = queue.process_step(move_process=True)
                if process:
                   
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

class CPU:
    def __init__(self, cores=None,memory=None,pagsize=None):
        
        if cores:
            self.cores = cores
            for core in self.cores:
                core.parent = self
        else:
            self.cores =[Core()]
            
        if isinstance(memory, int) and pagsize:
            self.memory= [[None]*pagsize]*(memory/pagsize)
        elif isinstance(memory, int):
            
            self.memory = [None]*memory
        elif memory:
            self.memory = memory
        else:
            self.memory = [None]*1024
            
    def process_step(self):
        for core in self.cores:
            core.process()
            self.check_interruption()
    def check_interruption(self):
        pass
    
    def queue_processes(self,processes, core = 0):
        self.cores[core].queue_processes(processes)
    
    def parse(self,instructions):
        ins = []
        for i in instructions.split("\n"):
            ins.append([int(x) for x in i.split(" ")])
        return ins
        
        

#instructions1 = [["01",3,5],["01",1,2]]
#instructions2 = [["01",2,5],["01",3,4]]


core1 = Core(queues=[Queue(quantum=5
                          ,processing_method ="rr"
                          )])

cpu = CPU(cores=[core1],memory=1024)

instructions1 =cpu.parse(
"""01 30 4
01 31 6
03 32 30 31
01 33 02 31 32"""
)


#MOV 30 4
#MOV 31 6
#ADC 31 6
#MOV 33 ADD 31 32
instructions2 =cpu.parse(
"""01 512 100
01 513 101
01 514 02 512 513
01 515 05 513 513
01 516 05 513 517
01 517 06 513 518""")
#MOV 512 100
#MOV 513 101
#MOV 514 ADD 512 513
#MOV 515 OR 513 513
#MOV 516 OR 513 517
#MOV 517 AND 513 518

instructions3 = [[1, 856, 0],[1, 857, 1]]
for i in range(80):
    instructions3.append([1, 858+i,2, 856+i, 857+i])
#fibonacci



processes = [Process(instructions = instructions1)
             ,Process(instructions = instructions2),
             Process(instructions = instructions3)
             ]


cpu.queue_processes(processes)
"""
cpu.process_step()
print(cpu.cores[0].queues)
cpu.process_step()
cpu.process_step()
cpu.process_step()
print(cpu.cores[0].queues)
"""
#print(instructions1)



for i in range(300):
    cpu.process_step()


print(cpu.memory)
print(instructions3)
