import random
from random import randint
import csv
import operator 
import collections
class Person(object):
    #=========CONSTRUCTORS==========    
    #x if the row index, y is the column index, state is an int indicate the health condition
    #state=0 healthy(green), state=1 being infected(yellow), state=2 infected state=2+50=52 dead
    #Currently the time between getting infected to dead is set to 50===========================
        
    def __init__(self, state):
        self.state = state
    
    #=========OBSERVERS==========
    #return the health state of a person 
    def checkState(self):
        return self.state
    #=========MODIFIERS==========
    #return the health state of a person 
    def changeState(self, my_state):
        self.state = my_state
    
class Population(object):
    #=========CONSTRUCTORS==========    
    def __init__(self, maxX, maxY):
        self.maxX = maxX
        self.maxY = maxY
        self.data = [[[None] for i in range(maxY)] for j in range(maxX)]
    
    #=========OBSERVERS========== 
    #count the number of adjacent infected people    
    def countAdj(self, x, y):
        count =0
        #case 0: no person at x,y
        if (self.data[x][y]==None):
            return -1       
        else:
            neighbors = lambda x,y : [(x2, y2) for x2 in range(x-1,x+2) for y2 in range(y-1,y+2)
                                    if (0<=x2<self.maxX) and (0<=y2<self.maxY) and (x==x2 or y==y2)]
            for each in neighbors(x,y):
                my_x = each[0]
                my_y = each[1]
                if self.data[my_x][my_y] != [None] and self.data[my_x][my_y].checkState() >= 2:
                    count += 1
            return count
    
    
    #highlight the most critical areas for vaccine-targeting
    def eval(self, new_infected):
        my_dict = {}
        my_lst = []
        
        for item in new_infected:
            neighbors = lambda x,y : [(x2, y2) for x2 in range(x-1,x+2) for y2 in range(y-1,y+2)
                        if (0<=x2<self.maxX) and (0<=y2<self.maxY) and (x==x2 or y==y2) and not (x==x2 and y==y2)]
            for each in neighbors(item[0],item[1]):
                if self.data[each[0]][each[1]] != [None] and self.data[each[0]][each[1]].checkState() >= 2:
                    if each in my_dict:
                        my_dict[each] += 1
                    else:
                        my_dict[each] = 1
        for each in my_dict:
            if my_dict[each] >= 1:
                my_lst.append(each)
        return my_lst
    
    
    
    #=========MODIFIERS==========
    def infect(self,x,y, new_infected):
        #Pre-condition: data[x][y] != None
        if(self.data[x][y] != [None]):
            #case 1: from healthy to being infected
            if (self.data[x][y].checkState()==0 and self.countAdj(x,y)>=2):
                self.data[x][y].changeState(1) 
                new_infected.append((x,y)) 
            #case 2: from being infected to infected
            elif (self.data[x][y].checkState()==1):
                self.data[x][y].changeState(2) 
            #case 3: after getting infected, disease becoming aggrevated if it's not cured
            elif (self.data[x][y].checkState()>=2 and self.data[x][y].checkState()<52):  
                self.data[x][y].changeState(self.data[x][y].checkState()+1)
            else:
                return
        
    def cure(self,x,y):
        if(self.data[x][y] != [None] and self.data[x][y].checkState()>0):
            self.data[x][y].changeState(0)    

    def move(self, x, y):
        #randomly swap population pixels, 
        if(density_map[x/5][y/5] != 0.0 and self.data[x][y] == [None]):
            neighbor = lambda x,y : [(x2,y2) for x2 in range(x-1,x+2) for y2 in range(y-1,y+2)
                                         if (0<=x2<self.maxX) and (0<=y2<self.maxY) and density_map[x2/5][y2/5] >=0.3
                                         and (x2!=x or y2!=y)]
            if len(neighbor(x,y))>0:       
                swap_neighbor = random.choice(neighbor(x,y))
                swap_x = swap_neighbor[0]
                swap_y = swap_neighbor[1]
                self.data[x][y] = self.data[swap_x][swap_y]
                self.data[swap_x][swap_y] = [None]
                
#INITIALIZATION OF THE POPULATION SYSTEM                            
global cell_width, cell_gap, my_population, denstiy_map, new_infected, highlight_lst
canvas_width = 1600
canvas_height = 600
cell_width = 4
cell_gap = 1
density_map = []
new_infected = []
highlight_lst = []

#Read CSV file and load the density data
with open('density and outbreak.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    current_i = -1
    for row in csv_reader:
        if line_count != 0:
            if int(row[0]) != current_i:
                density_map.append([])
                current_i = int(row[0])
            density_map[current_i].append(float(row[2]))
        line_count += 1
 
unit_size = cell_width + cell_gap
num1 = canvas_width / unit_size
num2 = canvas_height / unit_size
my_population = Population(num1, num2)
for i in range(num1):
    for j in range(num2):
        #Probability of the outbreak of plauge        
        if(density_map[i/5][j/5] != 0):
            threshold = int(float(density_map[i/5][j/5])*10)
            prob = randint(0, 10)
            if(prob <= threshold):    
                outbreak = randint(0,10) 
                if(outbreak==0):
                    my_population.data[i][j] = Person(2)  
                else:
                    my_population.data[i][j] = Person(0)

          
def setup():
    frameRate(96)
    size (canvas_width,canvas_height)
    smooth()
    background(255)

        
def draw():    
    global cell_width, cell_gap, my_population, img, new_infected, highlight_lst
    noStroke()
    # stroke (127)
    # strokeWeight(1)
    # strokeCap(SQUARE)    
    background(255)   
    
    #display of the population    
    for i in range(num1):
        for j in range(num2):
            #CHECK NULL
            if (my_population.data[i][j] != None and my_population.data[i][j] != [None]):
                if (my_population.data[i][j].checkState() == 0):
                    # fill(0,255,0)
                    if random.uniform(0,1)<0.8:
                        fill(200,200,255) #COLOR 1
                    else:
                        fill(61,153,252) #COLOR 2
                    rect(i*unit_size, j*unit_size, cell_width, cell_width)                    
                elif(my_population.data[i][j].checkState() == 1):
                    fill(0,255,0) #COLOR 3
                    rect(i*unit_size, j*unit_size, cell_width, cell_width)
                #ADD DIFFERENT GRADIENT OF RED
                elif(my_population.data[i][j].checkState() >= 2 and my_population.data[i][j].checkState() < 52):
                    # delta = my_population.data[i][j].checkState()-2
                    # fill(255-delta*5,0,0)
                    fill(255,92,58) #COLOR 4                                    
                    rect(i*unit_size, j*unit_size, cell_width, cell_width)
                elif(my_population.data[i][j].checkState() ==52): 
                    fill(127) #COLOR 5: MEDIUM GREY
                    rect(i*unit_size, j*unit_size, cell_width, cell_width)
                else:
                    print("Exception")

                if ((i,j) in highlight_lst):
                    fill(255,56,56) #COLOR 6
                    rect(i*unit_size, j*unit_size, cell_width, cell_width) 
                    fill(0,0,255)

    new_infected = [] 
    highlight_lst = []  
                    
    for i in range(num1):
        for j in range(num2):
            my_population.infect(i,j,new_infected)
            #cure rate = 10%
            if random.uniform(0,1) < (10.0/100.0):
                my_population.cure(i,j)     
            
    for i in range(num1):
        for j in range(num2):
            #population fluidity = 50%
            if random.uniform(0,1) < (50.0/100.0):
                my_population.move(i,j)
                
    highlight_lst = my_population.eval(new_infected)
    
    title()  
    # saveFrame("outputD/plagueD_####.png")  
    
def title():
    fill(0);
    textSize(16);
    text("Cure Rate=10% \nPopulation Fluidity=50%", 30, 30); 
