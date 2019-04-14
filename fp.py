import funcy as F
import functools

def wrap(f, wrapper):
    @functools.wraps(f)
    def wrapped(*args, **kargs):
        return wrapper(f(*args,**kargs))
    return wrapped

pipe = F.rcompose
cmap = curry(F.map)
clmap = curry(F.lmap)
tup = lambda f: lambda argtup: f(*argtup)
into = lambda f: lambda xs: walk(f, xs)
