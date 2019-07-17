import os
import os.path


def find_saga_config():
    """Find the saga config file."""

    def hasConfig(here):
        config = '{}/saga.yaml'.format(here)
        if os.path.exists(config):
            return config
        return None

    # Walk backwards from the current directory to find the saga.yaml
    here = os.getcwd()

    while here != "/":
        print("Here is {}".format(here))
        if hasConfig(here):
            return here

        here = os.path.dirname(here)

    return None

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

