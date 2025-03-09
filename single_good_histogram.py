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
        bucket = self.get_bucket(price)
        self.buckets[bucket] += 1.0
        self.total += 1.0

    def smooth(self, alpha):
        for key in self.buckets:
            self.buckets[key] *= (1 - alpha)
        self.total = sum(self.buckets.values())

    def update(self, new_hist, alpha):
        self.smooth(alpha)
        for key in self.buckets:
            self.buckets[key] += new_hist.buckets.get(key, 0)
        self.total = sum(self.buckets.values())

    def sample(self):
        if self.total == 0:
            return random.uniform(0, self.max_bucket)
        r = random.uniform(0, self.total)
        cumulative = 0.0
        for key in sorted(self.buckets.keys()):
            cumulative += self.buckets[key]
            if r <= cumulative:
                return key + random.uniform(0, self.bucket_size)
        return self.max_bucket
