class CurrencyCalculator:
    def __init__(self):
        self.total = 0

    def add_currency(self, label, value):
        """
        Always add value.
        Same currency can be counted multiple times.
        """
        self.total += value
        return True

    def get_total(self):
        return self.total

    def reset(self):
        self.total = 0
