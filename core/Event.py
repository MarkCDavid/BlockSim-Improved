from models.BaseBlock import BaseBlock
from models.BaseNode import BaseNode


class Event:

    def __init__(self: 'Event', type: 'str', node: 'BaseNode', time: 'float', block: 'BaseBlock'):
        self.type = type
        self.node = node
        self.time = time
        self.block = block