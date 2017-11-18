#!/usr/bin/env python

#!/usr/bin/env python
"""
bloom-filter.py

This file contains an implementation of a bloom filter as outlined in
https://en.wikipedia.org/wiki/Bloom_filter
"""

import mmh3

class BloomFilter(object):
    """
    Basic implementation of a bloom filter, using extra bits for
    counting so deletions are possible up to a point.

    Uses murmurhash3 to build the hashing
    """

    def __init__(self, capacity, num_hashes=5, counting_bits=4):
        if counting_bits > 8:
            raise ValueError("""The number of bits dedicated to counting each
element in the hash range can not exceed 8.""")
        self.num_hashes = num_hashes
        self.capacity = capacity
        self.bitarray = bitarray(capacity * counting_bits)
        self.bitarray.setall(False)

    def make_hashes(self, hashable):
        prehash1 = mmh3.hash(hashable, 0)
        prehash2 = mmh3.hash(hashable, prehash1)

        return [(prehash1 + i * prehash2) % self.capacity for i in range(self.num_hashes)]

    def contains(self, hashable):
        hashes = self.make_hashes(hashable)
        return all(self.has_hash(h) for h in hashes)

    def insert(self, hashable):
        hashes = self.make_hashes(hashable)
        for h in hashes:
            self.increment_hash(h)

    def remove(self, hashable):
        hashes = self.make_hashes(hashable)
        for h in hashes:
            self.decrement_hash(h)

    def get_bits(self, index):
        start = index * self.counting_bits
        end = start + self.counting_bits
        return self.bitarray[start:end]

    def set_bits(self, index, bits):
        start = index * self.counting_bits
        end = start + self.counting_bits
        self.bitarray[start:end] = bits

    def has_hash(self, h):
        return self.get_bits(h).any()

    def increment_hash(self, h):
        bits = self.get_bits(h)
        if bits.all():
            # We've reached the max count. Can't safely increment.
            return
        val = int(bits.to01(), 2)
        incremented_bits = bitarray()
        incremented_bits.frombytes(chr(val+1))
        set_bits(h, incremented_bits[-self.counting_bits:])

    def decrement_hash(self, h):
        bits = self.get_bits(h)
        if bits.all():
            # We've reached the max count. Can's safely decrement.
        val = int(bits.to01(), 2)
        incremented_bits = bitarray()
        incremented_bits.frombytes(chr(val-1))
        set_bits(h, incremented_bits[-self.counting_bits:])


if __name__ == '__main__':
    bloom = BloomFilter()
    d = {}
    data = [chr(num) for num in range(ord('a'), ord('z')+1)]
