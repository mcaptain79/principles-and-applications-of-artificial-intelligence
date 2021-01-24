"""
Created on Wed Dec  9 18:56:51 2020

@author: mcaptain79
"""
import copy 
import sys
#making a node class in order to save and retrieve informations better  
class node:
    #all the nodes have their own parent and they heuristic
    def __init__(self,value,parent):
        self.value = value 
        self.heuristic = 0
        self.path = 0 
        self.parent = parent
    def __str__(self):
        return str(self.value)
    def __eq__(self, obj):
        return self.value == obj.value
    #in A* algorithm we sort nodes by heuristic+the path by which they are reached 
    def __lt__(self,obj):
        return self.heuristic+self.path < obj.heuristic+obj.path
#note that getting input is the same as two previous parts
n,m,k = list(map(int,input('enter n,m,k: ').split())) 
#this list saves the initial state of our game and at first it is empty
firstState = []
#we have k regions and we should fill this regions one by one in a for loop
for i in range(k):
    theStr = input('enter region'+str(i+1)+': ')
    if theStr == '#':
        firstState.append('')
    else:
        firstState.append(theStr) 
firstStateNode = node(firstState,None)
"""
this function is similar to check_region
                this just calculate heuristic for one region
"""
def region_heuristic(myStr):
    if myStr == '':
        return 0
    members = myStr.split()
    #numbers list in a string
    numList = []
    for i in members:
        numList.append(int(i[0:len(i)-1]))
    #we have to calculate heuristic depending on paradox in array and colors
    #if the ith number is less than (i+1)th number we add num paradox by one
    numParadox = 0
    for i in range(len(numList)-1):
        if numList[i] < numList[i+1]:
            numParadox += 1
    #returning paradox num
    return numParadox
"""
this function is similar to goal_test it returs sum of heuristic of each region
"""
def node_heuristic(myNode):
    value = myNode.value
    total = 0
    #we have k regions in each node and this value is terminal
    for i in range(k):
        myStr = value[i] 
        total += region_heuristic(myStr)
    return total
#in this function we calculate the distance
def distance_calc(myNode):
    res = 0
    x = myNode.parent
    while x is not None: 
        res += 1 
        x = x.parent
    return res
firstStateNode.heuristic = node_heuristic(firstStateNode)
firstStateNode.path = distance_calc(firstStateNode)
"""
this function just check if a region is ok
        if it was ok it reurns true else returns false
"""
def check_region(myStr):
    if myStr == '':
        return True
    members = myStr.split()
    #numbers list in a string
    numList = []
    #colors list in a string
    colorList = []
    for i in members:
        numList.append(int(i[0:len(i)-1]))
        colorList.append(i[len(i)-1])
    #if numbers not in desc order we return false
    if numList != sorted(numList,reverse = True):
        return False
    #color of every member should the same
    theColor = colorList[0]
    for i in colorList:
        if i != theColor:
            return False
    #if none of above constraints happend then this region is ok and makes no problem
    return True
#a function that tests if a node is a goal state or not
#we have m colors n numbers for colors and k regions
def goal_test(myNode):
    value = myNode.value
    #we have k regions in each node and this value is terminal
    for i in range(k):
        myStr = value[i] 
        #only if one of regions is not ok this state(node) is not goal
        if check_region(myStr) == False:
            return False
    return True
#this is not ready yet
#this function makes children of a given node
#this func needs some modification
def make_children(myNode):
    #value is the list containing regions
    value = copy.copy(myNode.value)
    n = len( value)
    childList = []
    #we should check all the areas with areas that are after the area
    for i in range(n):
        value = copy.copy(myNode.value)
        #we can not make a change to an empty area 
        #if area i is empty we can not move froward
        if value[i] != '': 
            splitholder = value[i].split()
            lastmember = splitholder[len(splitholder)-1]
            #holding number of the last card in area
            #it is all the string except the last char and its color
            inum = int(lastmember[:len(lastmember)-1])
            #we will check all other area
            for j in range(n): 
                value = copy.copy(myNode.value)  
                #we can move in this condition 
                if value[j] == '':
                    if len(splitholder) == 1:
                        #removing spaces that occur at the first and end of string
                        value[j] = value[i]
                        value[i] = ''
                        child = node(value,myNode)
                        child.heuristic = node_heuristic(child)
                        child.path = distance_calc(child)
                        childList.append(child)
                    else:
                        value[j] = lastmember
                        #we dont want the last card 
                        value[i] = value[i].replace(lastmember,'')
                        #removing unneeded spaces
                        value[i] = value[i].strip()
                        child = node(value,myNode)
                        child.heuristic = node_heuristic(child)
                        child.path = distance_calc(child)
                        childList.append(child)
                else:
                    splitholderj = value[j].split()
                    lastmemberj = splitholderj[len(splitholderj)-1]        
                    jnum = int(lastmemberj[:len(lastmemberj)-1])
                    if inum < jnum:  
                        if len(splitholder) == 1: 
                            value[j] = value[j]+' '+value[i]
                            value[i] = '' 
                            child = node(value,myNode)
                            child.heuristic = node_heuristic(child)
                            child.path = distance_calc(child)
                            childList.append(child)
                        else:
                            value[j] = value[j]+' '+lastmember
                            value[i] = value[i].replace(lastmember,'')
                            value[i] = value[i].strip()
                            child = node(value,myNode)
                            child.heuristic = node_heuristic(child)
                            child.path = distance_calc(child)
                            childList.append(child)
    return childList
frontier = [firstStateNode]
explored = []
def Astar():
    global frontier
    if goal_test(firstStateNode):
        print(firstStateNode,' is goal',firstStateNode.path+firstStateNode.heuristic)
        return
    else:
        print(firstStateNode,' is not goal',firstStateNode.path+firstStateNode.heuristic) 
    while True:
        if len(frontier) == 0:
            print('the A* algorithm failed')
            return
        thenode = frontier.pop(0)  
        explored.append(thenode)
        for i in make_children(thenode):
            if i not in explored:
                if goal_test(i): 
                    print(i,' is goal',i.path+i.heuristic)
                    return
                if i not in frontier:
                    print(i,' is not goal',i.path+i.heuristic)  
                    frontier.append(i) 
                else:
                    for k in range(len(frontier)):
                        if i == frontier[k]:
                            if i.path < frontier[k].path:
                                frontier.pop(k)
                                frontier.append(i)
                            break 
        #sorting by heuristic plus path in asc order
        frontier = sorted(frontier)
Astar() 
print('explored: ',len(explored))
print('frontier: ',len(frontier)) 
"""
print('-----------------------------------------')
print('explored nodes: ')
for i in explored:
    print(i,i.heuristic+i.path)
"""

    
    
    
    
    
    
    
    