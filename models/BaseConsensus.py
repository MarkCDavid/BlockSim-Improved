from models.BaseNode import BaseNode

class BaseConsensus:

    def __init__(self: 'BaseConsensus') -> 'None':
        self.global_chain = []

    def Protocol(self: 'BaseConsensus', node: 'BaseNode') -> 'float':
        pass

    def fork_resolution(self: 'BaseConsensus') -> 'None':
        pass
