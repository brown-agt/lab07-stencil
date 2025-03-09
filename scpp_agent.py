import random
import pickle
import os
from agt_server.agents.base_agents.sa_agent import SimultaneousAuctionAgent
from agt_server.agents.test_agents.sa.truth_bidder.my_agent import TruthfulAgent
from independent_histogram import IndependentHistogram
from localbid import local_bid
from sample_valuations import additive_valuation

class SCPPAgent(SimultaneousAuctionAgent):
    def setup(self):
        # NOTE: Many internal methods (e.g. self.get_valuations) aren't available during setup.
        # So we delay any setup that requires those until get_action() is called.
        
        self.simulation_count = 0
        self.NUM_SIMULATIONS_PER_ITERATION = 10
        self.ALPHA = 0.1
        self.num_iterations_localbid = 100
        self.num_samples = 50
        self.distribution_file = f"learned_distribution_{self.name}.pkl"

        self.valuation_function = None
        self.learned_distribution = None
        self.curr_distribution = None

    def calculate_valuation(self, bundle):
        """
        Internal method to calculate the valuation of a bundle.
        Here we use an additive valuation based on self.get_valuations().
        """
        valuations = self.get_valuations()
        return additive_valuation(bundle, valuations)

    def load_distribution(self):
        """
        Load the learned distribution from disk, if it exists.
        """
        if os.path.exists(self.distribution_file):
            with open(self.distribution_file, "rb") as f:
                self.learned_distribution = pickle.load(f)
            self.curr_distribution = self.learned_distribution.copy()
        else:
            self.initialize_distribution()

    def save_distribution(self):
        """
        Save the learned distribution to disk.
        """
        with open(self.distribution_file, "wb") as f:
            pickle.dump(self.learned_distribution, f)

    def initialize_distribution(self):
        """
        Initialize the learned distribution using the goods and default parameters.
        We assume bucket sizes of 5 and max values of 100 per good.
        """
        self.learned_distribution = IndependentHistogram(
            self.goods,
            bucket_sizes=[5 for _ in range(len(self.goods))],
            max_buckets=[100 for _ in range(len(self.goods))]
        )
        self.curr_distribution = self.learned_distribution.copy()
    
    def get_action(self):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        In RUN mode, load the distribution from disk.
        In TRAIN mode, initialize a new distribution if needed.
        """
        self.valuation_function = self.calculate_valuation

        self.load_distribution()

        return self.get_bids()
    
    def get_bids(self):
        bids = local_bid(
            self.goods,
            self.valuation_function,
            self.learned_distribution,
            num_iterations=self.num_iterations_localbid,
            num_samples=self.num_samples
        )
        return bids

    def update(self):
        price_history = self.get_price_history()
        if not price_history:
            return

        observed_prices = price_history[-1]
        # print(price_history)
        if observed_prices:
            self.curr_distribution.add_record(observed_prices)
            self.simulation_count += 1

            if self.simulation_count % self.NUM_SIMULATIONS_PER_ITERATION == 0:
                self.learned_distribution.update(self.curr_distribution, self.ALPHA)
                self.curr_distribution = self.learned_distribution.copy()
                print("Saving learned distribution to disk.")
                self.save_distribution()

################### SUBMISSION #####################
agent_submission = SCPPAgent("SCPP Agent")
####################################################

if __name__ == "__main__":
    import argparse
    import time
    from agt_server.local_games.sa_arena import SAArena

    parser = argparse.ArgumentParser(description='SCPP Agent')
    parser.add_argument('--join_server', action='store_true',
                        help='Connects the agent to the server')
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port number (default: 8080)')
    parser.add_argument('--mode', type=str, default='TRAIN',
                        help='Mode: TRAIN or RUN (default: TRAIN)')

    args = parser.parse_args()

    if args.join_server:
        agent_submission.connect(ip=args.ip, port=args.port)
    elif args.mode == "TRAIN":
        arena = SAArena(
            timeout=1,
            num_goods=3,
            num_rounds=100,
            valuation_type="randomized",
            players=[
                agent_submission,
                SCPPAgent("Agent_1"),
                SCPPAgent("Agent_2"),
                SCPPAgent("Agent_3"),
                SCPPAgent("Agent_4"),
                SCPPAgent("Agent_5"),
                SCPPAgent("Agent_6"),
            ]
        )
        start = time.time()
        arena.run()
        end = time.time()
        print(f"{end - start} Seconds Elapsed")
    else:
        arena = SAArena(
            timeout=1,
            num_goods=3,
            num_rounds=100,
            valuation_type="randomized",
            players=[
                agent_submission,
                TruthfulAgent("Agent_1"),
                TruthfulAgent("Agent_2"),
                TruthfulAgent("Agent_3"),
                TruthfulAgent("Agent_4"),
                TruthfulAgent("Agent_5"),
                TruthfulAgent("Agent_6"),
            ]
        )
        start = time.time()
        arena.run()
        end = time.time()
        print(f"{end - start} Seconds Elapsed")
