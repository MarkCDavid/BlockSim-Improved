import Configuration
from models.BaseBlock import BaseBlock
from models.BaseConsensus import BaseConsensus


class Incentives:

    def distribute_rewards(self: 'Incentives', consensus: 'BaseConsensus'):
        for block in consensus.global_chain:
            for node in Configuration.NODES:
                if block.miner != node.id:
                    continue

                node.blocks += 1
                node.balance += Configuration.BLOCK_REWARD
                node.balance += self.transactions_fee(block)

    # FIXME: Move to the BaseBlock
    def transactions_fee(self: 'Incentives', block: 'BaseBlock') -> 'float':
        return sum(transaction.fee for transaction in block.transactions)
