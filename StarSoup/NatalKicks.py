def randomise_directions(number):
    
    import numpy
    
    theta_sph = numpy.arccos(2*numpy.random.rand(number)-1)
    phi_sph = 2*numpy.pi*numpy.random.rand(number)
    x_list = numpy.sin(theta_sph)*numpy.cos(phi_sph)
    y_list = numpy.sin(theta_sph)*numpy.sin(phi_sph)
    z_list = numpy.cos(theta_sph)
    return numpy.vstack((x_list, y_list, z_list)).T

def approx_mean2true_anomaly(t, e):
    
    import numpy
    
    return numpy.tan(t*2*numpy.pi*numpy.sqrt(e)/(1+e)**1.5)/numpy.sqrt(1.0/e-1.0)

class MomentumKick:
    
    def __init__(self, mom):
        
        self.mom = mom
        
    def calc(self, masses):
        
        import numpy
        
        return numpy.absolute(numpy.random.normal(0,self.mom,len(masses)))/masses
    
class VelocityKick:
    
    def __init__(self, vel):
        
        self.vel = vel
        
    def calc(self, masses):
        
        import numpy
        
        return numpy.absolute(numpy.random.normal(0,self.vel,len(masses)))

class NatalKicks:
    
    def __init__(self, kick_speed_recipe):
        
        self.kvm = kick_speed_recipe
        
    def evolve(self,
               primary_masses,
               black_hole_masses,
               companion_masses,
               semi_major_axes,
               eccentricities):
        
        import numpy
        
        G = 4.5e-15
        n = len(primary_masses)
        kick_speeds = self.kvm(black_hole_masses)
        kick_velocities = numpy.outer(kick_speeds,[1,1,1])*randomise_directions(n)
        mean_anomalies = numpy.random.rand(n)-0.5
        true_anomalies = approx_mean2true_anomaly(mean_anomalies, eccentricities)
        radii = semi_major_axes*(1-eccentricities**2)/(1-eccentricities*numpy.cos(true_anomalies))
        semilatus_recta = semi_major_axes*(1-eccentricities**2)
        angular_momenta = numpy.sqrt(G*(primary_masses+companion_masses)*semilatus_recta)
        angular_velocities = angular_momenta/radii**2
        v_init = numpy.sqrt(G*(primary_masses+companion_masses)*(2.0/radii-1.0/semi_major_axes))
        vi_y = angular_velocities*radii
        vi_x = numpy.sqrt(v_init**2-vi_y**2)
        final_velocity = numpy.sqrt(kick_velocities.T[2]**2+
                                    (kick_velocities.T[1]+vi_y)**2+
                                    (kick_velocities.T[0]+vi_x)**2)
        final_sma = radii/(2.0-final_velocity**2*radii/G/(black_hole_masses+companion_masses))
        final_e2 = 1-radii**2*(kick_velocities.T[2]**2+(kick_velocities.T[1]+vi_y)**2)/G/(black_hole_masses+companion_masses)/final_sma
        final_e = numpy.sqrt(final_e2)
        return final_sma, final_e, companion_masses
    