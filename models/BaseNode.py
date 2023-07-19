from typing import List
from models.BaseBlock import BaseBlock

# FIXME: Needs factory for Block
# NOTE: `nodes` should come from `configuration.NODES`
def generate_genesis_block(nodes: 'List[BaseNode]') -> 'None':
    for node in nodes:
        node.blockchain.append(BaseBlock())
        
# NOTE: `nodes` should come from `configuration.NODES`
def reset_nodes(nodes: 'List[BaseNode]') -> 'None':
    for node in nodes:
        node.blockchain = [] # create an array for each miner to store chain state locally
        node.transactionsPool = []
        node.blocks = 0 # total number of blocks mined in the main chain
        node.balance = 0 # to count all reward that a miner made

class BaseNode:
    def __init__(self: 'BaseNode', id: 'int'):
        self.id = id # the uinque id of the node
        self.blockchain = [] # the local blockchain (a list to store chain state locally) for the node
        self.transactionsPool = [] # the transactions pool. Each node has its own pool if and only if Full technique is chosen
        self.blocks = 0 # the total number of blocks mined in the main chain
        self.balance = 0 # the amount of cryptocurrencies a node has

    def last_block(self: 'BaseNode') -> 'BaseBlock':
        return self.blockchain[self.blockchain_length()]
    
    def blockchain_length(self: 'BaseNode') -> 'int':
        return len(self.blockchain) - 1