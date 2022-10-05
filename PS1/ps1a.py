###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================
# Lotus , 10
# Horns , 9
# Dottie , 6
# Betsy , 5
# Milkshake , 4
# Miss Moo-dy , 3
# Rose , 3
# Miss Bella , 2

#   'ps1_cow_data_2.txt'

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    inFile = open(filename, 'r')

    
    cow_dict = {}
    
    for line in inFile:
        cows=line.strip('\n')
        cowlist=cows.split(',')
        cow_dict[cowlist[0]]=cowlist[1]
    inFile.close()
    return cow_dict

class Cows(object):
    
    def __init__(self, name, weight):
        self.name=name
        self.weight=int(weight)
        
    def get_name(self):
        return self.name
    
    def get_weight(self):
        return self.weight
    
    def __str__(self):
        return self.name + ' , ' + str(self.weight)

# Problem 2
def greedy_cow_transport(cow_dict,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cow_dict - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    cow_list=[]
    
    # build a list with elements of type Cows
    for i in cow_dict.keys():
        cow_list.append(Cows(i,cow_dict[i]))    
    
    items=sorted(cow_list, key=Cows.get_weight, reverse=True) # sort the cows by weight
    
    trips=[]
    itemscopy=items[:]

    
    while len(items) > 0:
          
        temptrips=[]
        totalcost= 0   
        for j in range(len(items)):
            if (totalcost+items[j].get_weight()) <= limit:
                temptrips.append(items[j].get_name())
                totalcost += items[j].get_weight()
                itemscopy.remove(items[j])
        
        trips.append(temptrips)
        items=itemscopy[:]

    return trips

# for partition in get_partitions([1,2,3,4]):
#     print(partition)


# Problem 3
def brute_force_cow_transport(cow_dict,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    cow_list=[]
    
    # build a list with elements of type Cows
    for i in cow_dict.keys():
        cow_list.append(Cows(i,cow_dict[i]))    
    
    trips=[]
    
    # indexes into the generator list
    for partition in get_partitions(cow_list):
        subtrip=[]  # initialize subtrip (len(subtrip) will be used to determine if partition is a valid trip)
        
        # sublist is each trip made within partition
        for sublist in partition:
            tempweight=0    # initialize tempweight, which if it exceeds limit, subtrip not valid
            temptrip=[]     # initialize temptrip (len(temptrip) will be used to determine if sublist is a valid trip)
            
            # iterates over each cow within the trip
            for i in sublist:
                tempweight += i.get_weight()
                
                # if tempweight exceeds the limit, resets temptrip to an empty list and breaks the loop
                if tempweight > limit:
                    temptrip=[]
                    break
                else:
                    temptrip.append(i.get_name())
            
            # if len(temptrip) > 0, limit was not exceeded and therefore a valid trip
            if len(temptrip) > 0:
                subtrip.append(temptrip)
            else:
                # one part of sublist was invalid, therefore partition is invalid
                subtrip=[]
                break
        
        # if all trips within partion are valid
        if len(subtrip) > 0:
            trips.append(subtrip)

    complen , besttrips = len(trips[0]) , trips[0]
    
    for j in trips[1:]:
        if len(j) < complen:
            complen , besttrips = len(j) , j
   
    
    return besttrips

# print("greedy: " + str(greedy_cow_transport(load_cows('ps1_cow_data_2.txt'))))
# print("\nbrute force: " + str(brute_force_cow_transport(load_cows('ps1_cow_data_2.txt'))))


       
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    start = time.time()
    greed = greedy_cow_transport(load_cows('ps1_cow_data_2.txt'))
    end = time.time()
    timegreed =  end - start
    
    print("Greedy Algorithm took " + str(timegreed) + " seconds, and required "
          + str(len(greed)) +" trips \n")
    
    start = time.time()
    brute = brute_force_cow_transport(load_cows('ps1_cow_data_2.txt'))
    end = time.time()
    timebrute =  end - start
    
    print("Brute Force Algorithm took " + str(timebrute) + " seconds, and required "
          + str(len(brute)) +" trips")
    
    
    
    
    return

compare_cow_transport_algorithms()
