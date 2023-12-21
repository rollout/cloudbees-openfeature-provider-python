from typing import List, Optional, Union
from openfeature.api import EvaluationContext

from openfeature.flag_evaluation import FlagResolutionDetails
from openfeature.api import Hook
from openfeature.provider.metadata import Metadata
from openfeature.provider.provider import AbstractProvider
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions

# example of a naive Logger
class MyLogger:
    def error(self, msg, ex=None):
        print('error: %s exception: %s' %(msg, ex))

    def warn(self, msg, ex=None):
        print('warn: %s' % msg)

    def debug(self, msg, ex=None):
        print('debug: %s' % msg)

class CloudbeesProvider(AbstractProvider):
    def __init__(self, api_key=""):
        print('setup')
        if api_key == "":
            raise Exception("Must provide apiKey")
        
        options = RoxOptions(
            logger=MyLogger()
        )
        Rox.setup(api_key, options).result()

    def get_metadata(self) -> Metadata:
        return Metadata("Cloudbees")

    def get_provider_hooks(self) -> List[Hook]:
        return []
    
    def shutdown(self):
        Rox.shutdown()

    def resolve_boolean_details(
        self,
        flag_key: str,
        default_value: bool,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[bool]:
        return FlagResolutionDetails(
            value=Rox.dynamic_api().is_enabled(flag_key, default_value, self._convert_context(evaluation_context))
        )

    def resolve_string_details(
        self,
        flag_key: str,
        default_value: str,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[str]:
        return FlagResolutionDetails(
            value=Rox.dynamic_api().value(flag_key, default_value, [default_value], self._convert_context(evaluation_context))
        )

    def resolve_integer_details(
        self,
        flag_key: str,
        default_value: int,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[int]:
        return FlagResolutionDetails(
            value=Rox.dynamic_api().get_int(flag_key, default_value, [default_value], self._convert_context(evaluation_context))
        )

    def resolve_float_details(
        self,
        flag_key: str,
        default_value: float,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[float]:
        return FlagResolutionDetails(
            value=Rox.dynamic_api().get_double(flag_key, default_value, [default_value], self._convert_context(evaluation_context))
        )

    def resolve_object_details(
        self,
        flag_key: str,
        default_value: Union[dict, list],
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[Union[dict, list]]:
        raise Exception("Not implemented")
    
    def initialize(self, evaluation_context: EvaluationContext):
        Rox.set_context(self._convert_context(evaluation_context))

    @staticmethod
    def _convert_context(evaluation_context: EvaluationContext):
         return None if not evaluation_context else evaluation_context.attributes
