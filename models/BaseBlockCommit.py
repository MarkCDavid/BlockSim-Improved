import Configuration
from core.Event import Event
from models.BaseBlock import BaseBlock
from models.BaseNode import BaseNode

class BaseBlockCommit:

    def __init__(self: 'BaseBlockCommit') -> 'None':
        pass

    def handle_event(self: 'BaseBlockCommit', event: 'Event') -> 'None':
        if event.type == "create_block":
            self.generate_block(event)
        elif event.type == "receive_block":
            self.receive_block(event)

    def generate_block (self: 'BaseBlockCommit', event: 'Event') -> 'None':
        pass

    def receive_block (self: 'BaseBlockCommit', event: 'Event') -> 'None':
        pass

    def generate_next_block(self: 'BaseBlockCommit', event: 'Event', currentTime: 'float') -> 'None':
        pass

    def generate_initial_events(self: 'BaseBlockCommit') -> 'None':
        pass

    def propagate_block(self: 'BaseBlockCommit', block: 'BaseBlock') -> 'None':
        pass

    def update_local_blockchain(self: 'BaseBlockCommit', targetNode: 'BaseNode', sourceNode: 'BaseNode', depth: 'int'):
        for index in range(depth):
            if (index < len(targetNode.blockchain)):
                targetNode.blockchain[index] = sourceNode.blockchain[index]
            else:
                targetNode.blockchain.append(sourceNode.blockchain[index])

            if Configuration.HAS_TRANSACTIONS and Configuration.TRANSACTION_TECHNIQUE == "Full": 
                self.update_transactionsPool(targetNode, targetNode.blockchain[index])

    
    # FIXME: Better naming?
    # Removes transactions from the local pool that are already commited in the block.
    def update_transactionsPool(self: 'BaseBlockCommit', node: 'BaseNode', block: 'BaseBlock'):
        block_transactions_ids = [transaction.id for transaction in block.transactions]
        node.transactionsPool = [transaction for transaction in node.transactionsPool if transaction.id not in block_transactions_ids]

