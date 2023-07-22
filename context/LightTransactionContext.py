import random
import Configuration
from typing import List, Tuple
from models.BaseNode import BaseNode
from models.BaseTransaction import BaseTransaction


class LightTransactionContext:

    def __init__(self: 'LightTransactionContext', nodes: 'List[BaseNode]') -> 'None':
        self.nodes = nodes
        self.pending_transactions = []
        self.transaction_count_in_block = Configuration.TRANSACTIONS_PER_SECOND * Configuration.AVERAGE_BLOCK_INTERVAL_IN_SECONDS

    def create_transactions(self: 'LightTransactionContext'):
        for _ in range(self.transaction_count_in_block):
            transaction = BaseTransaction()

            transaction.id = random.randrange(100000000000)
            transaction.sender = random.choice(self.nodes).id
            transaction.to = random.choice(self.nodes).id
            transaction.size = random.expovariate(1 / Configuration.AVERAGE_TRANSACTION_FEE)
            transaction.fee = random.expovariate(1 / Configuration.AVERAGE_TRANSACTION_SIZE_IN_MB)

            self.pending_transactions.append(transaction)

        random.shuffle(self.pending_transactions)


    def execute_transactions(self: 'LightTransactionContext') -> 'Tuple[List[BaseTransaction], float]':
        transactions = []
        block_size = 0

        sorted_transactions = sorted(self.pending_transactions, key=lambda transaction: transaction.fee, reverse=True)

        for transaction in sorted_transactions:
            if block_size + transaction.size <= Configuration.BLOCK_SIZE_IN_MB:
                block_size += transaction.size
                transactions.append(transaction)

        return transactions, block_size