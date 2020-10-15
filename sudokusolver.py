import numpy as np
class Sudoku:
    def __init__(self,grid=None, order =3):
        if type(grid) == None:
            self.grid=np.zeros((9,9))
        else:
            self.grid =grid
        self.s = 0
        self.stop=False
        self.order = order
    def check_square(self,pos,n):
        sqf = pos[0]//self.order #Get 0  if in first square, 1 if in second square, 2 if in third square...
        sqc = pos[1]//self.order
        current = self.grid[sqf*self.order:sqf*self.order+self.order:1,   sqc*self.order:sqc*self.order+3]
        #print(current)
        if n in current.flatten():
            return False
        else:
            return True
    def check_lines(self,pos,n):
        currentf = self.grid[:,pos[1]]
        currentc = self.grid[pos[0],:]
        
        #print(currentf)
        #print(currentc)
        return  (n not in currentf and n not in currentc)
    
    def solve(self):
         
        for i in range(self.order**2):
            for j in range(self.order**2):
                if self.grid[i][j] == 0  :
                    for k in range(1,self.order**2+1):
                        if (self.check_lines((i,j),k) and self.check_square((i,j),k)) and not self.stop:
                            self.grid[i][j]=k
                            self.s+=1
                            if self.s%10000==0:
                                print(self.grid)
                            self.solve() 
                            self.grid[i][j]=0 #IF this k creates conflict (makes the grid unsolvable) then it will set all the values above the k creating conflict to 0, and it will try with the next number for that k
                    return      #so if lets say the value 5 made the grid unsolvable, it will try with 6 and it will do the whole process again
            
        print(self.grid, self.s)
        
        self.stop=True
                
                    
    
grid = np.array([[5,3,0,0,7,0,0,0,0],
                 [6,0,0,1,9,5,0,0,0],
                 [0,9,8,0,0,0,0,6,0],
                 [8,0,0,0,6,0,0,0,3],
                 [4,0,0,8,0,3,0,0,1],
                 [7,0,0,0,2,0,0,0,6],
                 [0,6,0,0,0,0,2,8,0],
                 [0,0,0,4,1,9,0,0,5],
                 [0,0,0,0,8,0,0,7,9]])
grid=np.zeros((9,9))
print(grid)
sudoku = Sudoku(grid=grid, order =3)
#print(sudoku.check_square((2,2),2))
#print(sudoku.check_lines((1,1),2))
sudoku.solve()

print(sudoku.s)
