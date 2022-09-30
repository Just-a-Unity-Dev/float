from classes.schema import Schema
from random import randint
import unittest

class SchemaTests(unittest.TestCase):
    def test_create_schema(self):
        schema = Schema()
        self.assertIsInstance(schema, Schema)

class FieldTests(unittest.TestCase):
    def test_create_field_single(self):
        schema = Schema()
        schema.add_field("test_field_1", "default_value")
        self.assertEqual(schema.get_field("test_field_1"), "default_value")
        
    def test_create_field_multi(self):
        schema = Schema()
        schema.add_field("test_field_1", "default_value")
        schema.add_field("test_field_2", "default_value2")
        schema.add_field("test_field_3", "default_value3")
        self.assertEqual(schema.get_field("test_field_1"), "default_value")
        self.assertEqual(schema.get_field("test_field_2"), "default_value2")
        self.assertEqual(schema.get_field("test_field_3"), "default_value3")
    
class DocumentTests(unittest.TestCase):
    def test_document_change_single(self):
        schema = Schema()
        schema.add_document()
        schema.add_field("test_field_1", "default_value")
        self.assertEqual(schema.documents[0]["test_field_1"], "default_value")
    
    def test_document_change_multi(self):
        schema = Schema()

        schema.add_document()
        schema.add_field("test_field_1", "default_value")
        self.assertEqual(schema.documents[0]["test_field_1"], "default_value")

        schema.add_field("test_field_2", "default_value2")
        schema.add_document()
        self.assertEqual(schema.documents[0]["test_field_2"], "default_value2")

        schema.add_document()
        schema.add_field("test_field_3", "default_value3")
        self.assertEqual(schema.documents[0]["test_field_3"], "default_value3")
    
    def test_document_id_getset(self):
        schema = Schema()

        for x in range(10):
            schema.add_document()
        schema.add_field("test_field_1", "default_value")
        schema.set_document_field(3, "test_field_1", "not_default_value")
        self.assertEqual(schema.get_document_field(3, "test_field_1"), "not_default_value")
        

if __name__ == '__main__':
    unittest.main()