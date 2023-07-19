from typing import List


class BaseTransaction:
    def __init__(self,
            id: 'int' = 0, # the uinque id or the hash of the transaction
            timestamp: 'int | List[int]' = 0 or [], # the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
            sender: 'int' = 0, # the id of the node that created and sent the transaction
            to: 'int' = 0, # the id of the recipint node
            value: 'int' = 0, # the amount of cryptocurrencies to be sent to the recipint node
            size: 'float' = 0.000546, # the transaction size in MB
            fee: 'int' = 0 # the fee of the transaction (usedGas * gasPrice)
        ):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to= to
        self.value=value
        self.size = size
        self.fee= fee