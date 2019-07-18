import os
import os.path

def find_saga_config():
    """Find the saga config file."""

    def hasConfig(here):
        if os.path.exists('{}/saga.yaml'.format(here)):
            return True
        return False

    # Walk backwards from the current directory to find the saga.yaml
    here = os.path.dirname(os.getcwd())

    while here != "/":
        # print("Here is {}".format(here))
        if hasConfig(here):
            return here

        here = os.path.dirname(here)


    # saga = os.path.dirname(os.path.dirname(here))

    # if os.path.exists('{}/saga.yaml'.format(saga)):
    #     return ""

    return None

def find_saga_lib():
    """Find the saga libraries."""

    return os.path.dirname(
        os.path.dirname(__file__)
    )
