
class Material:
    # Constructor
    def __init__(self, density, e_modulus, state, bulk_modulus, thickness):
        self.density = density
        self.e_modulus = e_modulus
        self.state = state
        self.bulk_modulus = bulk_modulus
        self.thickness = thickness
        if self.state == 'liquid':
            self.square_velocity = self.bulk_modulus/self.density
        else:
            self.square_velocity = self.e_modulus/self.density


