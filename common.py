
class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance  


class DotDict(dict):

    def __getattr__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return getattr(dict, key)

    def __setattr__(self, key, val):
        dict.__setitem__(self, key, val)