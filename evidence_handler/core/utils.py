import importlib


def dynamic_import(class_path: str) -> type:
    """
    Dynamically imports a class based on its module path.
    :param class_path: The module path of the class to import.
    :return:
    """
    # Split the module path into module name and class name
    module_name, class_name = class_path.rsplit(".", 1)

    # Import the module
    module = importlib.import_module(module_name)

    # Get the class from the module
    return getattr(module, class_name)
