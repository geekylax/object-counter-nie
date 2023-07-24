# Machine Learning & Hexagonal Architecture

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system 

The model used in this example has been taken from 
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)

## Project organisation 


ª   .env                                        
ª   assesment.md                                
ª   docker-compose.yml                          
ª   dvc.yaml                                   
ª   makefile                                    
ª   params.yaml                                
ª   README.md                                  
ª   requirements.txt                           
ª   requirements_train.txt
ª   test.txt
ª   tox.ini
ª   train_params.yaml
+---counter
ª   ª   config.py
ª   ª   debug.py
ª   ª   loggers.py
ª   ª   __init__.py
ª   ª   
ª   +---adapters
ª   ª   ª   count_repo.py
ª   ª   ª   mscoco_label_map.json
ª   ª   ª   object_detector.py
ª   ª   ª   __init__.py
ª   ª   ª   
ª   ª           
ª   +---domain
ª   ª   ª   actions.py
ª   ª   ª   models.py
ª   ª   ª   ports.py
ª   ª   ª   predictions.py
ª   ª   ª   __init__.py
ª   +---entrypoints
ª   ª   ª   main.py
ª   ª   ª   webapp.py
ª   ª   ª   __init__.py
ª   ª           
ª   +---resources
ª   ª       arial.ttf
ª   ª       
+---db
ª       db.sql
ª       
+---images
ª       image_20230723_215344_3389_0.9.jpg
ª       image_20230723_222023_2641_0.9.jpg
ª       image_20230723_222042_8025_0.9.jpg
ª       
+---log
ª       2023-07-23.log
ª       
+---reports
+---resources
ª   +---images
ª           boy.jpg
ª           cat.jpg
ª           food.jpg
ª           test.jpg
ª           
+---tests
ª   ª   __init__.py
ª   ª   
ª   +---domain
ª   ª   ª   api_test.py
ª   ª   ª   helpers.py
ª   ª   ª   test_actions.py
ª   ª   ª   test_predictions.py
ª   ª   ª   __init__.py
+---tmp
ª   +---debug
ª   ª       all_predictions.jpg
ª   ª       valid_predictions_with_threshold_0.5.jpg
ª   ª       valid_predictions_with_threshold_0.9.jpg
ª   ª       
ª   +---model
ª       +---1
ª               saved_model.pb
ª               
+---yolo_train
        predict.py
        train.py
        utils.py
        


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

