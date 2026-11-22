include .env
include ./ml/.env
export

.PHONY: venv
CLI = ./.venv/bin/python3 
PIP = ./.venv/bin/pip3
PATH_TRAIN = ./ml/train.py  
PATH_PREDICT = ./ml/predict.py
PATH_EVALUATE = ./ml/evaluate.py

# Run system through Docker compose
dc-up:
	docker compose up

# Running system through Docker compose
# with waiting getting statues 'healthy' everything service
dc-wait-up:
	docker compose up -d --wait


# Installing python virtual envirement
venv:
	python3 -m venv .venv

# Installing ml package for ML on CPU
ml-lib-cpu: 
	${PIP} install torch torchvision torchaudio   

# Installing utils for mamba
ml-util-mamba: venv 
	${PIP} install --upgrade pip setuptools wheel

# Installing model for CPU
ml-model-cpu: ml-util-mamba ml-lib-cpu
	${PIP} install mamba-ssm --no-build-isolation

# Installing model for GPU
ml-model-gpu: ml-util-mamba ml-lib-cuda
	MAMBA_KEEP_CUDA_BUILD=TRUE ${PIP} install mamba-ssm --no-build-isolation

# Installing ml package for ML on CUDA
ml-lib-cuda: venv ml-model-gpu
	${PIP} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/${CUDA}   

# Running train model
ml-train: 
	${CLI} ${PATH_TRAIN}

# Running predict model
ml-predict:
	${CLI} ${PATH_PREDICT}

# Running evaluate model
ml-evaluate:
	${CLI} ${PATH_EVALUATE}

# Running script for updating datetime in dataset
update-time:
	${CLI} ml/scripts/update_time.py