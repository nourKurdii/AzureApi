import httpx
import json
from ResponseDataClass import SuccessResponse, ErrorResponse
from ClientInterface import ClientInterface


class SyncClient(ClientInterface):
    """class for sync client derived from client interface"""

    def __init__(self, bot):
        super().__init__()
        # create httpx sync client instance and pass the proper headers to it
        self.httpx_client = httpx.Client(headers=self.headers)
        self.bot = bot

    def check_response(self, msg, response, send_to_bot):
        """ check the requests' response and according to it
        store the response in the right dataclass"""
        if response.is_success:
            # if response is success store it in success data class ,
            # print msg for user and send the msg to the bot
            if send_to_bot:
                self.bot.add_msg(msg)
                self.bot.send_msg()
            print(msg)
            success_response = SuccessResponse(body=response.text)
        else:
            # if response is error print it to user and store it in error dataclass
            error_response = ErrorResponse(body=response.text)
            print(error_response.body)
        return response

    def create_project(self, name, description):
        """ create a new project """
        try:
            response = self.httpx_client.post(
                url=f"https://dev.azure.com/{self.sett.organization}"
                    f"/_apis/projects?api-version=6.0",
                json={"name": name,
                      "description": description,
                      "capabilities": {
                          "versioncontrol": {
                              "sourceControlType": "Git"
                          },
                          "processTemplate": {
                              "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"
                          }
                      }}
            )

            msg = f"New project on Organization {self.sett.organization} created," \
                  f" Project Name: {name}"
            return self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            self.httpx_client.close()

    def list_projects(self):
        """get list of the available projects"""
        try:
            response = self.httpx_client.get(
                url=f"https://dev.azure.com/{self.sett.organization}"
                    f"/_apis/projects?api-version=5.1")
            parse_json = json.loads(response.text)
            msg = json.dumps(parse_json, indent=2)
            return self.check_response(msg,response,False)

        except httpx.HTTPError as exc:
            error_response = ErrorResponse(body=str(exc))
            print(error_response.body)
            self.httpx_client.close()

    def delete_project(self, project_id):
        """delete specific project by its id"""
        try:
            response = self.httpx_client.delete(
                url=f"https://dev.azure.com/{self.sett.organization}"
                    f"/_apis/projects/{project_id}?api-version=6.0")

            msg = f"Project in Organization {self.sett.organization} deleted," \
                  f" Project Id: {project_id}"
            return self.check_response(msg, response,True)

        except httpx.HTTPError as exc:
            error_response = ErrorResponse(body=str(exc))
            print(error_response.body)
            self.httpx_client.close()

    def create_item(self, project_name, item_name, item_type):
        """create a project item for specific project by its name or id"""
        try:
            response = self.httpx_client.post(
                url=f"https://dev.azure.com/{self.sett.organization}/{project_name}"
                    f"/_apis/wit/workitems/${item_type}?api-version=6.0",
                json=[
                    {
                        "op": "add",
                        "path": "/fields/System.Title",
                        "from": "null",
                        "value": item_name
                    }
                ],
                headers=self.patch_headers)
            msg = f"New {item_type} named: {item_name} created in project {project_name}"
            return self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error_response = ErrorResponse(body=str(exc))
            print(error_response.body)
            self.httpx_client.close()

    def list_items(self, project_name, items_ids):
        """get list of specific projects' items by their ids"""
        try:
            response = self.httpx_client.get(
                url=f"https://dev.azure.com/{self.sett.organization}/{project_name}"
                    f"/_apis/wit/workitems?ids={items_ids}&api-version=7.0")
            parse_json = json.loads(response.text)
            msg = json.dumps(parse_json, indent=2)

            return self.check_response(msg, response, False)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            self.httpx_client.close()

    def update_item(self, project_name, item_id, description):
        """update specific projects' item"""
        try:
            response = self.httpx_client.patch(
                url=f"https://dev.azure.com/{self.sett.organization}"
                    f"/_apis/wit/workitems/{item_id}?api-version=6.0",
                json=[
                    {
                        "op": "add",
                        "path": "/fields/System.History",
                        "value": description
                    },

                ],
                headers=self.patch_headers
            )
            msg = f"Item id {item_id} updated in project : {project_name}"
            return self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            self.httpx_client.close()

    def get_item(self, project_name, item_id):
        """get projects' specific item"""
        try:
            response = self.httpx_client.get(
                url=f"https://dev.azure.com/{self.sett.organization}/{project_name}"
                    f"/_apis/wit/workitems/{item_id}?api-version=7.0")
            msg = response.json()
            return self.check_response(msg, response, False)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            self.httpx_client.close()

    def delete_item(self, project_name, item_id):
        """delete projects' specific item"""
        try:
            response = self.httpx_client.delete(
                url=f"https://dev.azure.com/{self.sett.organization}"
                    f"/{project_name}/_apis/wit/workitems/{item_id}?api-version=6.0")
            msg = f"Item id: {item_id} in project : {project_name} was deleted"
            return self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error_response = ErrorResponse(body=str(exc))
            print(error_response.body)
            self.httpx_client.close()
