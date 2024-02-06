#!/bin/bash

mkdir code
mkdir datasets
mkdir models
mkdir jobs
mkdir trains
mkdir preds

mv job.slurm jobs
mv $(ls -I code README.md) code