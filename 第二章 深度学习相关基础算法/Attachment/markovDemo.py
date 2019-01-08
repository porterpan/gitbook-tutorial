import numpy as np
def markov(): 
    init_array = np.array([1, 0, 0]) 
    transfer_matrix = np.array([[0.625, 0.375, 0], 
                                [0.25, 0.58, 0.17], 
                                [0, 0.67, 0.33]]) 
    restmp = init_array 
    for i in range(25): 
        res = np.dot(restmp, transfer_matrix) 
        print('N(',i+1,')', "\t", res ) 
        restmp = res 
  
markov()

