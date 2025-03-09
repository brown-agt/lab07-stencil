from single_good_histogram import SingleGoodHistogram

class IndependentHistogram:
    def __init__(self, goods, bucket_sizes, max_buckets):
        self.bucket_sizes = bucket_sizes
        self.max_buckets = max_buckets
        self.histograms = {}
        for good, bucket_size, max_bucket in zip(goods, bucket_sizes, max_buckets):
            self.histograms[good] = SingleGoodHistogram(bucket_size, max_bucket)

    def add_record(self, price_vector):
        for good, price in price_vector.items():
            if good in self.histograms:
                self.histograms[good].add_record(price)

    def update(self, new_data, alpha):
        for good in self.histograms:
            self.histograms[good].update(new_data.histograms[good], alpha)

    def sample(self):
        sample_vector = {}
        for good, hist in self.histograms.items():
            sample_vector[good] = hist.sample()
        return sample_vector

    def copy(self):
        new_ind = IndependentHistogram(list(self.histograms.keys()), self.bucket_sizes, self.max_buckets)
        for good, hist in self.histograms.items():
            new_hist = new_ind.histograms[good]
            new_hist.buckets = hist.buckets.copy()
            new_hist.total = hist.total
        return new_ind
