from typing import List
import Configuration
from models.BaseBlock import BaseBlock
from models.BaseConsensus import BaseConsensus
from models.BaseNode import BaseNode


class BaseIncentives:

    def distribute_rewards(self: 'BaseIncentives', nodes: 'List[BaseNode]', consensus: 'BaseConsensus'):
        for block in consensus.global_chain:
            for node in nodes:
                if block.miner != node.id:
                    continue

                node.blocks += 1
                node.balance += Configuration.BLOCK_REWARD
                node.balance += self.transactions_fee(block)

    # FIXME: Move to the BaseBlock
    def transactions_fee(self: 'BaseIncentives', block: 'BaseBlock') -> 'float':
        return sum(transaction.fee for transaction in block.transactions)
