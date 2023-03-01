#!/bin/bash

set -ex

export AUTO_QC_HOME=/Users/cslater/projects/AutoQC
export AUTO_QC_PIPELINE_ROOT=/Users/cslater/projects/auto-qc-pipeline
export PYTHONPATH="$AUTO_QC_PIPELINE_ROOT/src:/Users/cslater/projects/AutoQC"
export PYTHONUNBUFFERED=1
export WOD_GZ_DATA=/Users/cslater/Desktop/wod/wod18
export WOD_UNGZ_DATA=/Users/cslater/Desktop/wod/wod18-tmp
export AUTO_QC_OUTPUT=/Users/cslater/Desktop/wod/wod18-out
export AUTO_QC_PIPELINE_UNZIP_CONCUR=3
export AUTO_QC_PIPELINE_TEST_CONCUR=4
export RUN_ONLY_IQUOD=False
export AUTO_QC_LOGGING_YAML=/Users/cslater/projects/auto-qc-pipeline/test-resources/logging.yaml

#python $AUTO_QC_PIPELINE_ROOT/src/autoqc_pipeline/application/run.py
nohup python $AUTO_QC_PIPELINE_ROOT/src/autoqc_pipeline/application/run.py > aqcp.log 2>&1 & 


