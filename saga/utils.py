import math
import re
import os
import os.path

def wordcount(s):
    # TODO: Do a proper word count
    if isinstance(s, list):
        s = "\n".join(s)
    wc = len(re.findall(r'\w+', s))

    # Round to the nearest 100
    return int(math.ceil(wc / 100.0)) * 100

# def find_saga_config():
#     """Find the saga config file."""

#     def hasConfig(here):
#         config = '{}/saga.yaml'.format(here)
#         if os.path.exists(config):
#             return config
#         return None

#     # Walk backwards from the current directory to find the saga.yaml
#     here = os.path.dirname(__file__)
#     # print("Saga is {}".format(__file__))

#     while here != "/":
#         # print("Here is {}".format(here))
#         if hasConfig(here):
#             return here

#         here = os.path.dirname(here)

#     return None

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

