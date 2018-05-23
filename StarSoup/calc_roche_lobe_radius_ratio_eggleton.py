def calc_roche_lobe_radius_ratio_eggleton(q_list):
    
    import numpy
    
    return (0.6*q_list**(-2.0/3.0)+numpy.log(1.0+q_list**(-1.0/3.0)))/(0.49*q_list**(-2.0/3.0))