import abc
from ConfigurationsDataClass import Configurations


class ClientInterface(abc.ABC):
    """since we have more than one client type create a client interface
     with the common methods as abstract methods"""
    headers = None
    patch_headers = None

    def __init__(self):
        """creating configuration object and setting the headers value"""
        self.sett = Configurations()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.sett.authorization
        }
        self.patch_headers = {
            'Content-Type': 'application/json-patch+json',
            'Authorization': 'Basic ' + self.sett.authorization
        }

    @abc.abstractmethod
    def check_response(self, msg, response, send_to_bot):
        """check requests' responses' state """

    @abc.abstractmethod
    def create_project(self, name, description):
        """create project"""

    @abc.abstractmethod
    def list_projects(self):
        """get all available projects"""

    @abc.abstractmethod
    def delete_project(self, project_id):
        """delete specific project"""

    @abc.abstractmethod
    def create_item(self, project_name, item_name, item_type):
        """create item for specific project"""

    @abc.abstractmethod
    def list_items(self, project_name, items_ids):
        """list all projects' items"""

    @abc.abstractmethod
    def update_item(self, project_name, item_id, description):
        """update specific projects' specific item"""

    @abc.abstractmethod
    def get_item(self, project_name, item_id):
        """get specific projects' specific item"""

    @abc.abstractmethod
    def delete_item(self, project_name, item_id):
        """delete specific projects' specific item"""
