import funcy as F
import functools
import itertools

def wrap(f, wrapper):
    @functools.wraps(f)
    def wrapped(*args, **kargs):
        return wrapper(f(*args,**kargs))
    return wrapped

def unzip(zipped):
    return zip(*zipped)

@F.curry
def foreach(f, seq):
    for elem in seq:
        f(elem)
permutations = itertools.permutations
lpermutations = lambda seq: list(itertools.permutations(seq))

reduce = functools.reduce
#creduce = F.curry(functools.reduce) # cannot curry reduce,,,??? it's impl issue!!
plus = lambda a,b: a+b
sub1 = lambda x: x - 1

first = F.first
remove = F.remove
lremove = F.lremove
cremove = F.curry(F.remove)
clremove = F.curry(F.lremove)

partial = F.partial
curry = F.curry
tap = F.tap
#ctap = F.curry(F.tap) #TODO

chunks = F.chunks
cchunks = F.curry(F.chunks)
clchunks = F.curry(F.lchunks)

flatten = F.flatten
lflatten = F.lflatten
cat = F.cat
lcat = F.lcat

ilen = F.ilen
pipe = F.rcompose

walk = F.walk
cwalk = F.curry(F.walk)
map = F.map
lmap = F.lmap
cmap = F.curry(F.map)
clmap = F.curry(F.lmap)

cmapcat = F.curry(F.mapcat)

repeat = F.repeat
pairwise = F.pairwise
butlast = F.butlast
lbutlast = lambda seq: list(F.butlast(seq))
zipdict = F.zipdict
cmerge_with = F.curry(F.merge_with)
merge = F.merge

tup = lambda f: lambda argtup: f(*argtup)
into = lambda f: lambda xs: F.walk(f, xs)
ginto = lambda f: lambda xs: map(f, xs)
linto = lambda f: lambda xs: list(map(f, xs))
flip = lambda f: lambda *args,**kargs: f(*reversed(args),**kargs)
