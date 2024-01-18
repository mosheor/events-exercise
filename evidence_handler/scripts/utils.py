import json

from evidence_handler.core.serializer import Serializer
from evidence_handler.settings import config as app_config


def dumps_config(config: dict[int, Serializer]) -> str:
    """
    Convert a config mapping object into a json representation
    :param config: a dictionary mapping between evidence id to serializer objects
    :return: a json representation of the config
    """
    return json.dumps({k: v.to_dict() for k, v in config.items()}, indent=2)


def dump_config(config: dict[int, Serializer], filename: str = None) -> None:
    """
    Convert a config mapping object into a json representation
    :param config: a dictionary mapping between evidence id to serializer objects
    :param filename: path to save the config to
    """
    with open(filename or app_config.DEFAULT_CONFIG_JSON_PATH, "w") as f:
        f.write(dumps_config(config))


def load_config(filename: str | None = None) -> dict[int, Serializer]:
    """
    Convert a json representation into a config object
    :param filename: a path to json file containing a dictionary mapping between evidence id to serializer jsons
    :return: a dictionary mapping between evidence id to serializer objects
    """
    with open(filename or app_config.DEFAULT_CONFIG_JSON_PATH) as f:
        config_dict = json.load(f)
    return {int(k): Serializer.from_dict(v) for k, v in config_dict.items()}
