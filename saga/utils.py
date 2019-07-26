import os
import os.path


class ReadingTime():
    def Estimate(self, wordcount, wpm=300):
        """Estimate the average reading time.

        Estimates the average reading time based on the Word count and Words per Minute.

        :param wordcount int: The words to be read.
        :param wpm int: The words per minute (based on reading difficulty)

        :return int: The time, in minutes, to read the work.

        Example:

        s = ReadingTime.Estimate(100000, 300)
        """

        return int(round(wordcount / wpm, 0))


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
    here = os.path.join(here, "templates")
    # print(here)
    files = [f for f in os.listdir(here) if os.path.isfile("{}/{}".format(here, f))]
    templates = []
    for file in files:
        if file not in ['__init__.py', '__pycache__']:
            templates.append(file[:-3])
    return templates
templates = list_templates()

