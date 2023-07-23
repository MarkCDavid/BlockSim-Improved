import random
from typing import List
import numpy as np

import Configuration
from models.BaseConsensus import BaseConsensus
from models.BaseNode import BaseNode

class Consensus(BaseConsensus):

    def __init__(self: 'Consensus', nodes: 'List[BaseNode]') -> 'None':
        super().__init__()
        self.nodes = nodes

    def Protocol(self: 'Consensus', miner: 'BaseNode'):
        TOTAL_HASHPOWER = sum([node.hashPower for node in self.nodes])
        hashPower = miner.hashPower/TOTAL_HASHPOWER
        return random.expovariate(hashPower * 1 / Configuration.AVERAGE_BLOCK_INTERVAL_IN_SECONDS)

    def fork_resolution(self: 'Consensus'):
        
        max_blockchain_length = max(node.blockchain_length() for node in self.nodes)

        miners_with_blockchains_of_max_length = [
            miner.id 
            for miner 
            in self.nodes 
            if miner.blockchain_length() == max_blockchain_length
        ]

        if len(miners_with_blockchains_of_max_length) > 1:
            miners_with_blockchains_of_max_length = [np.argmax(np.bincount([
                miner.last_block().miner
                for miner
                in self.nodes
                if miner.blockchain_length() == max_blockchain_length
            ]))]

        miner_with_blockchain_of_max_length = miners_with_blockchains_of_max_length[0]

        for miner in self.nodes:
            if miner.blockchain_length() == max_blockchain_length and miner.last_block().miner == miner_with_blockchain_of_max_length:
                self.global_chain = miner.blockchain.copy()
                break
