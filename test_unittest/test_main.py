import unittest
from unittest.mock import MagicMock

from app.main import app
from app.models import Contact
from app.schemas import ContactCreate


class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_main_function_1(self):
        # Напишіть тест для вашої функції your_main_function_1
        # Приклад:
        response = self.app.get('/your_endpoint')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expected Response Content', response.data)

    def test_main_function_2(self):
        # Напишіть тест для вашої функції your_main_function_2
        # Приклад:
        response = self.app.post('/another_endpoint', json={'key': 'value'})
        self.assertEqual(response.status_code, 201)


class TestCRUD(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()

    def test_create_contact(self):
        contact_data = ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            birth_date="1990-01-01",
            additional_data="Some data"
        )

        response = self.app.post('/contacts/', json=contact_data.dict())
        self.assertEqual(response.status_code, 201)
        created_contact = Contact(**response.json())

        self.db.add.assert_called_once_with(created_contact)
        self.db.commit.assert_called_once()

    def test_get_contacts(self):
        contacts = [Contact(first_name="John"), Contact(first_name="Jane")]
        self.db.query(Contact).all.return_value = contacts

        response = self.app.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        returned_contacts = response.json()

        self.assertEqual(len(returned_contacts), len(contacts))
        self.assertEqual(
            returned_contacts[0]['first_name'], contacts[0].first_name)
        self.assertEqual(
            returned_contacts[1]['first_name'], contacts[1].first_name)


if __name__ == '__main__':
    unittest.main()
