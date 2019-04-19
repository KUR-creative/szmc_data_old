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


curry = F.curry
rcurry = F.rcurry
partial = F.partial
rpartial = F.rpartial

reduce = functools.reduce
#creduce = F.curry(functools.reduce) # cannot curry reduce,,,??? it's impl issue!!
plus = lambda a,b: a+b
equals = lambda a,b: a == b 
sub1 = lambda x: x - 1

first = F.first
second = F.second
nth = F.nth

cnth = F.curry(F.nth)
remove = F.remove
lremove = F.lremove
cremove = F.curry(F.remove)
clremove = F.curry(F.lremove)

#ckeep = F.curry(F.keep) # doesn't work!!!
# use partial..
keep = F.keep

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
cfilter = F.curry(F.filter)

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

idx_enum = F.first
val_enum = F.second
negate = lambda x: (not x)
def negated(predicate) -> bool:
    return wrap(predicate, negate)

def nths(seq, idxs):
    return map( rcurry(nth)(unzip(seq)), idxs ) 

import unittest
class Test_fp(unittest.TestCase):
    def test_negated(self):
        pred = lambda x: x != 1
        self.assertEqual( pred(1), negated(negated(pred))(1) )
        self.assertEqual( pred(0), negated(negated(pred))(0) )
        self.assertNotEqual( pred(1), negated(pred)(1) )
        self.assertNotEqual( pred(0), negated(pred)(0) )

if __name__ == '__main__':
    unittest.main()
