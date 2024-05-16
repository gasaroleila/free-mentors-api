"""
 tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_email = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Creating a user without email raises an exception"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_request(self):
        """Test Creating a request"""

        mentor = get_user_model().objects.create_user(
            email="uwamgaleila@example.com",
            password="P@ss12345",
            first_name="Gasaro",
            last_name="Leila",
            is_mentor=True
        )

        mentee = get_user_model().objects.create_user(
            email="leila@example.com",
            password="password",
            first_name="Leila",
            last_name="1",
            is_mentor=False
        )

        request = models.Request.objects.create(
            mentor=mentor,
            mentee=mentee,
            question="How to integrate Graphql in Django"
        )

        self.assertEqual(str(request), request.question)
