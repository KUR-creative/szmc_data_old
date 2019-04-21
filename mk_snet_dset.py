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

print('dev',dev57idxs, 'test',test28idxs, 'train',train200idxs, sep='\n')

idxs_rdt = { # rdt = tRain / Dev / Test
    200:[train200idxs, dev57idxs, test28idxs],
   #150:3/4 200_idxs_rdt
   #100:2/3 150_idxs_rdt
   #50: 1/2 100_idxs_rdt
}

# img_paths
# rbk_paths
# wk_paths

# rbk_origin_map
# wk_origin_map

# mkdir ./snet_data/190421/
# 
