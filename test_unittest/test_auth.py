import unittest
from app.main import app
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth import create_access_token


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_register_user(self):
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        response = self.app.post('/register/', json=user_data.dict())
        self.assertEqual(response.status_code, 201)

        created_user = User(**response.json())
        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, user_data.username)
        self.assertEqual(created_user.email, user_data.email)

        # Додайте перевірку збереження користувача в базу даних

    def test_login_user(self):
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        login_data = UserLogin(
            email="test@example.com",
            password="testpassword"
        )

        response = self.app.post('/register/', json=user_data.dict())
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/login/', json=login_data.dict())
        self.assertEqual(response.status_code, 200)
        access_token = response.json()['access_token']

        # Додайте перевірку, що отриманий access_token є дійсним

    def test_access_protected_route(self):
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        response = self.app.post('/register/', json=user_data.dict())
        self.assertEqual(response.status_code, 201)

        access_token = create_access_token(data={"sub": user_data.email})

        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.app.get('/protected/', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Granted', response.data)


if __name__ == '__main__':
    unittest.main()
