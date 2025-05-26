from scipy import optimize
import numpy as np

def pred_parabola (I, unitary_i, N):
    """parabola should be given by following formula"""
    ###sigma_2 = i * I - I^2 / N
    
    #vector size of I
    return unitary_i * I - I ** 2 / N
    
def double_parabola (I_early, unitary_i_early, I_late, unitary_i_late, N):
    """parabola should be given by following formula"""
    ###sigma_2 = i * I - I^2 / N
    
   
    Sigma_2_early = unitary_i_early * I_early - I_early ** 2 / N
    Sigma_2_late = unitary_i_late * I_late - I_late ** 2 / N
    
    #two vectors, size of I_early and I_late
    return Sigma_2_early, Sigma_2_late
   

def fitDoubleParabola (earlyData, lateData):
    # when the variance-current plot has two paths, we can fit separately with common N
    """has guesses built in"""
    
    i_guess_early = 1
    i_guess_late = 0.1
    N_guess = 10
    
    errfunc = lambda guesses: (predDoubleparabola(earlyData[0], guesses[0], guesses[1], lateData[0], guesses[2]) - data[1]) #modify
    
    return optimize.least_squares(errfunc, guesses, bounds = (0, np.inf))
    
def fitParabola (data):
    """has guesses built in"""
        
    i_guess = 7
    N_guess = 10
    
    guesses = [i_guess, N_guess]
    
    errfunc = lambda guesses: (pred_parabola(data[0], guesses[0], guesses[1]) - data[1])

    # loss="soft_l1" is bad!
    return optimize.least_squares(errfunc, guesses, bounds = (0, np.inf))

    
if __name__ == "__main__":

    #### easy variance current data
    #### generated with N = 100, i = 3,
    #### baseline Noise of 2 pA (pk-to-pk)
    #### Current noise of (sqrt (2 * I)) pA (pk-to-pk)
    noisy_I = np.array([
    2.130859892,
    2.996041558,
    4.684199386,
    4.09689902,
    6.394982768,
    12.56642134,
    18.6256529,
    24.16009169,
    43.20173064,
    56.23348266,
    87.82550029,
    108.215676,
    151.0720489,
    203.330102,
    228.3818252]
    )

    sigma_2 = np.array([
    6.347174038,
    8.898362023,
    13.83318092,
    12.12285125,
    18.77599026,
    36.12011456,
    52.40780925,
    66.64317476,
    110.9412966,
    137.0784023,
    186.3433159,
    207.5407027,
    224.9885071,
    196.5590022,
    163.5628948]
    )

    #print (noisy_I, sigma_2)
    
    test_data = [noisy_I, sigma_2]
    
    result = fitParabola (test_data)

    print (result)
