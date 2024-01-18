import abc

from evidence_handler.core.consts import CLASS, KWARGS
from evidence_handler.core.utils import dynamic_import


class JsonSerializableClass(abc.ABC):
    """
    An abstract base class for classes that can be serialized to and deserialized from JSON.
    """

    @classmethod
    def from_dict(cls, dict_repr: dict) -> "JsonSerializableClass":
        """
        create a Field object from a json representation of a Field object
        :param dict_repr: the json representation of a Field object
        """
        field_class = dynamic_import(dict_repr[CLASS])
        if issubclass(field_class, JsonSerializableClass):
            return field_class(**dict_repr[KWARGS])
        raise ValueError("dict_repr is invalid - should be a json representation of a JsonSerializableClass object")

    def to_dict(self) -> dict:
        """
        create a json representation of a Field object
        """
        return {CLASS: f"{self.__class__.__module__}.{self.__class__.__name__}", KWARGS: self.kwargs_to_dict()}

    @abc.abstractmethod
    def kwargs_to_dict(self) -> dict:
        """
        return a dict representation of the init kwargs arguments of the object
        """
        ...
