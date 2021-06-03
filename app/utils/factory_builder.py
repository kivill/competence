

class ObjectFactory:
    """
    Generate interface of object factory
    """
    def __init__(self):
        self._builders = {}

    def register(self, key, builder):
        self._builders[key] = builder

    def get(self, key):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder

    def create(self, key, *args, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(*args, **kwargs)