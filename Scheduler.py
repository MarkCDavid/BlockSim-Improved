import random
import Configuration
from core.Event import Event
from core.Queue import Queue

from models.BaseBlock import BaseBlock
from models.BaseNode import BaseNode

class Scheduler:
    
    def __init__(self: 'Scheduler', queue: 'Queue') -> 'None':
        self.queue = queue

    def event__create_block(self: 'Scheduler', miner: 'BaseNode', event_time: 'float') -> 'None':
        if event_time > Configuration.SIMULATION_LENGTH_IN_SECONDS:
            return
        
        block = BaseBlock()
        block.miner = miner.id
        block.depth = len(miner.blockchain)
        block.id = random.randrange(100000000000)
        block.previous = miner.last_block().id
        block.timestamp = event_time

        event = Event("create_block", block.miner, event_time, block)

        self.queue.push(event)

    def event__receive_block(self: 'Scheduler', recipient: 'BaseNode', block: 'BaseBlock', blockDelay: 'float') -> 'None':
        receive_block_time = block.timestamp + blockDelay
        if receive_block_time > Configuration.SIMULATION_LENGTH_IN_SECONDS:
            return
        
        event = Event("receive_block", recipient.id, receive_block_time, block)
        self.queue.push(event)

# class Scheduler:

#     def create_block_event_AB(node, eventTime, receiverGatewayId):
#         eventType = "create_block"
#         if eventTime <= p.simTime:
#             block = AB()
#             block.id = random.randrange(100000000000)
#             block.timestamp = eventTime
#             block.nodeId = node.id
#             block.gatewayIds = node.gatewayIds
#             block.receiverGatewayId = receiverGatewayId
#             event = Event(eventType, node.id, eventTime, block)
#             Queue.add_event(event)  # add the event to the queue

#     def append_tx_list_event(txList, gatewayId, tokenTime, eventTime):
#         eventType = "append_tx_list"
#         if eventTime <= p.simTime:
#             block = AB()
#             block.transactions = txList.copy()
#             block.timestamp = tokenTime
#             event = Event(eventType, gatewayId, eventTime, block)
#             Queue.add_event(event)

#     def receive_tx_list_event(txList, gatewayId, tokenTime, eventTime):
#         eventType = "receive_tx_list"
#         if eventTime <= p.simTime:
#             block = AB()
#             block.transactions = txList.copy()
#             block.timestamp = tokenTime
#             event = Event(eventType, gatewayId, eventTime, block)
#             Queue.add_event(event)
