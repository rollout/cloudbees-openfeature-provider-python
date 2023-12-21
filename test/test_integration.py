from openfeature import api
from openfeature.api import EvaluationContext
from cloudbees.provider import CloudbeesProvider
import unittest

class IntegrationTests(unittest.TestCase):
    provider: CloudbeesProvider

    @classmethod
    def setUpClass(self):
        provider = CloudbeesProvider("62bee5bbca1059d18808adad")
        api.set_provider(provider)
        self.client = api.get_client()

    @classmethod
    def tearDownClass(self) -> None:
        api.shutdown()
    
    def test_no_api_key(self):
        with self.assertRaises(Exception):
            CloudbeesProvider("")

    def test_bool_targeting_off(self):
        self.assertFalse(self.client.get_boolean_value("boolean-disabled", False))
        self.assertTrue(self.client.get_boolean_value("boolean-disabled", True))

    def test_bool_targeting_on(self):
        self.assertTrue(self.client.get_boolean_value("boolean-static-true", False))
        self.assertFalse(self.client.get_boolean_value("boolean-static-false", True))

    def test_bool_targeting_with_context(self):
        self.assertTrue(self.client.get_boolean_value("boolean-with-context", False, EvaluationContext(attributes={"stringproperty": "on"})))
        self.assertFalse(self.client.get_boolean_value("boolean-with-context", False, EvaluationContext(attributes={"stringproperty": 'off'})))

    def test_string_with_targeting(self):
        # targeting on
        self.assertEqual(self.client.get_string_value("string-static-yes", "default"), "yes")
        self.assertEqual(self.client.get_string_value("string-static-no", "default"), "no")

        # targeting off
        self.assertEqual(self.client.get_string_value("string-disabled", "banana"), "banana")

        # different contextes
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={"stringproperty": "on"})), "yes")
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={"stringproperty": "off"})), "no")
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={"not_defined": "whatever"})), "not specified")
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={})), "not specified")
        self.assertEqual(self.client.get_string_value("string-with-context", "default"), "not specified")
    
    #   it('with targeting off', async () => {
    #     await expect(client.getStringValue('string-disabled', 'banana')).resolves.toBe('banana')
    #   })

    #   it('using a context', async () => {
    #     await expect(client.getStringValue('string-with-context', 'default', {stringproperty: 'on'})).resolves.toBe('yes')
    #     await expect(client.getStringValue('string-with-context', 'default', {stringproperty: 'off'})).resolves.toBe('no')
    #     await expect(client.getStringValue('string-with-context', 'default', {not_defined: 'whatever'})).resolves.toBe('not specified')
    #     await expect(client.getStringValue('string-with-context', 'default', {})).resolves.toBe('not specified')
    #     await expect(client.getStringValue('string-with-context', 'default')).resolves.toBe('not specified')
    #   })
    
    def test_number_different_context_types(self):
        # matching targeting to property
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": "one"})), 1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"numberproperty": 1})), 1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"booleanproperty": True})), 1)

        # unmatching targeting to property
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": "no"})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"numberproperty": 0})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"booleanproperty": False})), -1)

        # wrong property type
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"badproperty": "whatever"})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": []})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": {}})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": 1})), -1)

    #     // Unexpected/unsupported contexts
    #     await expect(client.getNumberValue('integer-with-complex-context', -1, {badproperty: 'whatever'})).resolves.toBe(-1)
    #     await expect(client.getNumberValue('integer-with-complex-context', -1, {stringproperty: []})).resolves.toBe(-1)
    #     await expect(client.getNumberValue('integer-with-complex-context', -1, {stringproperty: {}})).resolves.toBe(-1)
    #     await expect(client.getNumberValue('integer-with-complex-context', -1, {stringproperty: 1})).resolves.toBe(-1)
    #   })
    # })
if __name__ == '__main__':
    unittest.main()