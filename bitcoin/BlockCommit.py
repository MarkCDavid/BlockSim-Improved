
import Configuration
from typing import List
from Scheduler import Scheduler
from context.BaseTransactionContext import BaseTransactionContext
from core.Event import Event
from Statistics import BaseStatistics
from core.Network import Network
from models.BaseBlock import BaseBlock
from models.BaseConsensus import BaseConsensus
from models.BaseNode import BaseNode
from models.BaseBlockCommit import BaseBlockCommit

class BlockCommit(BaseBlockCommit):

    def __init__(self: 'BlockCommit', nodes: 'List[BaseNode]', network: 'Network', consensus: 'BaseConsensus', scheduler: 'Scheduler', transaction_context: 'BaseTransactionContext', statistics: 'BaseStatistics') -> 'None':
        self.nodes = nodes
        self.network = network
        self.consensus = consensus
        self.scheduler = scheduler
        self.statistics = statistics
        self.transaction_context = transaction_context

    def generate_block(self: 'BlockCommit', event: 'Event') -> 'None':
        
        miner = self.nodes[event.block.miner]

        if event.block.previous != miner.last_block().id:
            return
        
        self.statistics.total_blocks += 1
        if self.transaction_context:
            transactions, size = self.transaction_context.execute_transactions(miner, event.time)
            event.block.transactions = transactions
            event.block.usedgas = size

        miner.blockchain.append(event.block)

        if self.transaction_context and Configuration.TRANSACTION_TECHNIQUE == "Light":
            self.transaction_context.create_transactions()

        self.propagate_block(event.block)
        self.generate_next_block(miner, event.time)

    def receive_block(self: 'BlockCommit', event: 'Event'):
        miner = self.nodes[event.block.miner]
        recipient = self.nodes[event.node]

        if event.block.previous == recipient.last_block().id:
            recipient.blockchain.append(event.block)

            if self.transaction_context and Configuration.TRANSACTION_TECHNIQUE == "Full": 
                self.update_transactionsPool(recipient, event.block)

            self.generate_next_block(recipient, event.time)

        else:
            depth = event.block.depth + 1
            if (depth > len(recipient.blockchain)):
                self.update_local_blockchain(recipient, miner, depth)
                self.generate_next_block(recipient, event.time)

            if self.transaction_context and Configuration.TRANSACTION_TECHNIQUE == "Full": 
                self.update_transactionsPool(recipient, event.block)

    def generate_next_block(self: 'BlockCommit', node: 'BaseNode', currentTime: 'float') -> 'None':
        if node.hashPower <= 0:
            return

        blockTime = currentTime + self.consensus.Protocol(node)
        self.scheduler.event__create_block(node, blockTime)

    def generate_initial_events(self: 'BlockCommit'):
        for node in self.nodes:
            self.generate_next_block(node, 0)

    def propagate_block(self: 'BlockCommit', block: 'BaseBlock'):
        for recipient in self.nodes:
            if recipient.id == block.miner:
                continue
            blockDelay= self.network.block_propogation_delay()
            self.scheduler.event__receive_block(recipient, block, blockDelay)
