def calc_massive_common_envelope_evolution(primary_masses,
                                         black_hole_masses,
                                         companion_masses,
                                         semi_major_axes,
                                         eccentricities):
    import numpy
    
    a = 1.0
    b = 0.5
    c1 = a*(1.0-b)-2.0
    c2 = -a*(1.0-b)-2.0
    q_list = companion_masses/primary_masses
    k_list = black_hole_masses/primary_masses
    sma_ratios = (k_list+b*(1-k_list)+q_list)/(1+q_list)*k_list**c1*(b*(1-k_list)/q_list+1)**c1
    terminal_semi_major_axes =  semi_major_axes*sma_ratios
    terminal_eccentricities = numpy.zeros_like(eccentricities)
    terminal_companion_masses = companion_masses + 0.5*(primary_masses-black_hole_masses)
    return terminal_semi_major_axes, terminal_eccentricities, terminal_companion_masses

def calc_wimpy_common_envelope_evolution(primary_masses,
                                         black_hole_masses,
                                         companion_masses,
                                         semi_major_axes,
                                         eccentricities,
                                        al=1.0):
    
    from calc_roche_lobe_radius_ratio_eggleton import calc_roche_lobe_radius_ratio_eggleton
    import numpy
    
    q_list = companion_masses/primary_masses
    k_list = black_hole_masses/primary_masses
    rl_list = 1.0/calc_roche_lobe_radius_ratio_eggleton(q_list)
    sma_ratios = k_list/(2.0*(1.0-k_list)/(al*rl_list*q_list)+1.0)
    terminal_semi_major_axes = semi_major_axes*sma_ratios
    terminal_eccentricities = numpy.zeros_like(eccentricities)
    terminal_companion_masses = companion_masses
    return terminal_semi_major_axes, terminal_eccentricities, terminal_companion_masses

def evolve_unrestricted_common_envelope(primary_masses,
                                        black_hole_masses,
                                        companion_masses,
                                        semi_major_axes,
                                        eccentricities,
                                        al=1.0):
    
    import numpy
    
    wimpy_sma, wimpy_e, wimpy_m2 = calc_wimpy_common_envelope_evolution(primary_masses,
                                                                        black_hole_masses,
                                                                        companion_masses,
                                                                        semi_major_axes,
                                                                        eccentricities,
                                                                        al=al)
    massive_sma, massive_e, massive_m2 = calc_massive_common_envelope_evolution(primary_masses,
                                                                                black_hole_masses,
                                                                                companion_masses,
                                                                                semi_major_axes,
                                                                                eccentricities)
    q_list = companion_masses/primary_masses
    mask = q_list > 0.5
    ce_sma = numpy.where(mask,
                         massive_sma,
                         wimpy_sma)
    ce_e = numpy.where(mask,
                       massive_e,
                       wimpy_e)
    ce_m2 = numpy.where(mask,
                        massive_m2,
                        wimpy_m2)
    return ce_sma, ce_e, ce_m2
    

def evolve_common_envelope(primary_masses,
                           black_hole_masses,
                          companion_masses,
                          semi_major_axes,
                          eccentricities,
                          al=1.0):
    
    import numpy
        
    ce_sma, ce_e, ce_m2 = evolve_unrestricted_common_envelope(primary_masses,
                                                               black_hole_masses,
                                                               companion_masses,
                                                               semi_major_axes,
                                                               eccentricities,
                                                               al=al)
    
    maximum_agb_radius = 3e-5
    periapses = semi_major_axes*(1-eccentricities)
    is_within_rlo = maximum_agb_radius > periapses
    final_sma = numpy.where(is_within_rlo,
                            ce_sma,
                            semi_major_axes)
    final_e = numpy.where(is_within_rlo,
                          ce_e,
                          eccentricities)
    final_m2 = numpy.where(is_within_rlo,
                           ce_m2,
                           companion_masses)
    return final_sma, final_e, final_m2
                            