def randomise_galaxy_position_yamaguchi(number):
    
    import numpy
    
    f_list = numpy.random.rand(number)
    z_list = -250*numpy.log(1-f_list)
    
    f_list = numpy.random.rand(number)
    r_list = -3500*numpy.log(1-f_list)
    
    phi_list = numpy.pi*numpy.random.rand(number)
    
    return numpy.vstack((r_list, z_list, phi_list))