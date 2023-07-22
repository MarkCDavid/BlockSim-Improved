from typing import List, Tuple
from models.BaseNode import BaseNode
from models.BaseTransaction import BaseTransaction

class BaseTransactionContext:

    def create_transactions(self: 'BaseTransactionContext') -> 'None':
        pass

    def propogate_transaction(self: 'BaseTransactionContext', transaction: 'BaseTransaction') -> 'None':
        pass

    def execute_transactions(self: 'BaseTransactionContext', miner: 'BaseNode', currentTime: 'float') -> 'Tuple[List[BaseTransaction], float]':
        pass