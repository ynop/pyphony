import os


def get_resource_path(sub_path_components):
    """
    Get the absolute path of a file in the resources folder
    with its relative path components.
    """

    if type(sub_path_components) not in (list, tuple):
        sub_path_components = (sub_path_components)

    path = os.path.join(
        os.path.dirname(__file__),
        *sub_path_components
    )

    return os.path.abspath(path)
