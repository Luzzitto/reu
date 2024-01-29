#!/bin/bash

#SBATCH --job-name clean_train
#SBATCH --output=clean_50ep_1280imgz_1b
#SBATCH --partition gpu
#SBATCH --gres gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ltupa001@odu.edu

module load container_env python3/2023

crun -p ~/envs/ultralytics yolo segment train data=reu/base/base.yaml model=model=models/yolov8x-seg.pt epochs=100 imgsz=1280 device=0 project=output name=base batch=1
