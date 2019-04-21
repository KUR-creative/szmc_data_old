import sys
from pathlib import Path
import pandas as pd

import fp

###################### make index table ##########################
xlsx_path = './snet_data/scores.xlsx'
xlsx_name = Path(xlsx_path).stem

dfs = pd.read_excel(xlsx_path, sheet_name=None)
df = dfs[xlsx_name].fillna(0)
print(df)

score_paths = df['path'][:-1]
devs  = df['dev' ][:-1]
tests = df['test'][:-1]
'''
print(score_paths)
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
    fp.pipe(len,range,set)(score_paths), 
    set(dev57idxs), set(test28idxs),
))

assert fp.pipe(len,range,set)(score_paths) \
       == set(fp.plus(train200idxs,dev57idxs,test28idxs))

#print('dev',dev57idxs, 'test',test28idxs, 'train',train200idxs, sep='\n')

import random
sample = lambda xs,ratio: random.sample(xs, int(len(xs) * ratio))
full_idxs_list = [train200idxs, dev57idxs, test28idxs]
keys = ['train','valid','test']
idxs_table = { # rdt = tRain / Dev / Test
    200: fp.zipdict(keys, full_idxs_list),
    150: fp.zipdict(keys, fp.map(sample, full_idxs_list,[3/4]*3)),
    100: fp.zipdict(keys, fp.map(sample, full_idxs_list,[1/2]*3)),
     50: fp.zipdict(keys, fp.map(sample, full_idxs_list,[1/4]*3)),
}
##################################################################

'''
print('-------200-------')
for x in idxs_table[200].items(): print(x)

print('-------150-------')
for x in idxs_table[150].items(): print(x)

print('-------100-------')
for x in idxs_table[100].items(): print(x)

print('-------50--------')
for x in idxs_table[50].items(): print(x)
'''

# img_paths
# rbk_paths
# wk_paths

# rbk_origin_map
# wk_origin_map

# mkdir ./snet_data/190421/
# 
