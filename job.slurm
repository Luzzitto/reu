#!/bin/bash

#SBATCH --job-name a100-train
#SBATCH --output=
#SBATCH --partition high-gpu-mem
#SBATCH --gres gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ltupa001@odu.edu

module load container_env python3/2023

crun -p ~/envs/ultralytics yolo segment train data=$1 model=$2 epochs=$3 imgsz=$4 batch=$5 device=0 project=$6 name=$7

# Example
# sbatch job.slurm datasets/clean/clean.yaml models/yolov8x-seg.pt 100 1280 1 ../trains clean "Baseline model for future references"