def randomise_semi_major_axis_yamaguchi(M1_list):
    
    import numpy
    
    f_list = numpy.random.rand(len(M1_list))
    A_min = 1e-8
    A_max = 1e-2
    return A_min*(A_max/A_min)**f_list