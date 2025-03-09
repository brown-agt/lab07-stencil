from marginal_value import calculate_expected_marginal_value
from sample_valuations import additive_valuation, complement_valuation, substitute_valuation, randomized_valuation
from independent_histogram import IndependentHistogram


def local_bid(goods, valuation_function, price_distribution, num_iterations=100, num_samples=50):
    """
    Iteratively computes a bid vector by updating bids to be the expected marginal value for each good.
    """
    bid_vector = {good: 0.0 for good in goods}
    for _ in range(num_iterations):
        new_bid_vector = {}
        #print(bid_vector)
        for good in goods:
            mv = calculate_expected_marginal_value(goods, good, valuation_function, bid_vector, price_distribution, num_samples)
            new_bid_vector[good] = mv
        bid_vector = new_bid_vector
    return bid_vector

if __name__ == "__main__":
    def valuation(bundle): 
        if len(bundle) == 1: 
            return 10 
        elif len(bundle) == 2:
            return 80 
        elif len(bundle) == 3: 
            return 50 
        else: 
            return 0
    
    print(local_bid(
        goods=["a", "b", "c"],
        valuation_function=valuation,
        price_distribution=IndependentHistogram(["a", "b", "c"], 
                                                [5, 5, 5], 
                                                [100, 100, 100]),
        num_iterations=10,
        num_samples=1000
    ))