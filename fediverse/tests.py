import json

from django.test import TestCase, Client
from django.urls import reverse

from fediverse.models import User

# Create your tests here.
class APResponseTests(TestCase):
    def test_response_person(self):
        testingUser = User.objects.create_user("testUser")
        res = self.client.get(reverse('UserShow', kwargs={'username': testingUser.username}), HTTP_ACCEPT="application/activity+json")
        resDict = json.loads(res.content.decode('utf-8'))
        self.assertEqual(type(resDict), dict, "Should response is json(ActivityPub)")
        self.assertEqual(type(resDict.get('@context')), list, "Should @context is list")
        self.assertEqual(resDict.get('type'), "Person", "Should user is not bot(Should return Person)")
        self.assertEqual(resDict.get('preferredUsername'), "testUser", "preferredUsername is username")
        self.assertEqual(type(resDict.get('publicKey')), dict, "Should publicKey is dict")
