import random

class SingleGoodHistogram:
    def __init__(self, bucket_size=5, max_bucket=150):
        self.bucket_size = bucket_size
        self.max_bucket = max_bucket
        self.buckets = {}
        for b in range(0, max_bucket + 1, bucket_size):
            self.buckets[b] = 0.0
        self.total = 0.0

    def get_bucket(self, price):
        bucket = int(price // self.bucket_size) * self.bucket_size
        if bucket > self.max_bucket:
            bucket = self.max_bucket
        return bucket

    def add_record(self, price):
        """
        Add a price to the histogram.
        Increment the frequency of the bucket that contains the price.
        """
        bucket = ???
        # Update the bucket frequencies
        raise NotImplementedError

    def smooth(self, alpha):
        """
        Smooth the histogram using the technique described in the handout.
        """
        raise NotImplementedError

    def update(self, new_hist, alpha):
        """ 
        Actually updating the histogram with new information: 
        1. Smooth the current histogram.
        2. Add the new histogram to the current histogram.
        """
        raise NotImplementedError

    def sample(self):
        """ 
        Return a random sample from the histogram. 
        """
        raise NotImplementedError
