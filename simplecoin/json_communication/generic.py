from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .request_type import RequestType

@dataclass_json
@dataclass
class GenericRequest:
    type: RequestType
    properties: any

