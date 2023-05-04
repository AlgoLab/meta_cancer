import re
import numpy as np
import pandas as pd
from math import log

def get_ll_from_output(path):
    if 'pso' in path:
        fname = path.replace(".best.gv", ".results.log")
    elif 'gp' in path or 'vns' in path:
        fname = path.replace(".gv", ".txt")
    elif 'sasc' in path:
        fname = path
    with open(fname, 'r') as fin:
        lines = fin.readlines()
    for line in lines:
        m = re.search(r'>> Final likelihood: (.+)$', line)
        if m:
            return float(m.group(1))
        m = re.search(r'Likelihood: \[(.+?)\]$', line)
        if m:
            return float(m.group(1))
        m = re.search(r'label="Confidence score: (.+?)";', line)
        if m:
            return float(m.group(1))
    return 0
        

def ll(tools_files, tool_names, exp, outdir):    

    tools = [[] for _ in enumerate(tools_files)]

    for t_ix, t_files in enumerate(tools_files):
        for f in t_files:
            s = get_ll_from_output(f)
            tools[t_ix].append(
                s
            )

    lh_np = np.zeros((len(tools_files[0]), len(tools)))

    for tool_ix, _ in enumerate(tools):
        for sim_ix, _ in enumerate(tools_files[0]):
            lh_np[sim_ix][tool_ix] = tools[tool_ix][sim_ix]

    for idx, name in enumerate(tool_names):
        print("%s -- Log-Likelihood: %f" %
            (name, np.mean(lh_np[idx]))
        )
    print('-'*40)

    # # ---------------- Compile Pandas

    df = pd.DataFrame(lh_np, columns=tool_names).assign(Measure='Log-Likelihood')
    df.to_csv(f'{outdir}/{exp}.loglikelihood.csv', index=False)
    
    

if __name__ == '__main__':
    import sys
    print(get_ll_from_output(sys.argv[1]))