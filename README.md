# Machine Learning & Hexagonal Architecture

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system 

The model used in this example has been taken from 
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)

## Project organisation 
.env
.gitattributes
.gitignore
README.md
assesment.md
counter
   |-- __init__.py
   |-- adapters
   |   |-- __init__.py
   |   |-- count_repo.py
   |   |-- mscoco_label_map.json
   |   |-- object_detector.py
   |-- config.py
   |-- debug.py
   |-- domain
   |   |-- __init__.py
   |   |-- actions.py
   |   |-- models.py
   |   |-- ports.py
   |   |-- predictions.py
   |-- entrypoints
   |   |-- __init__.py
   |   |-- main.py
   |   |-- webapp.py
   |-- loggers.py
   |-- resources
   |   |-- arial.ttf
db
   |-- db.sql
docker-compose.yml
dvc.yaml
images
   |-- image_20230723_215344_3389_0.9.jpg
   |-- image_20230723_222023_2641_0.9.jpg
   |-- image_20230723_222042_8025_0.9.jpg
log
   |-- 2023-07-23.log
makefile
params.yaml
requirements.txt
requirements_train.txt
resources
   |-- images
   |   |-- boy.jpg
   |   |-- cat.jpg
   |   |-- food.jpg
   |   |-- test.jpg
test.txt
tests
   |-- __init__.py
   |-- domain
   |   |-- __init__.py
   |   |-- api_test.py
   |   |-- helpers.py
   |   |-- test_actions.py
   |   |-- test_predictions.py
tmp
   |-- .gitignore
tox.ini
train_params.yaml
yolo_train
   |-- predict.py
   |-- train.py
   |-- utils.py


## Download the model
```
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
mkdir -p tmp/model/1
mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/1
rm -rf tmp/rfcn_resnet101_coco_2018_01_28
```


## Setup and run Tensorflow Serving

```
model_name=rfcn
cores_per_socket=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs`
num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs`
num_physical_cores=$((cores_per_socket * num_sockets))
echo $num_physical_cores

docker rm -f tfserving

docker run \
    --name=tfserving \
    -d \
    -p 8500:8500 \
    -p 8501:8501 \
    -v "$(pwd)/tmp/model:/models/$model_name" \
    -e MODEL_NAME=$model_name \
    -e OMP_NUM_THREADS=$num_physical_cores \
    -e TENSORFLOW_INTER_OP_PARALLELISM=2 \
    -e TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores \
    intel/intel-optimized-tensorflow-serving:2.3.0
    
```


## Run mongo 

```bash
docker rm -f test-mongo
docker run --name test-mongo --rm --net host -d mongo:latest
```


## Setup virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### for running the makefile 
```if you have installed make then use the makefile to setup 

make 

```

## Run the application

### Using fakes
```
python -m counter.entrypoints.webapp
```

### running the app in prod env with infernce the model in realtime

```
ENV=prod python -m counter.entrypoints.webapp
```

## Call the service

```shell script
 curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://0.0.0.0:5000/object-count

 curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://0.0.0.0:5000/object-list

```

## Run the tests

``` use tox to run the text and check the lint 
pytest

tox 

```

