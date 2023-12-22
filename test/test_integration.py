from openfeature import api
from openfeature.exception import ErrorCode
from openfeature.flag_evaluation import Reason
from openfeature.api import EvaluationContext
from cloudbees.provider import CloudbeesProvider
import unittest
from rox.server.rox_options import RoxOptions

# example of a naive Logger
class MyLogger:
    def error(self, msg, ex=None):
        print('error: %s exception: %s' %(msg, ex))

    def warn(self, msg, ex=None):
        print('warn: %s' % msg)

    def debug(self, msg, ex=None):
        print('debug: %s' % msg)

class IntegrationTests(unittest.TestCase):
    provider: CloudbeesProvider

    @classmethod
    def setUpClass(self):
        provider = CloudbeesProvider("62bee5bbca1059d18808adad", RoxOptions(logger=MyLogger()))
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

    def test_string_targeting_off(self):
        # targeting off
        self.assertEqual(self.client.get_string_value("string-disabled", "banana"), "banana")

    def test_string_targeting_on(self):
        # targeting on
        self.assertEqual(self.client.get_string_value("string-static-yes", "default"), "yes")
        self.assertEqual(self.client.get_string_value("string-static-no", "default"), "no")

        # different contextes
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={"stringproperty": "on"})), "yes")
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={"stringproperty": "off"})), "no")
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={"not_defined": "whatever"})), "not specified")
        self.assertEqual(self.client.get_string_value("string-with-context", "default", EvaluationContext(attributes={})), "not specified")
        self.assertEqual(self.client.get_string_value("string-with-context", "default"), "not specified")
    
    def test_integer_flag(self):
        # targeting on
        self.assertEqual(self.client.get_integer_value("integer-static-5", 2), 5)

        # targeting off
        self.assertEqual(self.client.get_integer_value("integer-disabled", 7), 7)

        # different contextes
        self.assertEqual(self.client.get_integer_value("integer-with-context", -1, EvaluationContext(attributes={"stringproperty": "1"})), 1)
        self.assertEqual(self.client.get_integer_value("integer-with-context", -1, EvaluationContext(attributes={"stringproperty": "5"})), 5)
        self.assertEqual(self.client.get_integer_value("integer-with-context", -1, EvaluationContext(attributes={"not_defined": "whatever"})), 10)
        self.assertEqual(self.client.get_integer_value("integer-with-context", -1, EvaluationContext(attributes={})), 10)
        self.assertEqual(self.client.get_integer_value("integer-with-context", -1), 10)
    
    def test_float_flag(self):
        # targeting on
        self.assertEqual(self.client.get_float_value("integer-static-5", 2.2), 5.0)

        # targeting off
        self.assertEqual(self.client.get_float_value("integer-disabled", 7.0), 7.0)

        # different contextes
        self.assertEqual(self.client.get_float_value("integer-with-context", -1.0, EvaluationContext(attributes={"stringproperty": "1"})), 1.0)
        self.assertEqual(self.client.get_float_value("integer-with-context", -1.0, EvaluationContext(attributes={"stringproperty": "5"})), 5.0)
        self.assertEqual(self.client.get_float_value("integer-with-context", -1.0, EvaluationContext(attributes={"not_defined": "whatever"})), 10.0)
        self.assertEqual(self.client.get_float_value("integer-with-context", -1.0, EvaluationContext(attributes={})), 10.0)
        self.assertEqual(self.client.get_float_value("integer-with-context", -1.0), 10.0)
    
    def test_object_flag(self):
        default_value = {'a': 'b'}
        result = self.client.get_object_details('not-supported', default_value)
        self.assertEqual(result.reason, Reason.ERROR)
        self.assertEqual(result.value, default_value)
        self.assertEqual(result.error_code, ErrorCode.GENERAL)
        self.assertEqual(result.error_message, 'Not implemented')

    def test_differently_typed_context_values(self):
        # matching targeting to property
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": "one"})), 1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"numberproperty": 1})), 1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"numberproperty": 1.0})), 1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"booleanproperty": True})), 1)

        # unmatching targeting to property
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"stringproperty": "no"})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"numberproperty": 0})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"numberproperty": 0.0})), -1)
        self.assertEqual(self.client.get_integer_value('integer-with-complex-context', -1, EvaluationContext(attributes={"booleanproperty": False})), -1)

        # can implement and add tests for non supported context type, Rollout support any context when via computed custom property
        # this is not currently wrapped in open feature, hence only default custom property to context key matching can be currently used (string => string/boo/int/double)

if __name__ == '__main__':
    unittest.main()
