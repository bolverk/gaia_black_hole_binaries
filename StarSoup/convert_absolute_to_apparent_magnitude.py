def convert_absolute_to_apparent_magnitude(absolute,
                                           d_pc,
                                           extinction=True):
    
    import numpy
    
    res = absolute+5*(numpy.log10(d_pc)-1)
    if extinction:
        res += d_pc/1e3
    return res