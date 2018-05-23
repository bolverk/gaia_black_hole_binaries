def randomise_primary_mass_salpeter(l):
    
    import numpy
    
    f = numpy.random.rand(l)
    
    return 20.0/(1.0-0.886*f)**0.741