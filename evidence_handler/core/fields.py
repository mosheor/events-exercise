from datetime import datetime

from dateutil import parser
from dateutil.parser import ParserError
from email_validator import validate_email

from evidence_handler.core.abstract.abstract_field import CompositeField, Field
from evidence_handler.core.consts import KWARGS
from evidence_handler.core.utils import dynamic_import


class IntegerField(Field):
    """
    this class represents an integer field.
    """

    def _to_representation(self, value) -> int:
        return int(value)

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"field {self.field_name} is not an integer")


class StringField(Field):
    """
    this class represents a string field.
    """

    def _to_representation(self, value) -> str:
        return str(value)

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"field {self.field_name} is not a string")


class EmailField(StringField):
    """
    this class represents an email field.
    """

    def validate(self, value):
        super().validate(value)
        validate_email(value, check_deliverability=False)


class DateTimeField(Field):
    """
    this class represents a datetime field.
    """

    def _to_representation(self, value) -> datetime:
        return parser.parse(value)

    def validate(self, value):
        try:
            parser.parse(value)
        except ParserError as e:
            raise ValueError(f"field {self.field_name} is not a datetime string representation") from e


class BooleanField(Field):
    """
    this class represents a boolean field.
    """

    def _to_representation(self, value) -> bool:
        return bool(value)

    def validate(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"field {self.field_name} is not a boolean")


class StrConcatFields(CompositeField):
    """
    this class represents a string field that is composed of other fields which are concatenated together by a
    separator string.
    """

    def __init__(self, fields: list[Field], output_field: str | None = None, separator: str = " "):
        """
        :param fields: List of fields composing the composite field.
        :param output_field: The field name in the output data.
        :param separator: The separator string.
        """
        super().__init__(fields=fields, output_field=output_field)
        self.separator = separator

    def kwargs_to_dict(self) -> dict:
        return super().kwargs_to_dict() | {"output_field": self.output_field, "separator": self.separator}

    @classmethod
    def from_dict(cls, dict_repr) -> "StrConcatFields":
        fields = []
        for field in dict_repr[KWARGS]["fields"]:
            klass = dynamic_import(field["class"])
            fields.append(klass.from_dict(field))
        return cls(
            fields=fields, output_field=dict_repr[KWARGS]["output_field"], separator=dict_repr[KWARGS]["separator"]
        )

    def to_representation(self, data: dict):
        return self.separator.join(self._to_representation(data))

    def _to_representation(self, data: dict) -> list:
        return [field.to_representation(data) for field in self.fields]

    def validate(self, value):
        pass  # Done in every field separately
