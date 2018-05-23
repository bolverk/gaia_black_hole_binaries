def calc_absolute_magnitude_smith(masses):
    
    import numpy
    
    mag_high = 4.8-10*numpy.log10(masses)
    mag_low = 0.56-5.88*numpy.log10(masses)
    return numpy.where(masses>0.4,
                       mag_high,
                       mag_low)