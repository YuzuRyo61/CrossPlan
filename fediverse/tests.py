import json

from django.test import TestCase, Client
from django.urls import reverse

from fediverse.models import User

# Create your tests here.
class APResponseTests(TestCase):
    def test_response_person(self):
        testingUser = User.objects.create_user("testUser")
        res = self.client.get(reverse('UserShow', kwargs={'username': testingUser.username}), HTTP_ACCEPT="application/activity+json")
        self.assertEqual(type(json.loads(res.content.decode('utf-8'))), dict, "Should response is json(ActivityPub)")
        
