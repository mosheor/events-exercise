from evidence_handler.core.abstract.abstract_field import Field
from evidence_handler.core.abstract.serializable_class import JsonSerializableClass
from evidence_handler.core.consts import KWARGS
from evidence_handler.core.utils import dynamic_import


class Serializer(JsonSerializableClass):
    """
    this class represents a serializer of evidence raw data.
    It is used to convert the raw data to a dictionary that will be sent to the output.
    It contains a list of fields that will be used during the serialization.
    """

    def __init__(self, fields: list[Field]):
        self.fields = fields

    def kwargs_to_dict(self) -> dict:
        return {"fields": [field.to_dict() for field in self.fields]}

    def to_representation(self, data):
        return {field.output_field or field.field_name: field.to_representation(data) for field in self.fields}

    @classmethod
    def from_dict(cls, dict_repr) -> "Serializer":
        fields = []
        for field in dict_repr[KWARGS]["fields"]:
            klass = dynamic_import(field["class"])
            fields.append(klass.from_dict(field))
        return cls(fields=fields)
