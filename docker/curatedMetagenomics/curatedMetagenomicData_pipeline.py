#!/usr/bin/env python3
import os
import glob
import sys
import subprocess as sb
import shutil
from utils import *

__author__ = 'Francesco Beghini (francesco.beghini@unitn.it)'
__date__ = 'May 26 2020'

if __name__ == '__main__':
    args = read_params()

    sample_name = args.sample
    runs = args.runs.split(';')

    ncores = os.environ.get('ncores', 2)
    output_path = os.environ.get('OUTPUT_PATH', os.path.abspath(__file__))
    
    hnn_dir = os.environ.get('hnn_dir')
    if hnn_dir is None:
        sys.exit('hnn_dir env environment variable must be set. Exiting.\n')

    metaphlandb = os.environ.get('metaphlandb')
    if metaphlandb is None:
        sys.exit('metaphlandb env environment variable must be set. Exiting.\n')

    humanndb = os.environ.get('humanndb')
    if humanndb is None:
        sys.exit('humanndb env environment variable must be set. Exiting.\n')
        
    chocophlandir = os.environ.get('chocophlandir')
    if chocophlandir is None:
        sys.exit('chocophlandir env environment variable must be set. Exiting.\n')
    else:
        make_folder(chocophlandir)

    unirefdir = os.environ.get('unirefdir')
    if unirefdir is None:
        sys.exit('unirefdir env environment variable must be set. Exiting.')
    else:
        make_folder(unirefdir)

    if args.demo:
        DEMO_unirefname="uniref90_DEMO_diamond_v201901.tar.gz"
        DEMO_unirefurl="https://www.dropbox.com/s/xaisk05u4l822pl/uniref90_DEMO_diamond_v201901.tar.gz?dl=1"
        DEMO_chocophlanname="DEMO_chocophlan.v296_201901.tar.gz"
        DEMO_chocophlanurl="https://www.dropbox.com/s/66wgnzw0eo1z142/DEMO_chocophlan.v296_201901.tar.gz?dl=1"

        download(DEMO_unirefurl, DEMO_unirefname)
        decompress_tar(DEMO_unirefname, unirefdir)
        os.unlink(DEMO_unirefname)

        download(DEMO_chocophlanurl, DEMO_chocophlanname)
        decompress_tar(DEMO_chocophlanname, chocophlandir)
        os.unlink(DEMO_chocophlanname)
    try:
        sb.check_call(['fasterq-dump', '-h'], stderr=sb.DEVNULL, stdout=sb.DEVNULL)
    except:
        sys.exit('fasterq-dump is not present in the system path. Exiting.\n')

    make_folder('reads')
           
    for run in runs:
        sys.stdout.write('Dumping run {}\n'.format(run))
        sb.check_call(['fasterq-dump', '--threads', ncores, '--split-files', run, '--outdir', 'reads'], stderr=sb.DEVNULL, stdout=sb.DEVNULL)
        sys.stdout.write('Finished downloading of run {}\n'.format(run))

    sys.stdout.write('Downloaded all runs.\n')
    sys.stdout.write('Concatenating runs...\n')

    with open(os.path.join('reads', '{}.fastq'.format(sample_name)), 'w') as sample_file:
        if args.demo:
            with open('{}/tests/data/demo.fastq'.format(hnn_dir)) as demo_fasta:
                shutil.copyfileobj(demo_fasta, sample_file)
        else:
            for fq_path in glob.glob('reads/*.fastq'):
                with open(fq_path) as fq_file:
                    shutil.copyfileobj(fq_file, sample_file)
