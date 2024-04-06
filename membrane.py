import numpy as np
from scipy.special import jv, jn_zeros, jnp_zeros

class CircularMembrane:
    def __init__(self, a:float, c:float, m:int, n:int, A=1):
        # membrane radius
        self.a = a
        # membrane stiffness
        self.c = c
        # amplitude
        self.A = A
        # m => gamma in the paper, i.e the order of the Bessel function
        self.m = m
        # n => nth root of the Bessel function to use
        self.n = n
        # lambda
        self.lamb = self.compute_lambda()
    
    def get_radius(self):
        return self.a
    
    def get_period(self):
        # Time to compute one full cycle
        return 2 * np.pi / (self.c * self.lamb)
    
    def get_wave_numbers(self):
        return self.m, self.n

    def compute_lambda(self):
        # Get the nth root of the Bessel function
        alpha = jn_zeros(self.m, self.n)[self.n-1]
        return alpha/self.a
    
    def get_amplitude(self):
        # find where the maxima of the Bessel function occurs
        max_x = jnp_zeros(self.m, 1)[0]
        # find the magnitude of the amplitude
        bessel_A = jv(self.m, max_x)

        return abs( self.A * bessel_A * 2**0.5 )
        
    def normalize(self, A=1):
        self.A /= self.get_amplitude()
        self.A *= A
    
    def evaluate(self, r, theta, t):
        return self.A * jv(self.m, self.lamb*r) \
            * np.sin(self.c * self.lamb * t) \
            * ( np.cos(self.m * theta) + np.sin(self.m * theta) )

class RectangularMembrane:
    def __init__(self, a:float, b:float, m:float, n:float, c:float, A=1):
        self.a = a
        self.b = b
        self.m = m
        self.n = n
        self.c = c
        self.A = A

        self.lamb = self.compute_lambda()
    
    def compute_lambda(self):
        return np.pi / (self.a * self.b) * np.sqrt(
            (self.n*self.b)**2 + (self.m*self.a)**2
        )
    
    def get_dimensions(self):
        return self.a, self.b
    
    def normalize(self, A=1):
        self.A = A
    
    def get_amplitude(self):
        return self.A

    def get_wave_numbers(self):
        return self.m, self.n
    
    def get_period(self):
        return 2*np.pi / (self.c * self.lamb)

    def evaluate(self, x, y, t):
        return self.A \
            * np.sin( self.n*np.pi/self.a * x ) \
            * np.sin( self.m*np.pi/self.b * y ) \
            * np.sin( self.lamb*self.c * t )