import random
def additive_valuation(bundle, valuations):
    """
    A simple additive valuation: sums the values of individual goods in the bundle.
    `valuations` is a dict mapping each good to its single-item value.
    """
    return sum(valuations.get(g, 0) for g in bundle)

def complement_valuation(bundle, valuations):
    """
    A valuation function that values a bundle more if it contains complementary goods.
    """
    base_value = additive_valuation(bundle, valuations)
    complement_multiplier = 1.2 ** (len(bundle) - 1)
    return base_value * complement_multiplier if bundle else 0

def substitute_valuation(bundle, valuations):
    """
    A valuation function that values a bundle less if it contains substitute goods.
    """
    base_value = additive_valuation(bundle, valuations)
    substitute_multiplier = 0.8 ** (len(bundle) - 1)
    return base_value * substitute_multiplier if bundle else 0

def randomized_valuation(bundle, valuations):
    """
    A valuation function that randomly applies either a complement or substitute effect.
    """
    key = random.randint(0, 2)
    valuation_functions = [
        additive_valuation,
        complement_valuation,
        substitute_valuation
    ]
    return valuation_functions[key](bundle, valuations)

