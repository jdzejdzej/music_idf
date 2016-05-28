from domain.hash_calculator import HashCalculator, array

class TestGetBins:

    def test_empty_frequencies_raises_index_error(self):
        c = HashCalculator()
        frequencies = []
        try:
            c.get_bins(frequencies)
            assert False
        except IndexError:
            assert True

    def test_frequencies_wrong_length(self):
        c = HashCalculator()
        frequencies = [0] * 4
        try:
            c.get_bins(frequencies)
            assert False
        except ValueError:
            assert True

    def test_zeros_frequencies(self):
        c = HashCalculator()
        frequencies = [0] * 300
        result = c.get_bins(frequencies)
        assert ([40, 60, 100, 180] == result).all()

    def test_range_frequencies(self):
        c = HashCalculator()
        frequencies = range(300)
        result = c.get_bins(frequencies)
        assert ([59, 99, 179, 299] == result).all()


class TestGetHash:

    def test_empty_bins_raises_value_error(self):
        bins = array([])
        c = HashCalculator()
        try:
            c.get_hash(bins)
            assert False
        except ValueError:
            assert True

    def test_wrong_size_bins(self):
        bins = array([0]*5)
        c = HashCalculator()
        try:
            c.get_hash(bins)
            assert False
        except ValueError:
            assert True

    def test_zeros_bins(self):
        bins = array([0] * 4)
        c = HashCalculator()
        assert 0 == c.get_hash(bins)

    def test_some_bins(self):
        bins = array([1, 2, 3, 4])
        c = HashCalculator()
        assert 131588 == c.get_hash(bins)