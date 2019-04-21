import sys
from pathlib import Path
import pandas as pd

import fp

xlsx_path = './snet_data/scores.xlsx'
xlsx_name = Path(xlsx_path).stem

dfs = pd.read_excel(xlsx_path, sheet_name=None)
df = dfs[xlsx_name].fillna(0)
print(df)

paths = df['path'][:-1]
devs  = df['dev' ][:-1]
tests = df['test'][:-1]
'''
print(paths)
print(devs)
print(tests)
'''
#print(list(enumerate(devs[:10])))
selected_idxs = fp.pipe(
    enumerate,
    fp.cremove(fp.tup( lambda i,x: x == 0.0 )),
    fp.clmap( fp.idx_enum ),
    #fp.cmap( fp.tap )
)

dev57idxs   = selected_idxs(devs)
test28idxs  = selected_idxs(tests)
train200idxs= list(fp.sub( 
    fp.pipe(len,range,set)(paths), 
    set(dev57idxs), set(test28idxs),
))

assert fp.pipe(len,range,set)(paths) \
       == set(fp.plus(train200idxs,dev57idxs,test28idxs))

#print('dev',dev57idxs, 'test',test28idxs, 'train',train200idxs, sep='\n')

import random
sample = lambda xs,ratio: random.sample(xs, int(len(xs) * ratio))

full_idxs_list = [train200idxs, dev57idxs, test28idxs]
idxs_rdt = { # rdt = tRain / Dev / Test
    200: full_idxs_list,
    150: fp.clmap(sample, full_idxs_list, [3/4]*3),
    100: fp.clmap(sample, full_idxs_list, [1/2]*3),
     50: fp.clmap(sample, full_idxs_list, [1/4]*3),
}

from pprint import pprint
print('-------200-------')
for x in idxs_rdt[200]: print('------->',x)

print('-------150-------')
for x in idxs_rdt[150]: print('------->',x)

print('-------100-------')
for x in idxs_rdt[100]: print('------->',x)

print('-------50--------')
for x in idxs_rdt[50]: print('------->',x)
# img_paths
# rbk_paths
# wk_paths

# rbk_origin_map
# wk_origin_map

# mkdir ./snet_data/190421/
# 
