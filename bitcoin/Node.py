from models.BaseNode import BaseNode

class Node(BaseNode):
    def __init__(self, id: 'int', hashPower: 'int'):
        super().__init__(id)
        self.hashPower = hashPower
        
