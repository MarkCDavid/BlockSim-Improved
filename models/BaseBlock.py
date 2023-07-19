from typing import Any, List


class BaseBlock:
    def __init__(
            self: 'BaseBlock',
            depth: 'int' = 0, # the index of the block in the local blockchain ledger
            id: 'int' = 0, # the uinque id or the hash of the block
            previous: 'int | None' = None, # the uinque id or the hash of the previous block
            timestamp: 'int' = 0, # the time when the block is created
            miner: 'int | None' = None, # the id of the miner who created the block
            transactions: 'List[Any]' = [], # a list of transactions included in the block
            size: 'float' = 1.0 # the block size in MB
        ):

        self.depth = depth
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions or []
        self.size = size
