import pandas
import Configuration
from typing import List
from models.BaseNode import BaseNode
from models.BaseConsensus import BaseConsensus


class BaseStatistics:
     
    def __init__(self: 'BaseStatistics', nodes: 'List[BaseNode]', consensus: 'BaseConsensus') -> 'None':
        self.nodes = nodes
        self.consensus = consensus

        self.reset_global_variables()
        self.reset_profit_results()

    def calculate(self: 'BaseStatistics') -> 'None':
        self.global_chain()
        self.blocks_results()
        self.profit_results()

    def global_chain(self: 'BaseStatistics'):
        for block in self.consensus.global_chain:
            self.chain.append([block.depth, block.id, block.previous, block.timestamp, block.miner, len(block.transactions), block.size])

    def blocks_results(self: 'BaseStatistics'):
        transactions = sum(len(block.transactions) for block in self.consensus.global_chain)
        self.main_blocks = len(self.consensus.global_chain) - 1
        self.stale_blocks = self.total_blocks - self.main_blocks
        self.stale_rate = round(self.stale_blocks / self.total_blocks * 100, 2)
        self.block_results.append([self.main_blocks, self.main_blocks, self.stale_blocks, self.stale_rate, transactions])

    def profit_results(self: 'BaseStatistics'):
        for node in self.nodes:
            node_index = self.index + node.id * Configuration.SIMULATION_RUNS

            self.profits[node_index][0] = node.id
            self.profits[node_index][2] = node.blocks
            self.profits[node_index][3] = round(node.blocks / self.main_blocks * 100, 2)
            self.profits[node_index][6] = node.balance

        self.index += 1

    def print_to_excel(self: 'BaseStatistics', fname):

        df1 = pandas.DataFrame({
            'Block Time': [Configuration.AVERAGE_BLOCK_INTERVAL_IN_SECONDS], 
            'Block Propagation Delay': [Configuration.AVERAGE_BLOCK_PROPOGATION_DELAY], 
            'No. Miners': [len(self.nodes)], 
            'Simulation Time': [Configuration.SIMULATION_LENGTH_IN_SECONDS]})

        df2 = pandas.DataFrame(self.block_results)
        df2.columns= ['Total Blocks', 'Main Blocks', 'Stale Blocks', 'Stale Rate', '# transactions']

        df3 = pandas.DataFrame(self.profits)
        df3.columns = ['Miner ID', '% Hash Power','# Mined Blocks', '% of main blocks','# Uncle Blocks','% of uncles', 'Profit (in ETH)']

        df4 = pandas.DataFrame(self.chain)
        df4.columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions', 'Block Size']

        writer = pandas.ExcelWriter(fname, engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='InputConfig')
        df2.to_excel(writer, sheet_name='SimOutput')
        df3.to_excel(writer, sheet_name='Profit')
        df4.to_excel(writer,sheet_name='Chain')

        writer.close()


    def reset_global_variables(self: 'BaseStatistics'):
        self.total_blocks = 0
        self.main_blocks = 0
        self.stale_blocks = 0
        self.stale_rate = 0

    def reset_profit_results(self: 'BaseStatistics'):
        self.block_results = []
        self.profits = [[0 for _ in range(7)] for _ in range(Configuration.SIMULATION_RUNS * Configuration.NODE_COUNT)]
        self.index = 0
        self.chain = []
