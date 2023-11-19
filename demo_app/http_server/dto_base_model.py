from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DTOBaseModel(BaseModel):
    """A base model for all Data Transfer Objects"""
    model_config = ConfigDict(
        alias_generator=to_camel,  # serialize objects using camelCase
    )
