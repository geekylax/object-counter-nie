Added and rearranged the folder structure for better maintenence .
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
        



1. Add a new service endpoint to receive the image and the desired threshold and return
the list of predictions.

    Added a new endpoint in webapp.py for listing the predictions with object-list endpoint with base ur 


2. Write a new adapter for ObjectCountRepo to persist data using a relational (MySQL or
PostgreSQL) database.

    I have used postgresql for storing the data for the class ObjectCountRepo and i used docker file for initialising a posgtresql database 


3. Review the rest of the source code and propose some improvements that you would
make in the code, the setup instructions, the tests,...

    1. added .env file for prod and dev environment change also the credentials of postresql is mentioned in the env file
    2. added test cases for the new function object-list 
    3. added a db/db.sql
    4. webapp is maintained with better error response 
    5. saved the files which is being processed by the model with txt and the images for feedback loop training.


4. Implement at least one of the proposed improvements.
    1. added param.yaml file to predefine the setting or model name there so that i will be easy to configure in the future scope asa well as reproductibality for differnt setting is easy as well
    2. added a new test case to check the image file is large then return error response
    3. added a condition to validate in the endpoint itself.
    4. added tox to check pytest also to lint the code for better code management as well as to review before deployment.


5. If we want to use multiple models trained internally (not public), what would you change
in the setup of the project?
    1. I have used a yolo 8 model for trianning i have created a dv pipeline for data versioning and adding piprline for training 
    since the data coming from the infernce is saved with the txt and the class name .
    2. we can validate the values with some certain threshold and use it for feedback loop trainig.
    3. added training code and prediction code with diffenrt yaml file and requiremnts_train.txt file 

6. Choose one of the following
a. Improve the testing by adding integration and e2e tests (or any other
improvements you consider necessary)
    1. added a full end to end api testing with diffenret error codes and for model we do have testing with mock test.
    2. added logging mecahnisim for the better approach of debugging.


b. Support models for object detection using different deep learning frameworks. If
the task seems too big, just lay out the main key points of the proposed solution.
    To support differnt model for object detction using different DL frameworks we can use grpc protocol for inferncing images it can be in pnnx or pth model we can have the sturcture only to infer and show the ouput irrespective of the model to be changed it can be mentioedn in the param.yaml 
    so that it would reflect automatcially.

