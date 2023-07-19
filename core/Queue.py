import bisect

from core.Event import Event


class Queue:

    def __init__(self: 'Queue'):
        self.queue = []

    def push(self: 'Queue', event: 'Event'):
        bisect.insort(self.queue, (event.time, event))

    def pop(self: 'Queue') -> 'Event':
        if not self:
            raise IndexError("Cannot get and remove from an empty queue")
        
        return self.queue.pop(0)[1]

    def __len__(self):
        return len(self.queue)
    
    def __bool__(self):
        return bool(self.queue)
