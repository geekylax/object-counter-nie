from PIL import Image

from counter.debug import draw
from counter.domain.models import CountResponse
from counter.domain.ports import ObjectDetector, ObjectCountRepo
from counter.domain.predictions import over_threshold, count
from counter.domain.models import ListResponse,FoundObject
import random 
import os 
import datetime
import yaml 

def config(config_path="params.yaml"):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

class CountDetectedObjects:
    def __init__(self, object_detector: ObjectDetector, object_count_repo: ObjectCountRepo):
        self.__object_detector = object_detector
        self.__object_count_repo = object_count_repo

    def execute(self, image, threshold) -> CountResponse:
        predictions = self.__find_valid_predictions(image, threshold)
        object_counts = count(predictions)
        self.__object_count_repo.update_values(object_counts)
        total_objects = self.__object_count_repo.read_values()
        return CountResponse(current_objects=object_counts, total_objects=total_objects)

    def __find_valid_predictions(self, image, threshold):
        predictions = self.__object_detector.predict(image)
        if image is not None:
            image = Image.open(image)
            self.__save_images_for_trainig(image,threshold)
        self.__debug_image(image, predictions, "all_predictions.jpg")
        valid_predictions = list(over_threshold(predictions, threshold=threshold))
        self.__debug_image(image, valid_predictions, f"valid_predictions_with_threshold_{threshold}.jpg")
        return valid_predictions

    @staticmethod
    def __debug_image(image, predictions, image_name):
        if __debug__ and image is not None:

            draw(predictions, image, image_name)

    @staticmethod
    def __save_images_for_trainig(image,threshold):
            random_number = random.randint(1000, 9999)
            # Get the current date and time
            current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            # Create a new filename with random number and timestamp
            new_filename = f"image_{current_time}_{random_number}_{threshold}.jpg"
            # Save the image to a designated directory
            configuration = config()
            folder_name  = configuration["images_folder"]
            image_path = os.path.join(folder_name, new_filename)
            try:
                os.mkdir(folder_name)
            except OSError:
                pass
            image.save(image_path)

class ListDetectedObjects:
    def __init__(self, object_detector: ObjectDetector):
        self.__object_detector = object_detector

    def execute(self, image, threshold) -> ListResponse:
        predictions = self.__find_valid_predictions(image, threshold)
        found_objects = [FoundObject(p.class_name, p.box) for p in predictions]
        return ListResponse(found_objects=found_objects)

    def __find_valid_predictions(self, image, threshold):
        predictions = self.__object_detector.predict(image)
        if image is not None:
            image = Image.open(image)
            self.__save_images_for_trainig(image,threshold)

        self.__debug_image(image, predictions, "all_predictions.jpg")
        valid_predictions = list(over_threshold(predictions, threshold=threshold))
        self.__debug_image(image, valid_predictions, f"valid_predictions_with_threshold_{threshold}.jpg")
        return valid_predictions

    @staticmethod
    def __debug_image(image, predictions, image_name):

        if __debug__ and image is not None:
            draw(predictions, image, image_name)

    @staticmethod
    def __save_images_for_trainig(image,threshold):
            random_number = random.randint(1000, 9999)
            # Get the current date and time
            current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            # Create a new filename with random number and timestamp
            new_filename = f"image_{current_time}_{random_number}_{threshold}.jpg"
            # Save the image to a designated directory
            configuration = config()

            folder_name  = configuration["images_folder"]

            image_path = os.path.join(folder_name, new_filename)
            try:
                os.mkdir(folder_name)
            except OSError:
                pass
            image.save(image_path)

