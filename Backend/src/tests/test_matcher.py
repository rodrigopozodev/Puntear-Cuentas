import unittest
from utils.matcher import complete_matching, debe_matching, haber_matching

class TestMatcher(unittest.TestCase):

    def setUp(self):
        self.debe_data = [
            {"fecha": "10/16/2024", "monto": 2665.29, "descripcion": "Creación Anticipo 409099909/1"},
            {"fecha": "10/24/2024", "monto": 2665.29, "descripcion": "Compensación Anticipo 409099909/1"}
        ]
        self.haber_data = [
            {"fecha": "10/16/2024", "monto": 2665.29, "descripcion": "Creación Anticipo 409099909/1"},
            {"fecha": "10/24/2024", "monto": 2615.42, "descripcion": "Compensación Anticipo 409099909/1"}
        ]

    def test_complete_matching(self):
        result = complete_matching(self.debe_data, self.haber_data)
        self.assertTrue(result)

    def test_debe_matching(self):
        debe_data = [
            {"fecha": "10/16/2024", "monto": 1000.00, "descripcion": "Transacción A"},
            {"fecha": "10/16/2024", "monto": 1665.29, "descripcion": "Transacción B"}
        ]
        result = debe_matching(debe_data, self.haber_data)
        self.assertEqual(result, [{"fecha": "10/16/2024", "monto": 2665.29, "descripcion": "Transacción A + B"}])

    def test_haber_matching(self):
        haber_data = [
            {"fecha": "10/24/2024", "monto": 2615.42, "descripcion": "Transacción C"},
            {"fecha": "10/24/2024", "monto": 49.87, "descripcion": "Transacción D"}
        ]
        result = haber_matching(self.debe_data, haber_data)
        self.assertEqual(result, [{"fecha": "10/24/2024", "monto": 2665.29, "descripcion": "Transacción C + D"}])

if __name__ == '__main__':
    unittest.main()