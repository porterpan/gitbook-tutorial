import numpy as np
def markov(): 
    init_array = np.array([0.4, 0.3, 0.3]) 
    transfer_matrix = np.array([[0.4, 0.3, 0.3], 
                                [0.6, 0.3, 0.1], 
                                [0.6, 0.1, 0.3]]) 
    restmp = init_array 
    for i in range(25): 
        res = np.dot(restmp, transfer_matrix) 
        print(i, "\t", res ) 
        restmp = res 

def markov_comsume(): 
    init_array = np.array([0.4, 0.3, 0.3]) 
    transfer_matrix = np.array([[0.4, 0.3, 0.3], 
                                [0.6, 0.3, 0.1], 
                                [0.6, 0.1, 0.3]]) 

    res=np.dot(init_array, transfer_matrix)  
    print("\t", res )    

    # restmp = init_array 
    # for i in range(25): 
    #     res = np.dot(restmp, transfer_matrix) 
    #     print(i, "\t", res ) 
    #     restmp = res        
# markov()
markov_comsume()
