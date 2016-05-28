from numpy import array, argmax, fromstring, int16, fft, vectorize, split


class HashCalculator(object):
    def __init__(self):
        self.intervals = array([40, 60, 100, 180])
        self.arg_max = vectorize(lambda x: argmax(x))
        self.fuzz = 2

    def from_bytes(self, _bytes):
        time_samples = fromstring(_bytes, dtype=int16)
        frequencies = abs(fft.rfft(time_samples))
        if frequencies.size < 181:
            return None
        bins = self.get_bins(frequencies)
        return self.get_hash(bins)

    def get_hash(self, bins):
        a, b, c, d = bins - bins % self.fuzz
        return ((a << 24) | (b << 16) | (c << 8) | d) & 0xffffffff

    def get_bins(self, frequencies):
        return self.arg_max(split(frequencies, self.intervals))[1:] + self.intervals


# def get_hash(self, bins):
#     return sum((bins - bins % self.fuzz) * self.shifts)
#     # return ((a << 24) | (b << 16) | (c << 8) | d) & 0xffffffff