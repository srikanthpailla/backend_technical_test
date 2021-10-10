import unittest
import tempfile

from app.main import app, db

class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()

    def test_1_add_product(self):
        with app.test_client() as mocked_app:
            json_data = {'name': 'prod1', 'price': 100.00}
            actual_result = mocked_app.post('/v1/product', json=json_data)
            actual_result = actual_result.get_json()
            actual_result.pop('id')
            self.assertDictEqual(actual_result, json_data)

    def test_2_get_product(self):
        with app.test_client() as mocked_app:
            actual_result = mocked_app.get('/v1/product/1')
            actual_result = actual_result.get_json()
            expected_data = {'name': 'prod1', 'price': 100.00, 'id': 1}
            self.assertDictEqual(actual_result, expected_data)

    def test_2_get_all_products(self):
        with app.test_client() as mocked_app:
            json_data = {'name': 'prod4', 'price': 300.00}
            mocked_app.post('/v1/product', json=json_data)
            actual_result = mocked_app.get('/v1/products')
            actual_result = actual_result.get_json()
            expected_data = [
                {'id': 1, 'name': 'prod1', 'price': 100.0},
                {'id': 2, 'name': 'prod4', 'price': 300.0}
            ]
            self.assertListEqual(actual_result, expected_data)

    def test_3_update_product(self):
        with app.test_client() as mocked_app:
            actual_result = mocked_app.put('/v1/product/1', json={'name': 'prod2'})
            actual_result = actual_result.get_json()
            expected_data = {'name': 'prod2', 'price': 100.00, 'id': 1}
            self.assertDictEqual(actual_result, expected_data)

    def test_4_delete_product(self):
        with app.test_client() as mocked_app:
            actual_result = mocked_app.delete('/v1/product/1')
            self.assertEqual(actual_result.data, b'Product 1 deleted successfully.')

    def test_5_get_product_exception(self):
        with app.test_client() as mocked_app:
            actual_result = mocked_app.get('/v1/product/1')
            self.assertEqual(actual_result.status_code, 404)

    def test_6_update_product_exception(self):
        with app.test_client() as mocked_app:
            actual_result = mocked_app.put('/v1/product/1')
            self.assertEqual(actual_result.status_code, 404)

    def test_7_delete_product_exception(self):
        with app.test_client() as mocked_app:
            actual_result = mocked_app.delete('/v1/product/1')
            self.assertEqual(actual_result.status_code, 404)
