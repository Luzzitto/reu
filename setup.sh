#!/bin/bash

mkdir code
mv $(ls -I code README.md) code

mkdir datasets
mkdir models
mkdir jobs
mkdir trains
mkdir preds

mv code/job.slurm jobs
