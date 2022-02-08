from abc import ABCMeta, abstractmethod


class ImplicitFormulation(metaclass=ABCMeta):

    @abstractmethod
    def time_0_node_0(self, gamma, u_left, initial_velocity, dt, uj_0):
        pass

    @abstractmethod
    def time_0_node_1(self, phi, u_left, initial_velocity, dt, uj_0):
        pass

    @abstractmethod
    def time_0_internal_node(self, phi, initial_velocity, dt, uj_0):
        pass

    @abstractmethod
    def time_0_node__1_interphase(self, gamma, initial_velocity, dt, uj_0):
        pass

    @abstractmethod
    def time_0_interphase(self, alpha):
        pass

    @abstractmethod
    def time_0_node_1_interphase(self, gamma, initial_velocity, dt, uj_0):
        pass

    @abstractmethod
    def time_0_penultimate_node(self, phi, initial_velocity, dt, u_right, uj_0):
        pass

    @abstractmethod
    def time_0_last_node(self, gamma, initial_velocity, dt, u_right, uj_0):
        pass

    @abstractmethod
    def node_0(self, gamma, uj_0, uj_1, u_left):
        pass

    @abstractmethod
    def node_1(self, phi, uj_0, uj_1, u_left):
        pass

    @abstractmethod
    def internal_node(self, phi, uj_0, uj_1):
        pass

    @abstractmethod
    def node__1_interphase(self, gamma, uj_0, uj_1):
        pass

    @abstractmethod
    def interphase(self, alpha):
        pass

    @abstractmethod
    def node_1_interphase(self, gamma, uj_0, uj_1):
        pass

    @abstractmethod
    def penultimate_node(self, phi, uj_0, uj_1, u_right):
        pass

    @abstractmethod
    def last_node(self, gamma, uj_0, uj_1, u_right):
        pass


class InputWave(ImplicitFormulation):

    def __init__(self):
        self.alpha = None
        self.a_i_i = None
        self.a_i_i1 = None
        self.a_i_i2 = None
        self.a_i_i_1 = None
        self.a_i_i_2 = None
        self.b = None

    def alpha_m(self, e_modulus_1, e_modulus_2):
        self.alpha = e_modulus_2 / e_modulus_1

    def time_0_node_0(self, gamma, u_left, initial_velocity, dt, uj_0):
        self.a_i_i = 1 + (2 * gamma)
        self.a_i_i1 = - gamma
        self.b = uj_0 + gamma*u_left + initial_velocity*dt

    def time_0_node_1(self, phi, u_left, initial_velocity, dt, uj_0):
        self.a_i_i = 1 + (30 * phi)
        self.a_i_i_1 = -16 * phi
        self.a_i_i1 = -16 * phi
        self.a_i_i2 = phi
        self.b = uj_0 + initial_velocity*dt - phi*u_left

    def time_0_internal_node(self, phi, initial_velocity, dt, uj_0):
        self.a_i_i_2 = phi
        self.a_i_i_1 = -16 * phi
        self.a_i_i = 1 + (30 * phi)
        self.a_i_i1 = -16 * phi
        self.a_i_i2 = phi
        self.b = uj_0 + initial_velocity * dt

    def time_0_node__1_interphase(self, gamma, initial_velocity, dt, uj_0):
        self.a_i_i_1 = - gamma
        self.a_i_i = 1 + (2*gamma)
        self.a_i_i1 = - gamma
        self.b = uj_0 + (initial_velocity * dt)

    def time_0_interphase(self, alpha):
        self.a_i_i_2 = 1
        self.a_i_i_1 = - 4
        self.a_i_i = 3 * (1 + alpha)
        self.a_i_i1 = - 4 * alpha
        self.a_i_i2 = alpha
        self.b = 0

    def time_0_node_1_interphase(self, gamma, initial_velocity, dt, uj_0):
        self.a_i_i_1 = - gamma
        self.a_i_i = 1 + (2 * gamma)
        self.a_i_i1 = - gamma
        self.b = uj_0 + (initial_velocity * dt)

    def time_0_penultimate_node(self, phi, initial_velocity, dt, u_right, uj_0):
        self.a_i_i_2 = phi
        self.a_i_i_1 = - 16 * phi
        self.a_i_i = 1 + (30 * phi)
        self.a_i_i1 = - 16 * phi
        self.b = uj_0 + (initial_velocity * dt) - (phi * u_right)

    def time_0_last_node(self, gamma, initial_velocity, dt, u_right, uj_0):
        self.a_i_i_1 = - gamma
        self.a_i_i = 1 + (2 * gamma)
        self.b = uj_0 + (initial_velocity * dt) + (gamma * u_right)

    def node_0(self, gamma, uj_0, uj_1, u_left):
        self.a_i_i = 1 + (2 * gamma)
        self.a_i_i1 = - gamma
        self.b = (2 * uj_0) - uj_1 + (gamma * u_left)

    def node_1(self, phi, uj_0, uj_1, u_left):
        self.a_i_i_1 = - 16 * phi
        self.a_i_i = 1 + (30 * phi)
        self.a_i_i1 = -16 * phi
        self.a_i_i2 = phi
        self.b = (2 * uj_0) - uj_1 - (phi * u_left)

    def internal_node(self, phi, uj_0, uj_1):
        self.a_i_i_2 = phi
        self.a_i_i_1 = -16 * phi
        self.a_i_i = 1 + (30 * phi)
        self.a_i_i1 = -16 * phi
        self.a_i_i2 = phi
        self.b = 2 * uj_0 - uj_1

    def node__1_interphase(self,  gamma, uj_0, uj_1):
        self.a_i_i_1 = - gamma
        self.a_i_i = 1 + (2 * gamma)
        self.a_i_i1 = - gamma
        self.b = 2 * uj_0 - uj_1

    def interphase(self, alpha):
        self.a_i_i_2 = 1
        self.a_i_i_1 = - 4
        self.a_i_i = 3 * (1 + alpha)
        self.a_i_i1 = - 4 * alpha
        self.a_i_i2 = alpha
        self.b = 0

    def node_1_interphase(self, gamma, uj_0, uj_1):
        self.a_i_i_1 = - gamma
        self.a_i_i = 1 + (2 * gamma)
        self.a_i_i1 = - gamma
        self.b = 2 * uj_0 - uj_1

    def penultimate_node(self, phi, uj_0, uj_1, u_right):
        self.a_i_i_2 = phi
        self.a_i_i_1 = - 16 * phi
        self.a_i_i = 1 + (30 * phi)
        self.a_i_i1 = - 16 * phi
        self.b = 2 * uj_0 - uj_1 - (phi * u_right)

    def last_node(self, gamma, uj_0, uj_1, u_right):
        self.a_i_i_1 = - gamma
        self.a_i_i = 1 + (2 * gamma)
        self.b = 2 * uj_0 - uj_1 + (gamma * u_right)


class StandingWave(ImplicitFormulation):

    def __init__(self):
        self.alpha = None
        self.a_i_i = None
        self.a_i_i1 = None
        self.a_i_i2 = None
        self.a_i_i_1 = None
        self.a_i_i_2 = None
        self.b = None

    def alpha_m(self, e_modulus_1, e_modulus_2):
        self.alpha = e_modulus_2 / e_modulus_1

    def time_0_node_0(self, gamma, u_left, initial_velocity, dt, uj0_initial):
        self.a_i_i = 1 + (2 * gamma)
        self.a_i_i1 = - gamma

    def time_0_node_1(self, phi, u_left, initial_velocity, dt, uj0_initial):
        pass

    def time_0_internal_node(self, phi, initial_velocity, dt, uj0_initial):
        pass

    def time_0_node__1_interphase(self, gamma, initial_velocity, dt, uj0_initial):
        pass

    def time_0_interphase(self, alpha):
        pass

    def time_0_node_1_interphase(self, gamma, initial_velocity, dt, uj0_initial):
        pass

    def time_0_penultimate_node(self, phi, initial_velocity, dt, u_right, uj0_initial):
        pass

    def time_0_last_node(self, gamma, initial_velocity, dt, u_right, uj0_initial):
        pass

    def node_0(self, gamma, uj0, uj_1, u_left):
        pass

    def node_1(self, phi, uj0, uj_1, u_left):
        pass

    def internal_node(self, phi, uj0, uj_1, u_left):
        pass

    def node__1_interphase(self,  gamma, uj0, uj_1):
        pass

    def interphase(self, alpha):
        pass

    def node_1_interphase(self, gamma, uj0, uj_1):
        pass

    def penultimate_node(self, phi, uj0, uj_1, u_right):
        pass

    def last_node(self, gamma, uj0, uj_1, u_right):
        pass
