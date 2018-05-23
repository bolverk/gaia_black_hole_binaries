class EvolutionSequence:
    
    def __init__(self, sequence):
        
        self.sequence = sequence
        
    def evolve(self,
               primary_masses,
               black_hole_masses,
               companion_masses,
               semi_major_axes,
               eccentricities):
        a_list = semi_major_axes
        e_list = eccentricities
        m2_list = companion_masses
        for stage in self.sequence:
            a_list, e_list, m2_list = stage(primary_masses,
                                            black_hole_masses,
                                            m2_list,
                                            a_list,
                                            e_list)
        return a_list, e_list, m2_list