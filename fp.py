import funcy as F
import functools

def wrap(f, wrapper):
    @functools.wraps(f)
    def wrapped(*args, **kargs):
        return wrapper(f(*args,**kargs))
    return wrapped

def unzip(zipped):
    return zip(*zipped)

partial = F.partial
curry = F.curry
tap = F.tap

flatten = F.flatten
lflatten = F.lflatten
cat = F.cat
lcat = F.lcat

ilen = F.ilen
pipe = F.rcompose

map = F.map
lmap = F.lmap
cmap = F.curry(F.map)
clmap = F.curry(F.lmap)

repeat = F.repeat
tup = lambda f: lambda argtup: f(*argtup)

into = lambda f: lambda xs: F.walk(f, xs)
ginto = lambda f: lambda xs: map(f, xs)
linto = lambda f: lambda xs: list(map(f, xs))
flip = lambda f: lambda *args,**kargs: f(*reversed(args),**kargs)

