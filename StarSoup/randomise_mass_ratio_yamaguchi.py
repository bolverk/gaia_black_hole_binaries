def randomise_mass_ratio_yamaguchi(M1_list):
    
    import numpy
    
    q_min = 0.08/M1_list
    f_list = numpy.random.rand(len(M1_list))
    return q_min + f_list*(1-q_min)