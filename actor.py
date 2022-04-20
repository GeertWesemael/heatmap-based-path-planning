import path


class Actor:
    def __init__(self, path, world):
        self.path = path
        self.map = world

    @classmethod
    def random_walking_actor(cls, fr, to, world):
        return cls(path.Path.random_path(fr, to, world), world)
