import random
import configuration
from typing import Any, List, Tuple
from copy import deepcopy
from models.BaseTransaction import BaseTransaction

class FullTransactionContext:
    
    def __init__(self: 'FullTransactionContext') -> 'None':
        self.transaction_count_during_simulation = configuration.TRANSACTIONS_PER_SECOND * configuration.SIMULATION_LENGTH_IN_SECONDS

    def create_transactions(self: 'FullTransactionContext') -> 'None':
        for _ in range(self.transaction_count_during_simulation):
            
            transaction = BaseTransaction()

            transaction.id = random.randrange(100000000000)

            creation_time = random.randint(0, configuration.SIMULATION_LENGTH_IN_SECONDS - 1)
            receive_time = creation_time
            transaction.timestamp = [creation_time, receive_time]

            sender = random.choice(configuration.NODES)
            transaction.sender = sender.id

            transaction.to = random.choice(configuration.NODES).id
            transaction.size = random.expovariate(1 / configuration.AVERAGE_TRANSACTION_SIZE_IN_MB)
            transaction.fee = random.expovariate(1 / configuration.AVERAGE_TRANSACTION_FEE)

            sender.transactionsPool.append(transaction)

    def propogate_transaction(self: 'FullTransactionContext', transaction: 'BaseTransaction') -> 'None':
        for node in configuration.NODES:
            if transaction.sender == node.id:
                continue

            propogated_transaction = deepcopy(transaction)
            propogated_transaction.timestamp[1] += Network.tx_prop_delay() # FIXME
            node.transactionsPool.append(propogated_transaction)

    def execute_transactions(self: 'FullTransactionContext', miner: 'Any', currentTime: 'float') -> 'Tuple[List[BaseTransaction], float]':
        transactions = []
        block_size = 0

        sorted_transactions = sorted(miner.transactionsPool, key=lambda transaction: transaction.fee, reverse=True)

        for transaction in sorted_transactions:
            # FIXME
            if block_size + transaction.size <= configuration.BLOCK_SIZE_IN_MB and transaction.timestamp[1] <= currentTime:
                block_size += transaction.size
                transactions.append(transaction)

        return transactions, block_size