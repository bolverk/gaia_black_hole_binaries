def is_outside_companion_roche_radius(population):
    
    from calc_roche_lobe_radius_ratio_eggleton import calc_roche_lobe_radius_ratio_eggleton
    from calc_radius_demircan_kahraman import calc_radius_demircan_kahraman
    
    periapses = population['terminal semi major axis']*(1-population['terminal eccentricity'])
    companion_radii = calc_radius_demircan_kahraman(population['terminal companion mass'])
    mass_ratios = population['black hole mass']/population['terminal companion mass']
    roche_radii = companion_radii*calc_roche_lobe_radius_ratio_eggleton(
        population['black hole mass']/population['terminal companion mass'])
    return population['terminal semi major axis']>roche_radii

def is_within_period_range(population):
    
    import numpy
    
    periods = population['terminal period']
    return numpy.logical_and(periods<5,periods>0.137)

def is_bright_enough(population):
    
    hipparcos_limiting_magnitude = 12.4
    return population['apparent magnitude']<hipparcos_limiting_magnitude

def calc_gaia_z12p09(gmag):
    
    import numpy
    
    capped_gmag = numpy.clip(gmag, 12, 200)
    return numpy.clip(10**(0.4*(capped_gmag-15)), 10**(0.4*(12.09-15)),1e30)

def calc_sigma_pomega(gmag):
    
    import numpy
    
    z = calc_gaia_z12p09(gmag)
    return numpy.sqrt(-1.63+680.8*z+32.7*z**2)

def calc_sigma_G(gmag):
    
    import numpy
    
    z = calc_gaia_z12p09(gmag)
    return 1.2e-3*numpy.sqrt(0.05*z**2+1.9*z+0.0002)

def is_black_hole_conclusive(population):
    
    import numpy
    
    sigma_pomega = 100*calc_sigma_pomega(population['apparent magnitude'])
    apoapses = population['terminal semi major axis']*(1 + population['terminal eccentricity'])
    opening_angle = 2e11*apoapses/population['distance from earth']
    sigma_G = calc_sigma_G(population['apparent magnitude'])
    
    return numpy.logical_and(population['black hole mass']>3.0/(1.0-(5./3.)*sigma_pomega/opening_angle-sigma_G),
                             apoapses>10*sigma_pomega*population['distance from earth']*5e-12)

def is_neutron_star_conclusive(population):
    
    import numpy
    
    sigma_pomega = 100*calc_sigma_pomega(population['apparent magnitude'])
    apoapses = population['terminal semi major axis']*(1 + population['terminal eccentricity'])
    opening_angle = 2e11*apoapses/population['distance from earth']
    sigma_G = calc_sigma_G(population['apparent magnitude'])
    
    aux = numpy.logical_and(population['black hole mass']>1.4/(1.0+(5./3.)*sigma_pomega/opening_angle-sigma_G),
                            population['black hole mass']<2.4/(1.0-(5./3.)*sigma_pomega/opening_angle-sigma_G))
    return numpy.logical_and(aux,
                             apoapses>10*sigma_pomega*population['distance from earth']*5e-12)


def is_bound(population):
    
    return population['terminal eccentricity']<0.99

def is_sma_positive(population):
    
    return population['terminal semi major axis']>0

def whittle_hipparcos(population, species='black hole'):
    
    import numpy
    
    species_filter = {'black hole':is_black_hole_conclusive,
                      'neutron star':is_neutron_star_conclusive}
    
    condition_list = [is_outside_companion_roche_radius,
                     is_within_period_range,
                     is_bright_enough,
                     species_filter[species],
                     is_bound,
                     is_sma_positive]
    mask_list = [cond(population) for cond in condition_list]
    res = numpy.all(mask_list, axis=0)
    return res
