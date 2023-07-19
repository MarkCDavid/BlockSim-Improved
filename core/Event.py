from models.BaseBlock import BaseBlock


class Event:

    def __init__(self: 'Event', type: 'str', node: 'int', time: 'float', block: 'BaseBlock'):
        self.type = type
        self.node = node
        self.time = time
        self.block = block