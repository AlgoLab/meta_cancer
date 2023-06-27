from os.path import join as pjoin
import sys

args = sys.argv
config_path = args[args.index("--configfiles") + 1]

SCGEN_BIN = "/data/software/sc_generator/SCgen.py"
TOT_SIM = config["Settings"]["Simulations"]
TOT_MUTS = config["Settings"]["Mutations"]
SIMS = range(1, TOT_SIM+1)
PSO_BIN = "/data/software/pso-cancer-evolution/psosc.py"
GP_BIN = "/data/software/sci-problem-cancer-evolution/prog/src/genetic_programming_dollo_k/main_gp.py"
VNS_BIN = "/data/software/sci-problem-cancer-evolution/prog/src/vns_dollo_k/main_vns.py"
SASC_BIN = "/data/sasc_rec_test/tools/sasc/sasc"

OUTDIR = "results"
EXPDIR = config_path.replace(".yaml", "")
CSVDIR = "csv"

rule run:
    input:
        # expand(
        #     pjoin(OUTDIR, "gp", EXPDIR, "sim_{i}.gp.gv"),
        #     i=SIMS,
        #     ),
        # expand(
        #     pjoin(OUTDIR, "vns", EXPDIR, "sim_{i}.vns.gv"),
        #     i=SIMS,
        #     ),
        expand(
            pjoin(OUTDIR, "pso", EXPDIR, "sim_{i}.pso.best.gv"),
            i=SIMS,
            ),
        expand(
            pjoin(OUTDIR, "sasc", EXPDIR, "sim_{i}.sasc.mlt.gv"),
            i=SIMS,
            ),
            

rule simulate:
    input: config_path
    output: 
        sim_scs=expand(pjoin(config["Settings"]["Folder"], "sim_{i}_scs.txt"), i=SIMS)
    shell: 
        """
        python {SCGEN_BIN} -c {input}
        """

rule run_pso:
    input:
        scs = pjoin(config["Settings"]["Folder"], "sim_{i}_scs.txt"),
    output:
        gv = pjoin(OUTDIR, "pso", EXPDIR, "sim_{i}.pso.best.gv"),
    benchmark:
        pjoin('benchmark', "pso", EXPDIR, "sim_{i}.pso.best.gv"),
    params:
        particles = 16,
        prefix = "sim_{i}.pso.",
        outdir = pjoin(OUTDIR, "pso", EXPDIR),
        k = config["Settings"]["MaxLosses"],
        d = config["Settings"]["MaxLosses"],
        a = config["Rates"]["FnRate"],
        b = config["Rates"]["FpRate"],
    threads: 8
    shell:
        """
        python {PSO_BIN} -i {input.scs} -p {params.particles} -c {threads} -k {params.k} -a {params.a} -b {params.b} -d {params.d} --outdir {params.outdir} --prefix {params.prefix}
        """

rule convert_to_ea:
    input: 
        scs = pjoin(config["Settings"]["Folder"], "sim_{i}_scs.txt"),
    output: 
        scs = pjoin(config["Settings"]["Folder"], "sim_{i}_scs.ea.txt"),
    run: 
        with open(output.scs, "w") as fout:
            fout.write(' '.join(str(x+1) for x in range(TOT_MUTS)))
            fout.write("\n")
            for line in open(input.scs):
                fout.write(line.replace("2", "?"))


rule run_gp:
    input: 
        scs = pjoin(config["Settings"]["Folder"], "sim_{i}_scs.ea.txt"),
    output: 
        log=pjoin(OUTDIR, "gp", EXPDIR, "sim_{i}.gp.txt"),
        gv=pjoin(OUTDIR, "gp", EXPDIR, "sim_{i}.gp.gv"),
    benchmark:
        pjoin('benchmark', "gp", EXPDIR, "sim_{i}.pso.best.gv"),
    params:
        popsize = 200,
        prefix = "sim_{i}.gp",
        outdir = pjoin(OUTDIR, "gp", EXPDIR),
        k = config["Settings"]["MaxLosses"],
        d = config["Settings"]["MaxLosses"], # do we have it?
        a = config["Rates"]["FnRate"],
        b = config["Rates"]["FpRate"],
        maxgens=0,
        maxtime=3000,
    shell:
        """
        python {GP_BIN} \
        EvaluationType=likelihood-012 \
        MaxFillFactor=6 \
        InputFormat=012 RandomSeed=0 \
        PopulationSize={params.popsize} \
        MaxTimeForExecutionInSeconds={params.maxtime} \
        MaxNumberGenerations={params.maxgens} \
        InputFile={input.scs} \
        DolloK={params.k} \
        Alpha={params.a} \
        Beta={params.b} \
        --outdir {params.outdir} \
        --prefix {params.prefix}
        """ 

rule run_vsn:
    input: 
        scs = pjoin(config["Settings"]["Folder"], "sim_{i}_scs.ea.txt"),
    output: 
        log=pjoin(OUTDIR, "vns", EXPDIR, "sim_{i}.vns.txt"),
        gv=pjoin(OUTDIR, "vns", EXPDIR, "sim_{i}.vns.gv"),
    benchmark:
        pjoin('benchmark', "vns", EXPDIR, "sim_{i}.pso.best.gv"),
    params:
        popsize = 200,
        prefix = "sim_{i}.vns",
        outdir = pjoin(OUTDIR, "vns", EXPDIR),
        k = config["Settings"]["MaxLosses"],
        d = config["Settings"]["MaxLosses"], # do we have it?
        a = config["Rates"]["FnRate"],
        b = config["Rates"]["FpRate"],
        maxiter=0,
        maxtime=3000, 
    shell:
        """
        python {VNS_BIN} \
        EvaluationType=likelihood-012 \
        MaxFillFactor=6 \
        InputFormat=012 RandomSeed=0 \
        MaxTimeForExecutionInSeconds=60 \
        MaxNumberIterations={params.maxiter} \
        InputFile={input.scs} \
        DolloK={params.k} \
        Alpha={params.a} \
        Beta={params.b} \
        --outdir {params.outdir} \
        --prefix {params.prefix}
        """

rule run_sasc:
    input: 
        scs = pjoin(config["Settings"]["Folder"], "sim_{i}_scs.txt"),
    output: 
        gv = pjoin(OUTDIR, "sasc", EXPDIR, "sim_{i}.sasc.mlt.gv"),
        txt = pjoin(OUTDIR, "sasc", EXPDIR, "sim_{i}.sasc.out.txt"),
    benchmark:
        pjoin('benchmark', "sasc", EXPDIR, "sim_{i}.pso.best.gv"),
    params:
        k = config["Settings"]["MaxLosses"],
        d = config["Settings"]["MaxLosses"],
        a = config["Rates"]["FnRate"],
        b = config["Rates"]["FpRate"],
        cells = config["Settings"]["Cells"],
        mutations = config["Settings"]["Mutations"],
        iters = 10,
        s = 100000.0,
        c = 0.001,
        prefix = pjoin(OUTDIR, "sasc", EXPDIR, "sim_{i}.sasc"),
        mkdir=pjoin(OUTDIR, "sasc", EXPDIR)
    threads: 8,
    shell:
        """
        {SASC_BIN} -i {input.scs} \
        -m {params.mutations} \
        -n {params.cells} \
        -b {params.b} -a {params.a} \
        -k {params.k} -d {params.d} -g 1 \
        -r {params.iters} -p {threads} \
        -S {params.s} -C {params.c} \
        -P {params.prefix} -x
        """