import random
import configuration

class Network:

    def __init__(self: 'Network') -> 'None':
        pass
    
    def block_propogation_delay(self: 'Network') -> 'float':
        return random.expovariate(1 / configuration.AVERAGE_BLOCK_PROPOGATION_DELAY)

    def transaction_propogation_delay():
    	return random.expovariate(1 / configuration.AVERAGE_TRANSACTION_PROPOGATION_DELAY)
