def calc_distance_from_earth(r_list, z_list, q_list):
    
    import numpy
    
    r0 = 8e3
    return numpy.sqrt(z_list**2+r_list**2+r0**2-2*r_list*r0*numpy.cos(q_list))

def cook(recipe, number):
    
    import numpy
    from calc_absolute_magnitude_smith import calc_absolute_magnitude_smith
    from convert_absolute_to_apparent_magnitude import convert_absolute_to_apparent_magnitude
    
    res = {}
    res['primary mass'] = recipe['primary mass'](number)
    res['initial mass ratio'] = recipe['initial mass ratio'](res['primary mass'])
    res['initial companion mass'] = res['primary mass']*res['initial mass ratio']
    res['initial semi major axis'] = recipe['initial semi major axis'](res['primary mass'])
    res['initial eccentricity'] = recipe['initial eccentricity'](number)
    res['galaxy position'] = recipe['galaxy position'](number)
    res['distance from earth'] = calc_distance_from_earth(res['galaxy position'][0],
                                                          res['galaxy position'][1],
                                                          res['galaxy position'][2])
    res['black hole mass'] = recipe['progenitor to black hole mass'](res['primary mass'])
    res['terminal semi major axis'], res['terminal eccentricity'], res['terminal companion mass'] = recipe['binary evolution'](
        res['primary mass'],
        res['black hole mass'],
        res['initial companion mass'],
        res['initial semi major axis'],
        res['initial eccentricity'])
    #res['lifetime'] = res['terminal companion mass']**-2.5 - res['primary mass']**-2.5
    res['lifetime'] = numpy.where(res['terminal companion mass']>1.01*res['initial companion mass'],
                                  res['terminal companion mass']**-2.5,
                                  res['initial companion mass']**-2.5-res['primary mass']**-2.5)
    res['statistical weight'] = numpy.clip(res['lifetime'],0,1)
    total_mass = res['black hole mass'] + res['terminal companion mass']
    res['terminal period'] = 9.4e7*res['terminal semi major axis']**1.5/numpy.sqrt(total_mass)
    res['absolute magnitude'] = calc_absolute_magnitude_smith(res['terminal companion mass'])
    res['apparent magnitude'] = convert_absolute_to_apparent_magnitude(res['absolute magnitude'],
                                                                 res['distance from earth'],
                                                                 extinction=True)
    return res