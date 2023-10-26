import random

class RandomDelegate:
    def __getattr__(self, name):
        if hasattr(random, name) and callable(getattr(random, name)):
            return getattr(random, name)
        else:
            raise AttributeError(f"'Random' object has no attribute '{name}'")
