import numpy as np

class Graph:
    def __init__(self, matrix = None):
        self.matrix = matrix
        self.paths = []
        self.node_list = []
        self.test = []
        self.sums = []
        self.count = 0
        
        
    def solve(self, a, seen=None,tot=0):
        #Gets all posible paths until there is nowhere to move.
        #Cant go to a node twice
        in_count = 0
        t = self.matrix[a]
        if not seen:
            seen=[]
        if a not in seen:

            seen.append(a)
        
        for i in range(t.shape[0]):
           
            if self.matrix[a][i]>0 and i not in seen:
                
                self.count+=1
                in_count+=1
                self.node_list.append(i)
                self.solve(i,seen=seen+[i],tot=tot+self.matrix[a][i]) #Appends the node to the seen list for the current path
        if in_count==0:
            self.sums.append(tot) #Appends the total sum of the path
            self.paths.append(seen) #Appends the path
        
        return 
            
            
                
    def shortest(self,a,b):
        maxi=99
        n =0
        for path in [x for x in self.paths if b in x]:
            
            count = 0
            current = a
            for i in range(len(path)-1):
                temp = self.matrix[path[i]][path[i+1]]
                count+=temp
                if path[i]==b:
                    #print(b)
                    break

                
            if count<maxi:
                maxi=count
                n=path
        return maxi,n
                
                
            
    def shortest_distance(self,a,b):
        matrix_node = self.matrix[a]
        self.solve(a)
      
        #print(self.paths)
        #print(self.sums)
        print(self.shortest(a,b))
        return 0
        
        
        
        
    
    
m = np.array([[0,4,0,5,0,0,2,0],
              [4,0,5,0,0,0,1,0],
              [0,5,0,0,0,1,0,1],
              [5,0,0,0,2,0,1,0],
              [0,0,0,2,0,1,0,3],
              [0,0,1,0,1,0,0,2],
              [2,1,0,1,0,0,0,0],
              [0,0,1,0,3,2,0,0]])
graph = Graph(m)

print(graph.shortest_distance(0,7))
print(graph.paths)