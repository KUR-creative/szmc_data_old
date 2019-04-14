import funcy as F
import functools

def wrap(f, wrapper):
    @functools.wraps(f)
    def wrapped(*args, **kargs):
        return wrapper(f(*args,**kargs))
    return wrapped

pipe = F.rcompose
cmap = F.curry(F.map)
clmap = F.curry(F.lmap)
tup = lambda f: lambda argtup: f(*argtup)
into = lambda f: lambda xs: F.walk(f, xs)
ginto = lambda f: lambda xs: map(f, xs)
linto = lambda f: lambda xs: list(map(f, xs))
