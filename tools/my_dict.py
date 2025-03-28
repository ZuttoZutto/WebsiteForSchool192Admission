# Этот класс позволяет сделать словарь, к элементам которого можно обратится
# через точку кроме обращения по ключу.

class MyDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, item):
        return self.get(item, None)