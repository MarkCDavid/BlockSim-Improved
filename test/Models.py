import os
import pickle

class Miner:
    def __init__(self, id, hash_power, mined_blocks, profit):
        self.id = id
        self.hash_power = hash_power
        self.mined_blocks = mined_blocks
        self.profit = profit

    def profit_per_block(self):
        return self.profit / self.mined_blocks if self.mined_blocks else 0

    def __str__(self):
        return f'Miner(id={self.id}, hash_power={self.hash_power}, mined_blocks={self.mined_blocks}, profit={self.profit})'


class Run:
    def __init__(self, total_blocks, transactions):
        self.total_blocks = total_blocks
        self.transactions = transactions
        self.miners = []

    def add_miner(self, id, hash_power, mined_blocks, profit):
        self.miners.append(Miner(id, hash_power, mined_blocks, profit))

    def average_transactions(self):
        return self.transactions / len(self.miners) if self.miners else 0

    def average_blocks(self):
        return sum(miner.mined_blocks for miner in self.miners) / len(self.miners) if self.miners else 0

    def average_profit_per_block(self):
        return sum(miner.profit_per_block() for miner in self.miners) / len(self.miners) if self.miners else 0


    def __str__(self):
        return f'Run(total_blocks={self.total_blocks}, transactions={self.transactions}, miners=[\n\t' + ',\n\t'.join(str(miner) for miner in self.miners) + '\n])'


class Simulation:
    def __init__(self, block_time, block_prop_delay, no_miners, sim_time):
        self.block_time = block_time
        self.block_prop_delay = block_prop_delay
        self.no_miners = no_miners
        self.sim_time = sim_time
        self.runs = []

    def add_run(self, run):
        self.runs.append(run)

    def average_transactions_per_run(self):
        return sum(run.average_transactions() for run in self.runs) / len(self.runs) if self.runs else 0

    def average_blocks_per_run(self):
        return sum(run.average_blocks() for run in self.runs) / len(self.runs) if self.runs else 0

    def average_profit_per_block_per_run(self):
        return sum(run.average_profit_per_block() for run in self.runs) / len(self.runs) if self.runs else 0
    
    def is_similar(self, other):
        x = abs(self.average_transactions_per_run() - other.average_transactions_per_run())
        y = abs(self.average_blocks_per_run() - other.average_blocks_per_run())
        z = abs(self.average_profit_per_block_per_run() - other.average_profit_per_block_per_run())
        return (x < 5000, y < 4, z < 50)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(filename, factory):
        if not os.path.exists(filename):
            return factory()
        with open(filename, 'rb') as file:
            return pickle.load(file)
        
    def __str__(self):
        return f'Simulation(block_time={self.block_time}, block_prop_delay={self.block_prop_delay}, no_miners={self.no_miners}, sim_time={self.sim_time}, runs=[\n' + ',\n'.join(str(run) for run in self.runs) + '\n])'