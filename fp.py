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

def lunzip(zipped):
    return list(zip(*zipped))

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
mul = lambda a,b: a*b
div2 = lambda a,b: a/b
cdiv2 = F.curry(div2)
equals = lambda a,b: a == b 
sub1 = lambda x: x - 1

first = F.first
second = F.second
nth = F.nth
cnth = F.curry(F.nth)

interleave = F.interleave
'''
import types
import inspect
def is_generator(seq):
    return (isinstance(seq, types.GeneratorType)
         or inspect(isgeneratorfunction(seq)))
'''

def list_nths(idxs, li):
    #print(idxs)
    #seq = F.tap(list(seq)[:10], label='seq')
    assert (  isinstance(li, list) 
           or isinstance(li,  str) 
           or isinstance(li,tuple)), 'arg2 "li": %s is not list/str/tuple' % type(li) 
    return map( rcurry(nth)(li), idxs ) 
    #return map(lambda idx: F.tap(nth(idx,seq),label='!!'), idxs)

remove = F.remove
lremove = F.lremove
cremove = F.autocurry(F.remove)
clremove = F.autocurry(F.lremove)

#ckeep = F.curry(F.keep) # doesn't work!!!
# use partial..
keep = F.keep

tap = F.tap
ctap = F.autocurry(F.tap) #TODO

chunks = F.chunks
cchunks = F.autocurry(F.chunks)
clchunks = F.autocurry(F.lchunks)

flatten = F.flatten
lflatten = F.lflatten
cat = F.cat
lcat = F.lcat

ilen = F.ilen
pipe = F.rcompose

walk = F.walk
cwalk = F.autocurry(F.walk)
walk_keys = F.walk_keys
cwalk_keys = F.autocurry(F.walk_keys)
walk_values = F.walk_values
cwalk_values = F.autocurry(F.walk_values)

itervalues = F.itervalues

map = F.map
lmap = F.lmap
cmap = F.autocurry(F.map)
clmap = F.autocurry(F.lmap)
cfilter = F.autocurry(F.filter)

cmapcat = F.autocurry(F.mapcat)

repeat = F.repeat
pairwise = F.pairwise
butlast = F.butlast
lbutlast = lambda seq: list(F.butlast(seq))

zipmap = lambda f,xs: cmap(f,zip(xs))
czipmap = F.autocurry( lambda f,xs: cmap(f,zip(xs)) )
zipwalk = lambda f: pipe(zip, cwalk(f))
czipwalk = F.autocurry( lambda f: pipe(zip, cwalk(f)) )
czipwalk_values = F.autocurry( lambda f: pipe(zip, cwalk_values(f)) )

zipdict = F.zipdict
omit = F.omit
comit = F.autocurry(F.omit)
cmerge_with = F.autocurry(F.merge_with)
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

def construct(dtype):
    def make(*args):
        return dtype([*args])
    return make

tree_nodes = F.tree_nodes
ltree_nodes = F.ltree_nodes
tree_leaves = F.tree_leaves
ltree_leaves = F.ltree_leaves
import unittest
class Test_fp(unittest.TestCase):
    def test_construct(self):
        self.assertEqual(construct(tuple)(),   tuple())
        self.assertEqual(construct(tuple)(1),  (1,)   )
        self.assertEqual(construct(tuple)(1,2),(1,2)  )
        self.assertEqual(construct(list)(),    []   )
        self.assertEqual(construct(list)(1),   [1,] )
        self.assertEqual(construct(list)(1,2), [1,2])

    def test_negated(self):
        pred = lambda x: x != 1
        self.assertEqual( pred(1), negated(negated(pred))(1) )
        self.assertEqual( pred(0), negated(negated(pred))(0) )
        self.assertNotEqual( pred(1), negated(pred)(1) )
        self.assertNotEqual( pred(0), negated(pred)(0) )
    def test_nths(self):
        self.assertEqual(nth(0,[1,2,3]), 1)
        self.assertEqual([ *list_nths([0,2],[1,2,3]) ], [1,3])

        print('ppap')
        self.assertEqual(
            [*list_nths([7,8], [c for c in '0123456789abc'])], ['7','8'] 
        )
        print('ppap2')
        with self.assertRaises(AssertionError):
            [*list_nths([7,8], (c for c in '0123456789abc'))]

    '''
    def test_is_generator(self):
        def gen(xs):
            for x in xs:
                yield x

        self.assertTrue(is_generator(gen))
        self.assertTrue(is_generator(map))
    '''


if __name__ == '__main__':
    unittest.main()
