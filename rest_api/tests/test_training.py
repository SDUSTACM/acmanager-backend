from collections import OrderedDict

from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from django.urls import reverse

from rest_api.models.Training import Training

from .utils import get_login_client

User = get_user_model()

def create_training(client, training_data):
    url = reverse("training-view-list")
    response = client.post(url, training_data, content_type="application/json")
    return response

class TrainingAddTestCase(TestCase):
    def setUp(self):
        self.client = get_login_client({
            "username": "test",
            "password": "test",
        })

    def test_add_training(self):
        training_data = {"name": "training", "description": "training description"}
        response = create_training(client=self.client, training_data=training_data)
        user = response.wsgi_request.user
        self.assertTrue(Training.objects
                        .filter(create_user=user, **training_data)
                        .exists(), response.data)


class TrainingListTestCase(TestCase):
    def setUp(self):
        self.client = get_login_client({
            "username": "test",
            "password": "test",
        })
        self.trainings_data = [
            {"name": "training", "description": "training_description"},
            {"name": "training1", "description": "training_description1"},
        ]
        for training_data in self.trainings_data:
            create_training(self.client, training_data)


    def test_list_training(self):
        url = reverse("training-view-list")
        response = self.client.get(url, content_type="application/json")
        gen0 = list(map(lambda x: OrderedDict({"name" :x["name"], "description": x["description"]}), response.data))
        gen1 = [OrderedDict(training_data) for training_data in self.trainings_data]
        # print("-------------")
        # print(gen0)
        # print(gen1)
        # print("-------------")
        self.assertEqual(gen0, gen1)


class TrainingUpdateTestCase(TestCase):
    def setUp(self):
        self.client = get_login_client({
            "username": "test",
            "password": "test",
        })
        self.trainings_data = [
            {"name": "training", "description": "training_description"},
            # {"name": "training1", "description": "training_description1"},
        ]
        for training_data in self.trainings_data:
            create_training(self.client, training_data)

    def test_update_name_training(self):
        url = reverse("training-view-detail", args=[1])
        response = self.client.patch(url, {"name": "updated"}, content_type="application/json")
        url = reverse("training-view-detail", args=[1])
        response = self.client.get(url, content_type="application/json")
        print(response.data)
        gen0 = OrderedDict({"name" : response.data["name"], "description": response.data["description"]})
        gen1 = OrderedDict({**self.trainings_data[0], "name": "updated"})
        print(gen0)
        print(gen1)
        self.assertEqual(gen0, gen1)

    def test_update_description_training(self):
        url = reverse("training-view-detail", args=[1])
        response = self.client.patch(url, {"description": "updated"}, content_type="application/json")
        url = reverse("training-view-detail", args=[1])
        response = self.client.get(url, content_type="application/json")
        print(response.data)
        gen0 = OrderedDict({"name" : response.data["name"], "description": response.data["description"]})
        gen1 = OrderedDict({**self.trainings_data[0], "description": "updated"})
        self.assertEqual(gen0, gen1)


class StageTestCase(TestCase):
    def setUp(self):
        self.client = get_login_client({
            "username": "test",
            "password": "test",
        })
        self.trainings_data = [
            {"name": "training", "description": "training_description"},
            # {"name": "training1", "description": "training_description1"},
        ]
        for training_data in self.trainings_data:
            create_training(self.client, training_data)

    def create_stage(self, data):
        response = self.client.post(reverse("stage-view-list"), data, content_type="application/json")
        self.assertEqual(response.status_code, 201, response.data)

    def retrieve_stage_by_training_id(self, training_id):
        response = self.client.get(reverse("stage-view-detail", args=[training_id]))
        self.assertEqual(response.status_code, 200, response.data)

    def test_training_stage_create(self):
        data = {
            "name": "stage_name",
            "description": "stage_description",
            "training_id": 1,
        }
        self.create_stage(data)


    def test_training_stage_list(self):
        pass

    def test_training_stage_update(self):
        url = reverse("training-view-detail", args=[1])
        response = self.client.patch(url, {"description": "updated"}, content_type="application/json")
        url = reverse("training-view-detail", args=[1])
        response = self.client.get(url, content_type="application/json")
        print(response.data)
        gen0 = OrderedDict({"name" : response.data["name"], "description": response.data["description"]})
        gen1 = OrderedDict({**self.trainings_data[0], "description": "updated"})
        self.assertEqual(gen0, gen1)