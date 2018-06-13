def uniform2powerlaw(x_min, x_max, alpha, f):
    
    p = 1-alpha
    return ((1-f)*x_min**p+f*x_max**p)**(1.0/p)

class PowerLawDistribution:
    
    def __init__(self, x_min, x_max, alpha):
        
        self.x_min = x_min
        self.x_max = x_max
        self.alpha = alpha
        
    def __call__(self, n):
        
        import numpy
        
        f = numpy.random.rand(n)
        return uniform2powerlaw(self.x_min, 
                                self.x_max, 
                                self.alpha, 
                                f)