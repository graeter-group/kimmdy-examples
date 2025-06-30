#!/bin/env bash

module purge
module use /hits/fast/mbm/hartmaec/sw/easybuild/modules/all
module load GROMACS/2022.5-plumed2.9_runtime--cuda-11.5

ml load Python/3.10.4-GCCcore-11.3.0
source /hits/fast/mbm/hartmaec/workdir/collagen_HAT/.venv_kimmdy_full/bin/activate
#source /hits/fast/mbm/hartmaec/workdir/collagen_HAT/.venv_kimmdy_GPU_Denis/bin/activate

