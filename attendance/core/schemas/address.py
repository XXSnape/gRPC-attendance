from .common import BaseSchema


class AddressSchema(BaseSchema):
    name: str


class AudienceSchema(BaseSchema):
    name: str
    address: AddressSchema
