class Energy:
    def __init__(self, value: float):
        self.value = value

    def remove(self, value_to_remove: float):
        self.value -= value_to_remove
        if self.value <= 0:
            raise NoMoreEnergy


class NoMoreEnergy(Exception):
    pass
