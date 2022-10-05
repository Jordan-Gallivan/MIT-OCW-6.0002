"""
Created on Mon Feb 28 09:02:48 2022

@author: jordangallivan
"""

def noneloc(value):
    '''
    Fucntion to determine if None is in value for int, tuple, and list

    Parameters
    ----------
    value : int, tuple, or list
        DESCRIPTION.

    Returns
    -------
    bool
        True if None in value
        False if None not in value

    '''
    
    try:
        #int case
        if None in value:
            return True
        else:
            return False
    except:
        if value == None:
            return True
        else: 
            return False    
    return





def DPEggs(eggs, maxWeight, memo={}):
    '''
    
    Uses Dynamic Programming to find optiaml result to number of golden eggs
        that can be taken based on input of eggs and maxWeight
    
    Parameters
    ----------
    
    eggs: list
        egg weights available to take, ordered from smalles to largest
    maxWeight: int
        weight available on the ship
    memo: dict
        keys: int 
            maxWeight 
        values: tuple 
            (total #of eggs, (eggs taken))
    Returns
    -------
    
    result: tuple
        (total #eggs, (eggs taken))
    
                      
    **Will return None in cases where weight is less than eggs available
    '''
    
    if maxWeight in memo:
        # memo case - has the weight already been evaluated?
        result = memo[maxWeight]


    ###### begining of Base Case
    elif eggs == [] and maxWeight != 0:
        result = (0, None)
        return result
    # Zero'd out weight with or without remaining eggs
    elif maxWeight == 0:
            # returns a zero'd result becasue value is incremented by default
            # and eggweight is added by default
        result = (0, ())
        return result
    #######end of base case

    elif eggs[-1] > maxWeight:
        # biggest egg exceeds maxweight, therefore right branch only
        result = DPEggs(eggs[:-1], maxWeight, memo)
        
    else:
        eggtaken = eggs[-1]
        
        # left branch (take the egg)
        withval, withtaken = DPEggs(eggs, maxWeight - eggtaken, memo)
        withval +=1
        
        # right branch (leave the egg)
        withoutval, withouttaken = DPEggs(eggs[:-1], maxWeight, memo)
        
        
        # determine if None in either result
        if noneloc(withtaken):
            if noneloc(withouttaken):
                result = (0, ())
            else:
                result = (withoutval, withouttaken)
        elif noneloc(withouttaken):
            result = (withval, withtaken + (eggtaken,))
        else:
            if withval < withoutval:
                result = (withval, withtaken + (eggtaken,))
            else:
                result = (withoutval, withouttaken)
            
    
    memo[maxWeight] = result    
    # print(memo)
    return result



eggs = [1, 5, 10, 25]

testeggs = ([1,5,10,25], [2,4,6,8,10,12], [1,3,6,9], [5,10,20,25,30])
testweights= (73, 54, 53, 4)

def test_DPEggs(testeggs, testweights):
    

    i=0
    numeggs, eggweights = DPEggs(testeggs[i], testweights[i])
    
    print("For the list: " + str(testeggs[i]) + " the number of eggs taken are: " 
          + str(numeggs) + " in the following combo: " + str(eggweights))

            
    return

test_DPEggs(testeggs, testweights)

    
    
    
    
    
    
    