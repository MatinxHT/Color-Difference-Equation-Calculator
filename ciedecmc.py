import numpy as np

standard = (13,23,1)
sample = (12,24,2)
pl = 2
pc = 1 

def e_cmc(standard, sample, pl, pc):
    "delta_e_cmc(pl:pc = 2:1)"
    
    #defining source's LAB
    Ls = standard[0]
    As = standard[1]
    Bs = standard[2]
    L = sample[0]
    A = sample[1]
    B = sample[2]
    
    #from Lab to LCH
    Cab_standard = np.sqrt(np.power(As,2)+np.power(Bs,2))
    Cab_sample = np.sqrt(np.power(A,2)+np.power(B,2))
    Hab_sample = np.degrees(np.arctan2(B,A))
    if Hab_sample < 0:
        Hab_sample += 360
    
    delta_L = L - Ls
    delta_C = Cab_sample - Cab_standard
    delta_E_Lab_square = np.power((L - Ls),2) + np.power((A-As),2) + np.power((B-Bs),2)
    delta_H = np.sqrt(delta_E_Lab_square - np.power((L-Ls),2) - np.power(delta_C,2))
    
    #formating S_L S_C S_H(special this motherfucker)
    if Ls < 16:
        S_L = 0.511
    else:
        S_L = (0.040975 * Ls) / (1 + 0.01765 * Ls)
    
    S_C = ((0.0638 * Cab_standard) / (1 + 0.0131 * Cab_standard)) + 0.638
    # computing f for S_H
    f = np.sqrt(np.power(Cab_standard, 4) / (np.power(Cab_standard, 4) + 1900.0))
    #computing T for S_H
    if 164 <= Hab_sample and Hab_sample <= 345:
        T = 0.56 + abs(0.2 * np.cos(np.radians(Hab_sample + 168)))
    else:
        T = 0.36 + abs(0.4 * np.cos(np.radians(Hab_sample + 35)))
    #so this motherfucker finally show up 
    S_H = ((f*T)+ 1 - f) * S_C

    delta_e_cmc = np.sqrt(np.power((delta_L/(pl*S_L)),2) + np.power((delta_C/(pc*S_C)),2) + np.power((delta_H/S_H),2))
    return[delta_e_cmc]

result = e_cmc(standard,sample,pl,pc)
print(result)