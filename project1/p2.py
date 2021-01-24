"""
Created on Thu Dec  3 19:16:10 2020

@author: mcaptain79
"""
"""
Created on Fri Nov 20 14:09:36 2020

@author: mcaptain79 
"""
import copy
import sys
#making a node class in order to save and retrieve informations better
class node:
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def __eq__(self, obj):
        if obj is not node:
            return False
        return self.value == obj.value
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
firstStateNode = node(firstState)
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
                        childList.append(node(value))
                    else:
                        value[j] = lastmember
                        #we dont want the last card 
                        value[i] = value[i].replace(lastmember,'')
                        #removing unneeded spaces
                        value[i] = value[i].strip()
                        childList.append(node(value))
                else:
                    splitholderj = value[j].split()
                    lastmemberj = splitholderj[len(splitholderj)-1]        
                    jnum = int(lastmemberj[:len(lastmemberj)-1])
                    if inum < jnum:  
                        if len(splitholder) == 1: 
                            value[j] = value[j]+' '+value[i]
                            value[i] = '' 
                            childList.append(node(value))
                        else:
                            value[j] = value[j]+' '+lastmember
                            value[i] = value[i].replace(lastmember,'')
                            value[i] = value[i].strip()
                            childList.append(node(value))
    return childList
number_of_generated_nodes = 0
def recursive_dls(myNode,limit):
    global number_of_generated_nodes
    if goal_test(myNode):
        number_of_generated_nodes += 1
        return myNode
    elif limit == 0:
        return 'cut off'
    else:
        cutoff_occured = False
        childList = make_children(myNode)
        for i in childList:
            number_of_generated_nodes += 1
            result = recursive_dls(i, limit-1)
            if result == 'cut off': 
                cutoff_occured = True
            else:
                if(goal_test(result)):  
                    return result
        if cutoff_occured: 
            return 'cut off'
        else:
            return 'algorithm has failed'
def depth_limited_search(limit):
    return recursive_dls(firstStateNode, limit) 
def iterative_deeping_search():
    for i in range(0,sys.maxsize):   
        result = depth_limited_search(i)
        if result != 'cut off':
            print('depth:',i)
            return result
print(iterative_deeping_search())
print('number of generated nodes:',number_of_generated_nodes)

                












