def fiducial():
    
    from randomise_primary_mass_salpeter import randomise_primary_mass_salpeter
    from randomise_mass_ratio_yamaguchi import randomise_mass_ratio_yamaguchi
    from randomise_semi_major_axis_yamaguchi import randomise_semi_major_axis_yamaguchi
    from randomise_galaxy_position_yamaguchi import randomise_galaxy_position_yamaguchi
    from calc_progenitor2black_hole_mass_yamaguchi_curved import calc_progenitor2black_hole_mass_yamaguchi_curved
    from randomise_eccentricity_duchene_kraus import randomise_eccentricity_duchene_kraus
    from CommonEnvelope import evolve_common_envelope
    
    res = {}
    res['primary mass'] = randomise_primary_mass_salpeter
    res['initial mass ratio'] = randomise_mass_ratio_yamaguchi
    res['initial semi major axis'] = randomise_semi_major_axis_yamaguchi
    res['initial eccentricity'] = randomise_eccentricity_duchene_kraus
    res['galaxy position'] = randomise_galaxy_position_yamaguchi
    res['progenitor to black hole mass'] = calc_progenitor2black_hole_mass_yamaguchi_curved
    res['binary evolution'] = evolve_common_envelope
    return res