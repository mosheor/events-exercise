import abc
from typing import Any

from evidence_handler.core.abstract.serializable_class import JsonSerializableClass
from evidence_handler.core.consts import KWARGS
from evidence_handler.core.utils import dynamic_import


class Field(JsonSerializableClass, abc.ABC):
    """
    this class represents an abstract field in evidence raw data.
    """

    def __init__(self, field_name: str, output_field: str | None = None):
        """
        :param field_name: the field name in the raw data
        :param output_field: the field name in the output data
        """
        self.field_name = field_name
        self.output_field = output_field

    def kwargs_to_dict(self) -> dict:
        """
        return a dict representation of the kwargs of the Field object
        this is used for de/serialization of the Field object
        """
        return {"field_name": self.field_name, "output_field": self.output_field}

    def _get_value(self, data: dict) -> Any:
        """
        get value from dictionary by field_name
        supports nested fields (e.g. "a.b.c")

        :param data: the dictionary to get the value from
        :return: the value of the field
        """
        keys = self.field_name.split(".")
        ret = data

        for key in keys:
            if key not in ret:
                raise ValueError(f"field {self.field_name} is not valid")
            ret = ret[key]

        return ret

    @abc.abstractmethod
    def _to_representation(self, value):
        """
        convert the value of the field to a representation that will be sent to the output
        """
        ...

    def to_representation(self, data: dict):
        """
        convert the value of the field to a representation that will be sent to the output
        """
        value = self._get_value(data)
        self.validate(value=value)
        return self._to_representation(value)

    @abc.abstractmethod
    def validate(self, value):
        """
        validate the value of the field
        @:raises: ValueError if the value is not valid
        """
        ...


class CompositeField(Field, abc.ABC):
    """
    this class represents an abstract composite fields - a field that is composed of other fields
    """

    def __init__(self, fields: list[Field], output_field: str | None = None):
        """
        :param fields: List of fields composing the composite field.
        :param output_field: The field name in the output data.
        """
        super().__init__(field_name="", output_field=output_field)
        self.fields = fields

    def kwargs_to_dict(self) -> dict:
        return {"fields": [field.to_dict() for field in self.fields]}

    @classmethod
    def from_dict(cls, dict_repr) -> "CompositeField":
        fields = []
        for field in dict_repr[KWARGS]["fields"]:
            klass = dynamic_import(field["class"])
            fields.append(klass.from_dict(field))
        return cls(fields=fields, output_field=dict_repr[KWARGS]["output_field"])
