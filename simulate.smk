from os.path import join as pjoin
import sys

args = sys.argv
config_path = args[args.index("--configfile") + 1]

SCGEN_BIN = "/data/software/sc_generator/SCgen.py"
TOT_SIM = config["Settings"]["Simulations"]
SIMS = range(1, TOT_SIM+1)


rule run:
    input:
        expand(
            pjoin(config["Settings"]["Folder"], "sim_{i}_scs.txt"), 
            i=SIMS
            ),

rule simulate:
    input: config_path
    output: 
        sim_scs=expand(pjoin(config["Settings"]["Folder"], "sim_{i}_scs.txt"), i=SIMS)
    shell: 
        """
        python {SCGEN_BIN} -c {input}
        """