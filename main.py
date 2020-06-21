switch=5
if switch!=4:
    print("\tEnter a number corresponding to one of the following choices\n\n \t1)Register Allocation\n \t2)Naive timetable Scheduling \n \t3)Backtrack search Timetable Scheduling \n \t4)Exit\n")
    switch=int(input("\tYour prefered choice is? "))
    if(switch==1):
        #!/usr/bin/python
        import string
        import networkx as nx
        import numpy as np
        import matplotlib.pyplot as plt


        class Graph():

            def __init__(self, vertices):
                self.V = vertices
                self.color_global = [0] * self.V
                self.indp = [0 for row in range(vertices)]
                self.graph = [[0 for column in range(vertices)]\
                                    for row in range(vertices)]

            #function to check if an assigned colour to v is not assigned to one of its neighbours
            def Safe(self, v, colour, c):
                for i in range(self.V):
                    if self.graph[v][i] == 1 and colour[i] == c:
                        return False
                return True
            
            #function to solve 'm' coloring problem recursively     
            def RecGraphColour(self, m, colour, v):
                if v == self.V:
                    return True

                for c in range(1, m+1):
                    if self.Safe(v, colour, c) == True:
                        colour[v] = c
                        if self.RecGraphColour(m, colour, v+1) == True:
                            return True
                        colour[v] = -1
            
            #function to colour given graph and return true if possible  
            def graphColour(self, m,var_list):
                colour = [0] * self.V
                if self.RecGraphColour(m, colour, 0) == False:
                    return False

                isZero = [0 for row in range(self.V)]
                sum = [0 for row in range(self.V)]  
                if colour[0] == -1:
                    return False
                else:
                    print ("")
                    print ("Following are the assigned colours and independent nodes:")

                    # Find maximum number of colours used 
                    colour_max = 0
                    self.color_global = colour
                    for i in range(self.V):
                        if colour_max < colour[i]:
                            colour_max = colour[i]
                            
                    for i in range(self.V):
                        if self.indp[i] == 1:
                            print (var_list[i]," node is independent")
                            self.color_global[i] = 0
                        else:
                            print ("Colour of ",var_list[i]," node is ",colour[i])
                    print ("")          
                    print ("Total number of registers used : ",colour_max)
                    return True
            
            # Finds the vertex of maximum degree in the graph and removes it    
            def reduceGraph(self):
                sum = [0 for row in range(self.V)]
                max_sum = 0
                indx = 0
                for i in range(self.V):
                    for j in range(self.V):
                        sum[i] = sum[i] + self.graph[i][j]
            
                for i in range(self.V):
                    if max_sum <= sum[i]:
                        max_sum = sum[i]
                        indx = i
                
                self.indp[indx] = 1;    
                if max_sum == 0:
                    raw_input("Error")
                for i in range(self.V):
                    self.graph[i][indx] = 0
                    self.graph[indx][i] = 0
                return True 
                        

                        
        # Used to find a list of variables for a given set of tuples, which may contain unordered multiple instances of the same
        def variable_list(tuples):
            var_list = []
            for i in range(0,len(tuples)):
                for j in range(0,len(tuples[i])):
                    if (not tuples[i][j] in var_list):
                        var_list.append(tuples[i][j])       #This appends a variable if it not present in the list
            print("Variable list for given code :",var_list)
            return var_list    


        # This function takes a list of tuples, and the corresponding variable list, and finds out the Adjacency matrix for the formed RIG      
        def adj(var_list, tuples):

            adj_mat = [[0 for x in range(0,len(var_list))] for y in range(0,len(var_list))] #Initialization of Ajdacency matrix 
            for i in range(0,len(tuples)):
                for j in range(0,len(tuples[i])):   #Loop for a variable in a tuple
                    for k in range(0,len(tuples[i])):   #Loop for the second variable in the tuple, between which we are introducing an edge
                        #print var_list.index(tuples[i][j])
                        adj_mat[var_list.index(tuples[i][j])][var_list.index(tuples[i][k])]=1   #For variables appearing together in a tuple, introduces an edge in the graph 

            for i in range(0,len(var_list)):
                adj_mat[i][i]=0     #Diagonal entries removed, since we dont want self loops in our graphs 
            print ("Adjacency Matrix of RIG :",adj_mat)
            return adj_mat

        #for a path in dataflow finds the tuples of live variables at different points of time
        def with_while_rig(tuples):
            out = []
            temp = []
            temp2 = []
            for i in range(len(tuples)):
                for start_check in range(i+1,len(tuples)):
                    # if output variable is reassigned before using it
                    if (tuples[i][0] == tuples[start_check][0]):
                        break
                    else:
                        # outputs are being stored incase if they are being used in next instructions 
                        if (tuples[i][0]!= tuples[start_check][0] and (tuples[i][0] in tuples[start_check])):
                            if (not tuples[i][0] in temp):
                                temp.append(tuples[i][0])
                                break
                                
                #test cases for live variables
                # input variable in one instruction will be decided as live.  
                # 1. If input variable is used without redefining it.
                # 2. If input variable is used in some next instruction, then removed from live variable list.
                # 3. In while loops last outputs are being used in the earlier statements. 
                for j in range(1,len(tuples[i])):
                    if (not tuples[i][j] in temp):
                        temp.append(tuples[i][j])
                    for check_i in range(i+1,len(tuples)):
                        for check_j in range(1,len(tuples[check_i])):
                            temp2.append(tuples[check_i][check_j])
                    for start_check in range(i+1,len(tuples)):
                        if ((tuples[i][j] == tuples[start_check][0] and (tuples[i][0] in tuples[start_check])) or (not tuples[i][j] in temp2)):
                            temp.remove(tuples[i][j])
                            break
                    temp2 =[]
                # either we use the last variable or not anyway it will be a live variable
                if (i == len(tuples)-1 and not (tuples[i][0] in temp)):
                    temp.append(tuples[i][0])
                #print temp,"after i", i+1
                out.append(temp[:])
            return out  

        ##########################################################################################################################################
        #reading from a code file
        f = open('test.txt','r')
        #f = open('test2.txt','r')
        #f = open('test3.txt','r')

        # reading file line by line and omitting while, if-else conditional lines.
        # gives only tuples of variables from the file
        # removes symbols, numerical values
        # only alphabets can be used to form a variable. 
        inp = []
        message = "start"
        while (message[0] != "return"):
            message = f.readline()
            if ("while" in message):
                message = f.readline()
            if ("if" in message):
                message = f.readline()
            if ("else" in message):
                message = f.readline()
            if ("end while" in message):
                message = f.readline()
            if ("end if" in message):
                message = f.readline()
            message = message.translate(str.maketrans('', '', '=+-*/;_'+ string.digits))
            message = message.split()
            inp.append(message)
            #print message
        del inp[-1]
        #print inp
        f.close()

        var = with_while_rig(inp)
        var_list = variable_list(var)

        g = Graph(len(var_list))
        g.graph = adj(var_list,var)

        # decides spilling in RIG
        number_of_registers = 5
        #number_of_registers = 3
        done = 0;
        while done == 0: 
            if g.graphColour(number_of_registers,var_list):
                done = 1;
            else:
                #print "Reducing Graph" 
                g.reduceGraph()
        #raw_input("Finished")
        print ("")
        print ("Finished Register Allocation using Graph Coloring\n")

        colors = g.color_global
        labels = {}
        graphmatrx = np.asarray(g.graph)
        G = nx.from_numpy_matrix(graphmatrx)
        for i in range(len(g.graph)):
            labels[i] = var_list[i] 

        # networkx library is used for building a graph.
        nx.draw(G,labels=labels, with_labels=True,node_size=650,node_color = colors)
        plt.show()
    elif(switch==2):
        import pygame
        import random
        import math
             
        print("PLEASE FILL THE FOLLOWING INFORMATION TO GET THE FINAL SCHEDULE \n \n")
        pygame.init()
        screen=pygame.display.set_mode((800,600))
        pygame.display.set_caption("DSA Project")   
        calendar=pygame.image.load('calendar.png')
        fontpermanent = pygame.font.Font('freesansbold.ttf', 32) 
        textpermanent = fontpermanent.render('EXAM SCHEDULING', True, (0,0,0))

        file=open('courses.txt','w')
        n=int(input("Enter number of courses"))        
        code=[]
        course=[]
        for i in range(n):
            code+=[int(input("Enter Course Code"))]
            course+=[input("Enter Subject Names")]
            file.write(str(code[i])+" "+course[i])
            file.write("\n")
        print("SNo. Code Course")
        file.close()
        file=open('input.txt','w')

        for i in range(n):
            print(i,"  ",code[i],"  ",course[i])

        running=True


        class button():
            def __init__(self, color):
                self.color = color

            def draw(self):    
                pygame.draw.rect(screen, self.color, (320,250,200,140),0)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render("CLICK BUTTON TO ENTER", 1, (0,0,0))
                screen.blit(text, (320 + (100 - text.get_width()/2), 250 + (70 - text.get_height()/2)))

            def isOver(self, pos):
                if pos[0] > 320 and pos[0] < 320 + 200:
                    if pos[1] > 250 and pos[1] < 250 + 140:
                        return True
                    return False

        class boxes():
            def __init__(self, noc,nor):
                self.screensizex=float(800/noc)
                self.screensizey=float(500/nor)
                self.x=0
                self.y=0
                self.color=0
                self.text=""
                self.choice=0
                self.real=0
            def isReal(self):
                if self.real==0:
                    return True
                return False
            def hide(self):
                self.x=math.inf
                self.y=math.inf
            def isFake(self):
                self.real=1
            def reset(self):
                self.choice=0
            def select(self):
                if self.choice==0:
                    self.choice=1
                else:
                    self.choice=0
            def isSelect(self):
                if self.choice==1:
                    return True
                return False
            def colorchange(self,color):
                self.color=color
            def textchange(self,text):
                self.text=text
            def show(self,x=0,y=0):
                self.x=x
                self.y=y
                pygame.draw.rect(screen, self.color, (x,y,self.screensizex,self.screensizey),0)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render(self.text, 1, (0,0,0))
                screen.blit(text, (x + (self.screensizex/2 - text.get_width()/2), y + (self.screensizey/2 - text.get_height()/2)))
            def draw(self):
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render(text, 1, (0,0,0))
                screen.blit(text, (self.x + (self.screensizex/2 - text.get_width()/2), self.y + (self.screensizey/2 - text.get_height()/2)))
            def update(self):
                self.screensizex=150
                self.screensizey=60
            def isOver(self, pos):
                if pos[0] > self.x and pos[0] < self.x + self.screensizex:
                    if pos[1] > self.y and pos[1] < self.y + self.screensizey:
                        return True
                    return False
                    
        enterbutton=button((0,255,0))
        first=True
        second=False
            
        noc=5
        if((n-1)%5==0):
            nor=int((n-1)/5)
        else:
            nor=int((n-1)/5)+1
        screensizex=int(800/noc)
        screensizey=int(500/nor)
            
        countfinal=0
        remaining=[]
        for j in range(n):
            remainingi=[]
            for i in range(n):
                if i==j:
                    continue
                remainingi+=[i]
            remaining+=[remainingi]

        array=[]
        flag=True
        for i in range(n):
            x=random.randrange(0,256)
            y=random.randrange(0,256)
            z=random.randrange(0,256)
            box=boxes(noc,nor)
            box.colorchange((x,y,z))
            box.textchange(str(code[i])+" "+course[i])
            array+=[box]
        for i in range(noc*nor-n+1):
            x=random.randrange(0,256)
            y=random.randrange(0,256)
            z=random.randrange(0,256)
            box=boxes(noc,nor)
            box.isFake()
            box.colorchange((x,y,z))
            box.textchange(" ")
            array+=[box]
            
        while running:
            pos=pygame.mouse.get_pos()
            screen.fill((255,255,255))
            screen.blit(calendar,(20,20))
            screen.blit(textpermanent,(250,40))
            selectedsubject=boxes(noc,nor)
            if second==True:
                selectedsubject.update()
                selectedsubject.colorchange((255,0,0))
                selectedsubject.textchange(str(code[countfinal])+" "+course[countfinal])
                array[countfinal].hide()
                selectedsubject.show(600,20)
                remainingcourse=remaining[countfinal]
                remainingcode=remaining[countfinal]
                countmiddle=0
                for i in range(0,noc):
                    x=i*screensizex
                    for j in range(0,nor):
                        y=j*screensizey+100
                        if countmiddle!=countfinal:
                            array[countmiddle].show(x,y)
                            countmiddle+=1
                        else:
                            countmiddle+=1
                            array[countmiddle].show(x,y)
                            countmiddle+=1
                            
            elif  first==True:
                enterbutton.draw()
            pygame.display.update()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    running=False
                    pygame.quit()
                if event.type==pygame.MOUSEMOTION and first==True:
                    if enterbutton.isOver(pos):
                        enterbutton.color=(255,0,0)
                    else:
                        enterbutton.color=(0,255,0)
                if event.type==pygame.MOUSEBUTTONDOWN and first==True:
                    if enterbutton.isOver(pos):
                        first=False
                        second=True
                        file.write(str(countfinal)+" ")
                elif event.type==pygame.MOUSEBUTTONDOWN and second==True:
                    if selectedsubject.isOver(pos):
                        for i in range(len(array)):
                            if array[i].isReal() and array[i].isSelect():
                                file.write(str(i)+" ")
                            array[i].reset()
                            x=random.randrange(0,256)
                            y=random.randrange(0,256)
                            z=random.randrange(0,256)
                            array[i].colorchange((x,y,z))
                        if countfinal==n-1:
                            running=False
                            pygame.quit()
                        else:
                            countfinal+=1
                            file.write("\n"+str(countfinal)+" ")
                    for i in range(len(array)):
                        if array[i].isOver(pos) and array[i].isReal():
                            array[i].select()
                            if array[i].isSelect:
                                array[i].colorchange((255,0,0))
                            else:
                                x=random.randrange(0,256)
                                y=random.randrange(0,256)
                                z=random.randrange(0,256)
                                array[i].colorchange((x,y,z))
                        
                            
        file.close()
        G=[]
        code=[]
        course=[]
        file=open('courses.txt','r')
        for line in file:
            line=line.strip()
            terms=[]
            for words in line.split(' '):
                terms+=[words]
            code+=[terms[0]]
            course+=[terms[1]]
        file.close()
        file=open('input.txt','r')
        for line in file:
            line=line.strip()
            adjacentVertices=[]
            first=True
            for node in line.split(' '):
                if first:
                    first=False
                    continue
                adjacentVertices.append(int(node))
            G.append(adjacentVertices)
        file.close()
        print(code)
        print(course)
        days=1
        length=len(G)
        color=[0 for i in range(length)]
        schedule=[[]for i in range(length)]
        for i in range(length):
            used=[]
            for j in G[i]:
                if color[j]!=0:
                    used+=[color[j]]
            if used==[]:
                color[i]=1
                schedule[0]+=[i]
            else:
                used.sort()
                num=1
                for j in used:
                    if num==j:
                        num+=1
                        if days<num:
                            days=num
                color[i]=num
                schedule[num-1]+=[i]

        coursecount=[0 for i in range(length) ]   
        for i in range(length):
            pointer=color[i]
            coursecount[pointer-1]+=1
        coursecount.sort()
        coursecount=coursecount[::-1]
        maxcourse=coursecount[0]

        pygame.init()
        screen=pygame.display.set_mode((800,600))
        pygame.display.set_caption("DSA Project")
        calendar=pygame.image.load('calendar.png')
        fontpermanent = pygame.font.Font('freesansbold.ttf', 32) 
        textpermanent = fontpermanent.render('EXAM SCHEDULING', True, (0,0,0))
        running=True
        days+=1
        maxcourse+=1

        print(maxcourse)

        class windowbox():
            def __init__(self,days,maxcourse):
                self.screensizex=float(800/days+1)
                self.screensizey=float(500/maxcourse+1)
            def show(self,text,color,x=0,y=0):
                pygame.draw.rect(screen, color, (x,y,self.screensizex,self.screensizey),0)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render(text, 1, (0,0,0))
                screen.blit(text, (x + (self.screensizex/2 - text.get_width()/2), y + (self.screensizey/2 - text.get_height()/2)))


        while running:
            screen.fill((255,255,255))
            screen.blit(calendar,(20,20))
            screen.blit(textpermanent,(250,40))
            flag=True
            daycount=-1
            schedulecount=-1
            screensizex=float(800/days+1)
            screensizey=float(500/maxcourse+1)
            for i in range(0,days+1):
                x=i*screensizex
                daycount+=1
                flag=not(flag)
                for j in range(0,maxcourse+1):
                    flag=not(flag)
                    schedulecount+=1
                    y=j*screensizey+100
                    if i==0 and j==0:
                        box=windowbox(days,maxcourse)
                        box.show(("SCHEDULE"),(255,0,0),x,y)
                    elif j==0 and flag==False:
                        box1=windowbox(days,maxcourse)
                        box1.show(str(daycount),(0,0,255),x,y)
                    elif j==0 and flag==True:
                        box2=windowbox(days,maxcourse)
                        box2.show(str(daycount),(0,255,0),x,y)
                    elif i==0 and flag==False and j!=0:
                        boxc=windowbox(days,maxcourse)
                        boxc.show(str(schedulecount),(0,0,255),x,y)
                    elif i==0 and flag==True and j!=0:
                        boxv=windowbox(days,maxcourse)
                        boxv.show(str(schedulecount),(0,255,0),x,y)
                    elif flag==True:
                        box3=windowbox(days,maxcourse)
                        text=""
                        if i<=days and j<=len(schedule[i-1]):
                            item=schedule[i-1][j-1]
                            text+=str(code[item])
                            text+=" "
                            text+=course[item]
                        box3.show(str(text),(0,255,0),x,y)
                    elif flag==False:
                        box3=windowbox(days,maxcourse)
                        text=""
                        if i<=days and j<=len(schedule[i-1]):
                            item=schedule[i-1][j-1]
                            text+=str(code[item])
                            text+=" "
                            text+=course[item]
                        box3.show(str(text),(0,0,255),x,y)
            pygame.display.update()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    running=False
        



    elif(switch==3):
        import pygame
        import random
        import math


        def backtrack(assignment):
            if len(assignment)==len(variables):
                return assignment
            var=select_unselected(assignment)
            for value in domain:
                new_assignment=assignment.copy()
                new_assignment[var]=value
                if consistent(new_assignment):
                    result=backtrack(new_assignment)
                    if result is not None:
                        return result
            return None

        def select_unselected(assignment):
            for i in variables:
                if i not in assignment:
                    return i
            return None

        def consistent(assignment):
            for (x,y) in constraints:
                if x not in assignment or y not in assignment:
                    continue
                if assignment[x]==assignment[y]:
                    return False
            return True

          
        print("PLEASE FILL THE FOLLOWING INFORMATION TO GET THE FINAL SCHEDULE \n \n")
        pygame.init()
        screen=pygame.display.set_mode((800,600))
        pygame.display.set_caption("DSA Project")   
        calendar=pygame.image.load('calendar.png')
        fontpermanent = pygame.font.Font('freesansbold.ttf', 32) 
        textpermanent = fontpermanent.render('EXAM SCHEDULING', True, (0,0,0))

        file=open('courses.txt','w')
        n=int(input("Enter number of courses"))        
        code=[]
        course=[]
        for i in range(n):
            code+=[int(input("Enter Course Code"))]
            course+=[input("Enter Subject Names")]
            file.write(str(code[i])+" "+course[i])
            file.write("\n")
        print("SNo. Code Course")
        file.close()
        file=open('input.txt','w')

        for i in range(n):
            print(i,"  ",code[i],"  ",course[i])

        running=True

        class windowbox():
            def __init__(self,days,maxcourse):
                self.screensizex=float(800/days+1)
                self.screensizey=float(500/maxcourse+1)
            def show(self,text,color,x=0,y=0):
                pygame.draw.rect(screen, color, (x,y,self.screensizex,self.screensizey),0)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render(text, 1, (0,0,0))
                screen.blit(text, (x + (self.screensizex/2 - text.get_width()/2), y + (self.screensizey/2 - text.get_height()/2)))



        class button():
            def __init__(self, color):
                self.color = color

            def draw(self):    
                pygame.draw.rect(screen, self.color, (320,250,200,140),0)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render("CLICK BUTTON TO ENTER", 1, (0,0,0))
                screen.blit(text, (320 + (100 - text.get_width()/2), 250 + (70 - text.get_height()/2)))

            def isOver(self, pos):
                if pos[0] > 320 and pos[0] < 320 + 200:
                    if pos[1] > 250 and pos[1] < 250 + 140:
                        return True
                    return False

        class boxes():
            def __init__(self, noc,nor):
                self.screensizex=float(800/noc)
                self.screensizey=float(500/nor)
                self.x=0
                self.y=0
                self.color=0
                self.text=""
                self.choice=0
                self.real=0
            def isReal(self):
                if self.real==0:
                    return True
                return False
            def hide(self):
                self.x=math.inf
                self.y=math.inf
            def isFake(self):
                self.real=1
            def reset(self):
                self.choice=0
            def select(self):
                if self.choice==0:
                    self.choice=1
                else:
                    self.choice=0
            def isSelect(self):
                if self.choice==1:
                    return True
                return False
            def colorchange(self,color):
                self.color=color
            def textchange(self,text):
                self.text=text
            def show(self,x=0,y=0):
                self.x=x
                self.y=y
                pygame.draw.rect(screen, self.color, (x,y,self.screensizex,self.screensizey),0)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render(self.text, 1, (0,0,0))
                screen.blit(text, (x + (self.screensizex/2 - text.get_width()/2), y + (self.screensizey/2 - text.get_height()/2)))
            def draw(self):
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render(text, 1, (0,0,0))
                screen.blit(text, (self.x + (self.screensizex/2 - text.get_width()/2), self.y + (self.screensizey/2 - text.get_height()/2)))
            def update(self):
                self.screensizex=150
                self.screensizey=60
            def isOver(self, pos):
                if pos[0] > self.x and pos[0] < self.x + self.screensizex:
                    if pos[1] > self.y and pos[1] < self.y + self.screensizey:
                        return True
                    return False
                    
        enterbutton=button((0,255,0))
        first=True
        second=False
            
        noc=5
        if((n-1)%5==0):
            nor=int((n-1)/5)
        else:
            nor=int((n-1)/5)+1
        screensizex=int(800/noc)
        screensizey=int(500/nor)
            
        countfinal=0
        remaining=[]
        for j in range(n):
            remainingi=[]
            for i in range(n):
                if i==j:
                    continue
                remainingi+=[i]
            remaining+=[remainingi]

        array=[]
        flag=True
        for i in range(n):
            x=random.randrange(0,256)
            y=random.randrange(0,256)
            z=random.randrange(0,256)
            box=boxes(noc,nor)
            box.colorchange((x,y,z))
            box.textchange(str(code[i])+" "+course[i])
            array+=[box]
        for i in range(noc*nor-n+1):
            x=random.randrange(0,256)
            y=random.randrange(0,256)
            z=random.randrange(0,256)
            box=boxes(noc,nor)
            box.isFake()
            box.colorchange((x,y,z))
            box.textchange(" ")
            array+=[box]
            
        while running:
            pos=pygame.mouse.get_pos()
            screen.fill((255,255,255))
            screen.blit(calendar,(20,20))
            screen.blit(textpermanent,(250,40))
            selectedsubject=boxes(noc,nor)
            if second==True:
                selectedsubject.update()
                selectedsubject.colorchange((255,0,0))
                selectedsubject.textchange(str(code[countfinal])+" "+course[countfinal])
                array[countfinal].hide()
                selectedsubject.show(600,20)
                remainingcourse=remaining[countfinal]
                remainingcode=remaining[countfinal]
                countmiddle=0
                for i in range(0,noc):
                    x=i*screensizex
                    for j in range(0,nor):
                        y=j*screensizey+100
                        if countmiddle!=countfinal:
                            array[countmiddle].show(x,y)
                            countmiddle+=1
                        else:
                            countmiddle+=1
                            array[countmiddle].show(x,y)
                            countmiddle+=1
                            
            elif  first==True:
                enterbutton.draw()
            pygame.display.update()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    running=False
                    pygame.quit()
                if event.type==pygame.MOUSEMOTION and first==True:
                    if enterbutton.isOver(pos):
                        enterbutton.color=(255,0,0)
                    else:
                        enterbutton.color=(0,255,0)
                if event.type==pygame.MOUSEBUTTONDOWN and first==True:
                    if enterbutton.isOver(pos):
                        first=False
                        second=True
                        file.write(str(countfinal)+" ")
                elif event.type==pygame.MOUSEBUTTONDOWN and second==True:
                    if selectedsubject.isOver(pos):
                        for i in range(len(array)):
                            if array[i].isReal() and array[i].isSelect():
                                file.write(str(i)+" ")
                            array[i].reset()
                            x=random.randrange(0,256)
                            y=random.randrange(0,256)
                            z=random.randrange(0,256)
                            array[i].colorchange((x,y,z))
                        if countfinal==n-1:
                            running=False
                            
                        else:
                            countfinal+=1
                            file.write("\n"+str(countfinal)+" ")
                    for i in range(len(array)):
                        if array[i].isOver(pos) and array[i].isReal():
                            array[i].select()
                            if array[i].isSelect:
                                array[i].colorchange((255,0,0))
                            else:
                                x=random.randrange(0,256)
                                y=random.randrange(0,256)
                                z=random.randrange(0,256)
                                array[i].colorchange((x,y,z))
                        
                            
        file.close()

        G=[]
        code=[]
        course=[]
        file=open('courses.txt','r')
        for line in file:
            line=line.strip()
            terms=[]
            for words in line.split(' '):
                terms+=[words]
            code+=[terms[0]]
            course+=[terms[1]]
        file.close()
        file=open('input.txt','r')
        for line in file:
            line=line.strip()
            adjacentVertices=[]
            first=True
            for node in line.split(' '):
                if first:
                    first=False
                    continue
                adjacentVertices.append(int(node))
            G.append(adjacentVertices)
        file.close()
        print(code)
        print(course)
        days=1
        domain=[]
        dayname=int(input("Enter number of days"))

        for i in range(dayname):
            domain+=[input("Enter Day")]

        constraints=[]
        variables=course

        for i in range(len(G)):
            for j in range(len(G[i])):
                temp=(course[i],course[G[i][j]])
                constraints+=[temp]

        solution=backtrack(dict())
        while solution==None:
            solution={}
            domain=[]
            print("Not enough days")
            dayname=int(input("Enter number of days"))

            for i in range(dayname):
                domain+=[input("Enter Day")]

            solution=backtrack(dict())  
            
        print(solution)

        coursecount={}
        for i in domain:
            coursecount[i]=0

        maxcourse=0

        for i in course:
            pointer=solution[i]
            coursecount[pointer]+=1
            if coursecount[pointer]>maxcourse:
                maxcourse=coursecount[pointer]

        days=dayname

        running=True

        schedule=[]
        for i in domain:
            temp=[]
            for j in range(len(course)):
                if solution[course[j]]==i:
                    temp+=[j]
            schedule+=[temp]
        print(schedule)    
                    
                    

        days+=1
        maxcourse+=1


        while running:
            screen.fill((255,255,255))
            screen.blit(calendar,(20,20))
            screen.blit(textpermanent,(250,40))
            flag=True
            daycount=-1
            schedulecount=-1
            screensizex=float(800/days+1)
            screensizey=float(500/maxcourse+1)
            for i in range(0,days):
                x=i*screensizex
                daycount+=1
                flag=not(flag)
                for j in range(0,maxcourse+1):
                    flag=not(flag)
                    schedulecount+=1
                    y=j*screensizey+100
                    if i==0 and j==0:
                        box=windowbox(days,maxcourse)
                        box.show(("SCHEDULE"),(255,0,0),x,y)
                    elif j==0 and flag==False:
                        box1=windowbox(days,maxcourse)
                        box1.show(str(domain[daycount-1]),(0,0,255),x,y)
                    elif j==0 and flag==True:
                        box2=windowbox(days,maxcourse)
                        box2.show(str(domain[daycount-1]),(0,255,0),x,y)
                    elif i==0 and flag==False and j!=0:
                        boxc=windowbox(days,maxcourse)
                        boxc.show(str(schedulecount),(0,0,255),x,y)
                    elif i==0 and flag==True and j!=0:
                        boxv=windowbox(days,maxcourse)
                        boxv.show(str(schedulecount),(0,255,0),x,y)
                    elif flag==True:
                        box3=windowbox(days,maxcourse)
                        text=""
                        if i<=days and j<=len(schedule[i-1]):
                            item=schedule[i-1][j-1]
                            text+=str(code[item])
                            text+=" "
                            text+=course[item]
                        box3.show(str(text),(0,255,0),x,y)
                    elif flag==False:
                        box3=windowbox(days,maxcourse)
                        text=""
                        if i<=days and j<=len(schedule[i-1]):
                            item=schedule[i-1][j-1]
                            text+=str(code[item])
                            text+=" "
                            text+=course[item]
                        box3.show(str(text),(0,0,255),x,y)
            pygame.display.update()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    running=False
                    pygame.quit()
        



    elif(switch==4):
        print("Quiting")
    else:
        print("ENTER A VALID OPTION")


                



                







