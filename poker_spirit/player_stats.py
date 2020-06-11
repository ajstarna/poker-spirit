from fraction import Fraction

class PlayerStats:
    def __init__(self, name):
        self._name = name
        self._hands_played = 0
        # Flops seen
        self._fs = 0
        self._vpip = 0
        self._pfr = 0
        self._cpfr = Fraction()
        self._uopfr = Fraction()
        self._3b = Fraction()
        self._f3b = Fraction()
        self._4b = Fraction()
        self._f4b = Fraction()

    @property
    def name(self):
        return self._name

    @property
    def hands_played(self):
        return self._hands_played

    def increase_hands_played(self):
        self._hands_played += 1

    @property
    def fs(self):
        return Fraction(self._fs, self._hands_played)

    def increase_fs(self):
        self._fs += 1

    @property
    def vpip(self):
        return Fraction(self._vpip, self._hands_played)

    def increase_vpip(self):
        self._vpip += 1

    @property
    def pfr(self):
        return Fraction(self._pfr, self._hands_played)

    def increase_pfr(self):
        self._pfr += 1

    @property
    def cpfr(self):
        return self._cpfr

    def increase_cpfr(self):
        self._cpfr.numerator += 1

    def increase_opt_cpfr(self):
        self._cpfr.denominator += 1

    @property
    def uopfr(self):
        return self._uopfr

    def increase_uopfr(self):
        self._uopfr.numerator += 1

    def increase_opt_uopfr(self):
        self._uopfr.denominator += 1

    @property
    def p3b(self):
        return self._3b

    def increase_3b(self):
        self._3b.numerator += 1

    def increase_opt_3b(self):
        self._3b.denominator += 1

    @property
    def f3b(self):
        return self._f3b

    def increase_f3b(self):
        self._f3b.numerator += 1

    def increase_opt_f3b(self):
        self._f3b.denominator += 1

    @property
    def p4b(self):
        return self._4b

    def increase_4b(self):
        self._4b.numerator += 1

    def increase_opt_4b(self):
        self._4b.denominator += 1

    @property
    def f4b(self):
        return self._f4b

    def increase_f4b(self):
        self._f4b.numerator += 1

    def increase_opt_f4b(self):
        self._f4b.denominator += 1

    def __str__(self):
        output = f'{self.name} / #h {self.hands_played} / fs {self.fs} / VPiP {self.vpip}\n'
        output += f'PFR {self.pfr} / CPFR {self.cpfr} / UOPFR {self.uopfr}\n'
        output += f'3B {self.p3b} / F3B {self.f3b} / 4B {self.p4b} / F4B {self.f4b}'
        return output
