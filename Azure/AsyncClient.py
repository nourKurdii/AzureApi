import json
import httpx
from ClientInterface import ClientInterface
from ResponseDataClass import SuccessResponse, ErrorResponse


class AsyncClient(ClientInterface):
    """class for async client derived from client interface"""
    def __init__(self, bot):
        super().__init__()
        # create httpx async client instance and pass the proper headers to it
        self.httpx_client = httpx.AsyncClient(headers=self.headers)
        self.bot = bot

    async def check_response(self, msg, response, send_to_bot):
        """according to the requests' response store the response in the right dataclass"""
        if response.is_success:
            # if response is success store it in success data class ,
            # print msg for user and send the msg to the bot
            print(msg)
            success_response = SuccessResponse(body=response.text)
            if send_to_bot:
                self.bot.add_msg(msg)
                self.bot.send_msg()

        else:
            # if response is error print it to user and store it in error dataclass
            error_response = ErrorResponse(body=response.text)
            print(error_response.body)

        return response

    # since async methods are coroutines they must await some returned value
    async def create_project(self, name, description):
        """create a new project"""
        try:
            response = await self.httpx_client.post(
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
            return await self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()

    async def list_projects(self):
        """get list of the available projects"""
        try:
            response = await self.httpx_client.get(
                url=f"https://dev.azure.com/{self.sett.organization}"
                    f"/_apis/projects?api-version=5.1")
            parse_json = json.loads(response.text)
            msg = json.dumps(parse_json, indent=2)
            return await self.check_response(msg, response, False)

        except httpx.HTTPError as exc:
            error_response = ErrorResponse(body=str(exc))
            print(error_response.body)

            return await self.httpx_client.aclose()

    async def delete_project(self, project_id):
        """delete specific project by its id"""
        try:
            response = await self.httpx_client.delete(
                url=f"https://dev.azure.com/{self.sett.organization}/_apis/projects/"
                    f"{project_id}?api-version=6.0")

            msg = f"Project in Organization {self.sett.organization} deleted," \
                  f" Project Id: {project_id}"
            return await self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()

    async def create_item(self, project_name, item_name, item_type):
        """create a project item for specific project by its name or id"""
        try:
            response = await self.httpx_client.post(
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
            return await self.check_response(msg, response, False)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()

    async def list_items(self, project_name, items_ids):
        """get list of specific projects' items by their ids"""
        try:
            response = await self.httpx_client.get(
                url=f"https://dev.azure.com/{self.sett.organization}/{project_name}"
                    f"/_apis/wit/workitems?ids={items_ids}&api-version=7.0")

            parse_json = json.loads(response.text)
            msg = json.dumps(parse_json, indent=2)

            return await self.check_response(msg, response, False)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()

    async def update_item(self, project_name, item_id, description):
        """update specific projects' item"""
        try:
            response = await self.httpx_client.patch(
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
            msg = "Item id {} updated in project : {}".format(item_id, project_name)
            return await self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()

    async def get_item(self, project_name, item_id):
        """get projects' specific item"""
        try:
            response = await self.httpx_client.get(
                url=f"https://dev.azure.com/{self.sett.organization}/{project_name}"
                    f"/_apis/wit/workitems/{item_id}?api-version=7.0")

            msg = response.json()
            return await self.check_response(msg, response, False)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()

    async def delete_item(self, project_name, item_id):
        """delete projects' specific item"""
        try:
            response = await self.httpx_client.delete(
                url=f"https://dev.azure.com/{self.sett.organization}/{project_name}"
                    f"/_apis/wit/workitems/{item_id}?api-version=7.0")

            msg = f"Item id: {item_id} in project : {project_name} was deleted"
            return await self.check_response(msg, response, True)

        except httpx.HTTPError as exc:
            error = ErrorResponse(body=str(exc))
            print(error.body)
            return await self.httpx_client.aclose()
