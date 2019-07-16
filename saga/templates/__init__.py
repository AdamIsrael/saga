import os
import os.path


def list_templates():
    """List the installed templates.

    :return: A list of installed templates
    """
    here = os.path.dirname(os.path.abspath(__file__))

    files = [f for f in os.listdir(here) if os.path.isfile("{}/{}".format(here, f))]
    templates = []
    for file in files:
        if file not in ['__init__.py', '__pycache__']:
            templates.append(file[:-3])
    return templates
templates = list_templates()

