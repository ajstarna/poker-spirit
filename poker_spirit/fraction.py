class Fraction:
    def __init__(self, n = 0, d = 0):
        self._n = n
        self._d = d

    @property
    def numerator(self):
        return self._n

    @numerator.setter
    def numerator(self, val):
        self._n = val

    @property
    def denominator(self):
        return self._d

    @denominator.setter
    def denominator(self, val):
        self._d = val

    def get_percent(self, precision=1):
        if self._d == 0:
            return 0.0
        
        return round(100*self._n/self._d, precision)

    def __str__(self):
        return f'{self._n}/{self._d}'
