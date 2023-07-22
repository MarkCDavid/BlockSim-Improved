import Configuration
from context.LightTransactionContext import LightTransactionContext
from context.FullTransactionContext import FullTransactionContext
from core.Network import Network
from core.Queue import Queue
from models.BaseBlockCommit import BaseBlockCommit
from models.BaseConsensus import BaseConsensus
from models.BaseNode import BaseNode, generate_genesis_block, reset_nodes
from models.BaseIncentives import BaseIncentives
from Scheduler import Scheduler
from Statistics import BaseStatistics


from bitcoin.Node import Node
from bitcoin.Consensus import Consensus
from bitcoin.BlockCommit import BlockCommit

def run():
    clock = 0


    nodes = [Node(id=0, hashPower=50), Node(id=1, hashPower=20), Node(id=2, hashPower=30)]
    # nodes = [BaseNode(id) for id in range(Configuration.NODE_COUNT)]

    queue = Queue()

    # consensus = BaseConsensus()
    consensus = Consensus(nodes)

    incentives = BaseIncentives()

    network = Network()

    statistics = BaseStatistics(nodes, consensus)

    scheduler = Scheduler(queue)
    
    if Configuration.HAS_TRANSACTIONS:

        if Configuration.TRANSACTION_TECHNIQUE == "Light":
            transaction_context = LightTransactionContext(nodes)

        elif Configuration.TRANSACTION_TECHNIQUE == "Full":
            transaction_context = FullTransactionContext(nodes, network)

        transaction_context.create_transactions()

    generate_genesis_block(nodes)

    # block_commit = BaseBlockCommit()

    block_commit = BlockCommit(nodes, network, consensus, scheduler, transaction_context, statistics)
    block_commit.generate_initial_events()

    while queue and clock <= Configuration.SIMULATION_LENGTH_IN_SECONDS:
        event = queue.pop()
        clock = event.time
        block_commit.handle_event(event)

    consensus.fork_resolution()
    incentives.distribute_rewards(nodes, consensus)

    statistics.calculate()

    statistics.reset_global_variables()

    reset_nodes(nodes)

    filename = "(Allverify)1day_{0}M_{1}K.xlsx".format(Configuration.BLOCK_SIZE_IN_MB/1000000, Configuration.TRANSACTIONS_PER_SECOND/1000)

    statistics.print_to_excel(filename)

    statistics.reset_profit_results()  

def main():
    for run_index in range(Configuration.SIMULATION_RUNS):
       run()

if __name__ == '__main__':
    main()
