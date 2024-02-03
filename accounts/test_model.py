import pytest
from .models import User, UserProfile,GenderChoices

@pytest.mark.django_db
def test_create_user():
    # Create a sample user
    user = User.objects.create_user(email="test@example.com", password="password")

    # Check if the user was created successfully
    assert user.id is not None
    assert user.slug == "test-example-com"

@pytest.mark.django_db
def test_create_superuser():
    # Create a superuser
    superuser = User.objects.create_superuser(email="admin@example.com", password="admin")

    # Check if the superuser was created successfully
    assert superuser.is_superuser is True

@pytest.mark.django_db
def test_create_user_profile():
    # Create a user
    user = User.objects.create_user(email="user@example.com", password="user")

    # Create a user profile
    profile = UserProfile.objects.create(user=user, gender=GenderChoices.male)

    # Check if the profile was created successfully
    assert profile.id is not None
    assert profile.gender == GenderChoices.male
