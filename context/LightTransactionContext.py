import random
import configuration
from typing import List, Tuple
from models.BaseTransaction import BaseTransaction


class LightTransactionContext:

    def __init__(self: 'LightTransactionContext') -> 'None':
        self.pending_transactions = []
        self.transaction_count_in_block = configuration.TRANSACTIONS_PER_SECOND * configuration.AVERAGE_BLOCK_INTERVAL_IN_SECONDS

    def create_transactions(self: 'LightTransactionContext'):
        for _ in range(self.transaction_count_in_block):
            
            transaction = BaseTransaction()

            transaction.id = random.randrange(100000000000)
            transaction.sender = random.choice(configuration.NODES).id
            transaction.to = random.choice(configuration.NODES).id
            transaction.size = random.expovariate(1 / configuration.AVERAGE_TRANSACTION_FEE)
            transaction.fee = random.expovariate(1 / configuration.AVERAGE_TRANSACTION_SIZE_IN_MB)

            self.pending_transactions.append(transaction)

        random.shuffle(self.pending_transactions)


    def execute_transactions(self: 'LightTransactionContext') -> 'Tuple[List[BaseTransaction], float]':
        transactions = []
        block_size = 0

        sorted_transactions = sorted(self.pending_transactions, key=lambda transaction: transaction.fee, reverse=True)

        for transaction in sorted_transactions:
            if block_size + transaction.size <= configuration.BLOCK_SIZE_IN_MB:
                block_size += transaction.size
                transactions.append(transaction)

        return transactions, block_size