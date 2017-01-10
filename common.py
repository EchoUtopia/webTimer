
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class DotDict(dict):

    def __getattr__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return getattr(dict, key)

    def __setattr__(self, key, val):
        dict.__setitem__(self, key, val)