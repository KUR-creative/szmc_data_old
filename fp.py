import funcy as F
import functools

def wrap(f, wrapper):
    @functools.wraps(f)
    def wrapped(*args, **kargs):
        return wrapper(f(*args,**kargs))
    return wrapped

def unzip(zipped):
    return zip(*zipped)

flip = lambda f: lambda *args,**kargs: f(*reversed(args),**kargs)

partial = F.partial
curry = F.curry
tap = F.tap
flatten = F.flatten
pipe = F.rcompose
map = F.map
repeat = F.repeat
cmap = F.curry(F.map)
clmap = F.curry(F.lmap)
tup = lambda f: lambda argtup: f(*argtup)
into = lambda f: lambda xs: F.walk(f, xs)
ginto = lambda f: lambda xs: map(f, xs)
linto = lambda f: lambda xs: list(map(f, xs))
