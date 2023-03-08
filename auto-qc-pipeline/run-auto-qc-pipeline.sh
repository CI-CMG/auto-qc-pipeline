#!/bin/bash

set -ex

export AUTO_QC_HOME=/Users/WOD/AutoQC
export AUTO_QC_PIPELINE_ROOT=/Users/WOD/auto-qc-pipeline
export PYTHONPATH="$AUTO_QC_PIPELINE_ROOT/src:$AUTO_QC_HOME"
export PYTHONUNBUFFERED=1
export WOD_GZ_DATA=/Users/WOD/data-in
export WOD_UNGZ_DATA=/Users/WOD/data-tmp
export AUTO_QC_OUTPUT=/Users/WOD/data-out
export AUTO_QC_PIPELINE_UNZIP_CONCUR=3
export AUTO_QC_PIPELINE_TEST_CONCUR=4
export RUN_ONLY_IQUOD=True
export AUTO_QC_LOGGING_YAML="$AUTO_QC_PIPELINE_ROOT/test-resources/logging.yaml"

python $AUTO_QC_PIPELINE_ROOT/autoqc_pipeline/application/run.py

#nohup python $AUTO_QC_PIPELINE_ROOT/autoqc_pipeline/application/run.py > aqcp.log 2>&1 &


