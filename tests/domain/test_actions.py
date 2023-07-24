from unittest.mock import Mock

import pytest

from counter.domain.actions import CountDetectedObjects
from counter.domain.models import ObjectCount,FoundObject, Box
from tests.domain.helpers import generate_prediction
from counter.domain.actions import ListDetectedObjects

class TestCountDetectedObjects:
    @pytest.fixture
    def object_detector(self) -> Mock:
        object_detector = Mock()
        object_detector.predict.return_value = [generate_prediction('cat', 0.9),
                                                generate_prediction('cat', 0.8),
                                                generate_prediction('dog', 0.8),
                                                generate_prediction('dog', 0.1),
                                                generate_prediction('rabbit', 0.9)]
        return object_detector

    @pytest.fixture
    def count_object_repo(self) -> Mock:
        return Mock()

    def test_count_valid_predictions(self, object_detector, count_object_repo) -> None:
        response = CountDetectedObjects(object_detector, count_object_repo).execute(None, 0.5)
        assert sorted(response.current_objects, key=lambda x: x.object_class) == \
            [ObjectCount('cat', 2), ObjectCount('dog', 1), ObjectCount('rabbit', 1)]

    def test_update_count_object_repo(self, object_detector, count_object_repo):
        CountDetectedObjects(object_detector, count_object_repo).execute(None, 0)
        count_object_repo.update_values.assert_called_with(
            [ObjectCount('cat', 2), ObjectCount('dog', 2), ObjectCount('rabbit', 1)])

class TestListObjects:
    @pytest.fixture
    def object_detector(self) -> Mock:
        object_detector = Mock()
        object_detector.predict.return_value = [generate_prediction('bowl', 0.9),
                                                generate_prediction('cup', 0.9),
                                                generate_prediction('dining table', 0.1)]
        return object_detector

    def test_list_valid_predictions(self, object_detector) -> None:
        response = ListDetectedObjects(object_detector).execute(None, 0.5)

        assert sorted(response.found_objects, key=lambda x: x.object_class) == \
               [FoundObject('bowl', Box(0, 0, 0, 0)), FoundObject('cup', Box(0, 0, 0, 0))]