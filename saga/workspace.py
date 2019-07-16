import os
import os.path
import yaml


class Workspace():
    configFile = "saga.yaml"

    def __init__(self, *args, **kwargs):
        self.workspace = os.getcwd()
        pass

    # Public methods

    def Initialize(self):
        print("Checking")
        if self.is_initialized():
            print("Already initialized")
        else:
            print("Not initialized yet")

        self.create_config()


    # Internal methods

    def create_config(self):
        """Create a new Config file."""

        data = dict(
            A = 'a',
            author = dict(
                name = 'Your name',
                email = 'Your email',
                phone = '(555) 555-1234',
                address1 = '123 Main St.',
                address2 = 'P.O. Box 2019',
                city = 'MyTown',
                state = 'Ontario',
                country = 'Canada',
            )

        )

        with open(self.get_config_file(), 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    def get_config_file(self):
        return "{}/{}".format(self.workspace, self.configFile)

    def is_initialized(self):
        """Is saga initialized?"""
        if os.path.exists(self.get_config_file()):
            return True
        else:
            return False


    