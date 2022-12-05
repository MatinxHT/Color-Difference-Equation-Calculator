import numpy as np

def e_cmc(standard, sample, pl, pc):
    "delta_e_cmc(pl:pc)"
    
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
    Hab_standard = np.degrees(np.arctan2(Bs,As))
    if Hab_standard < 0:
        Hab_standard += 360
    Hab_sample = np.degrees(np.arctan2(B,A))
    if Hab_sample < 0:
        Hab_sample += 360
    
    delta_L = L - Ls
    delta_C = Cab_sample - Cab_standard
    
    #figuring out the +- of delta_E_Lab
    m = Hab_sample - Hab_standard
    if m >= 0:
        p = 1
    else:
        p = -1
    
    if abs(m) <= 180:
        q = 1
    else:
        q = -1
    
    delta_E_Lab_square = np.power((L - Ls),2) + np.power((A-As),2) + np.power((B-Bs),2)
    delta_H = p * q * np.sqrt(delta_E_Lab_square - np.power((L-Ls),2) - np.power(delta_C,2))

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
   # delta_e_cmc2 = np.sqrt(np.power((delta_L/(pl*S_L)),2) + np.power((delta_C/(pc*S_C)),2) + np.power((delta_H2/S_H),2))
    delta_l_cmc = np.sqrt(np.power((delta_L/(pl*S_L)),2))
    delta_c_cmc = np.sqrt(np.power((delta_C/(pc*S_C)),2))
    delta_h_cmc = np.sqrt(np.power((delta_H/S_H),2))
    
    return[delta_e_cmc,delta_l_cmc,delta_c_cmc,delta_h_cmc]

def e_2000(standard, sample, k_L , k_C , k_H):
    "delta_e_2000 kl=kc=kh=1"
    
    #defining source's LAB
    L_1_star = standard[0]
    a_1_star = standard[1]
    b_1_star = standard[2]
    L_2_star = sample[0]
    a_2_star = sample[1]
    b_2_star = sample[2]

    #L_1_star,a_1_star,b_1_star=lab1
	#L_2_star,a_2_star,b_2_star=lab2
    C_1_star = np.sqrt(np.power(a_1_star,2) + np.power(b_1_star,2))
    C_2_star=np.sqrt(np.power(a_2_star,2) + np.power(b_2_star,2))
    C_bar_star=(C_1_star+C_2_star)/2
    
    G = 0.5*(1-np.sqrt(np.power(C_bar_star,7)/(np.power(C_bar_star,7)+np.power(25,7))))
    
    a_1_dash = (1 + G)*a_1_star
    a_2_dash = (1 + G)*a_2_star
    C_1_dash = np.sqrt(np.power(a_1_dash,2) + np.power(b_1_star,2))
    C_2_dash = np.sqrt(np.power(a_2_dash,2) + np.power(b_2_star,2))
    h_1_dash = np.degrees(np.arctan2(b_1_star,a_1_dash))
    h_1_dash += (h_1_dash < 0) * 360
    h_2_dash = np.degrees(np.arctan2(b_2_star,a_2_dash))
    h_2_dash += (h_2_dash < 0) * 360
    
    delta_L_dash = L_2_star - L_1_star
    delta_C_dash = C_2_dash - C_1_dash
    delta_h_dash = 0.0
    
    if(C_1_dash * C_2_dash):
        if(abs(h_2_dash-h_1_dash) <= 180):
            delta_h_dash = h_2_dash - h_1_dash
        elif(h_2_dash - h_1_dash > 180):
            delta_h_dash = (h_2_dash-h_1_dash) - 360
        elif (h_2_dash-h_1_dash) <- 180:
            delta_h_dash = (h_2_dash-h_1_dash) + 360
    
    delta_H_dash= 2 * np.sqrt(C_1_dash*C_2_dash)* np.sin(np.radians(delta_h_dash)/2.0)
	
    L_bar_dash = (L_1_star + L_2_star)/2
    C_bar_dash = (C_1_dash + C_2_dash)/2
    h_bar_dash = h_1_dash + h_2_dash
    
    if(C_1_dash * C_2_dash):
        if(abs(h_1_dash - h_2_dash) <= 180):
            h_bar_dash = (h_1_dash + h_2_dash)/2
        else:
            if(h_1_dash + h_2_dash) < 360:
                h_bar_dash = (h_1_dash + h_2_dash + 360)/2
            else:
                h_bar_dash = (h_1_dash + h_2_dash - 360)/2

    T = 1 - 0.17 * np.cos(np.radians(h_bar_dash-30)) + 0.24 * np.cos(np.radians(2 * h_bar_dash))\
	+ 0.32 * np.cos(np.radians(3 * h_bar_dash + 6))-0.20 * np.cos(np.radians(4*h_bar_dash-63))
	
    delta_theta = 30 * np.exp(-1 * np.power( (h_bar_dash-275) / 25, 2))

    R_c = 2 * np.sqrt( np.power(C_bar_dash,7) / (np.power(C_bar_dash,7) + np.power(25,7)) )
	
    S_L = 1 + ((0.015 * np.power(L_bar_dash - 50,2))/np.sqrt(20 + np.power(L_bar_dash-50,2)))
    S_C = 1 + 0.045 * C_bar_dash
    S_H = 1 + 0.015 * C_bar_dash * T
    R_T = -1 * R_c * np.sin(2 * np.radians(delta_theta))
	
    delta_E_00 = np.sqrt(np.power(delta_L_dash/(k_L*S_L),2) + np.power(delta_C_dash/(k_C*S_C),2) + 
    np.power(delta_H_dash/(k_H*S_H),2) + R_T*(delta_C_dash/(k_C*S_C)) * 
    (delta_H_dash/(k_H*S_H)))
    delta_L_00 = np.sqrt(np.power(delta_L_dash/(k_L*S_L),2))
    delta_C_00 = np.sqrt(np.power(delta_C_dash/(k_C*S_C),2))
    delta_H_00 = np.sqrt(np.power(delta_H_dash/(k_H*S_H),2))

    return(delta_E_00,delta_L_00,delta_C_00,delta_H_00)
