import pygame

class PygameDelegate:
    def __getattr__(self, name):
        if hasattr(pygame, name):
            return getattr(pygame, name)
        else:
            raise AttributeError(f"'Pygame' object has no attribute '{name}'")
