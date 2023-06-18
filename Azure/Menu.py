from ClientFactory import ClientFactory


class Menu:
    """Menu class contains menus' data and functionality"""
    clients_options = ["Sync", "Async"]
    main_options = ["Create", "List", "Get", "Delete", "Exit"]
    get_options = ['Create', 'List', 'Update', 'Get', 'Delete']
    items_list = ['Epic', 'Bug', 'Task', 'Feature', 'Impediment',
                  'Test Case', 'Product Backlog Item']

    def __init__(self):
        self.client_type = None
        # while run is true the fist menu will stay displayed after each operation
        self.run = True
        self.client = None

    def pick_client(self, bot):
        """choose client type"""
        print("Please choose Your Option:")
        for i, element in enumerate(self.clients_options):
            print(f"{i + 1}) {element}")

        j = input("Enter number: ")
        if 0 < int(j) <= len(self.clients_options):
            match int(j):
                case 1:
                    self.client_type = "Sync"

                case 2:
                    self.client_type = "Async"

            # call client factory to create client object
            # according to chosen type and pass the bot to it
            self.client = ClientFactory.create_client(self.client_type, bot)

    def run_menu(self):
        """if the chosen client is async call the subroutine run_async
        if chosen is sync call run_sync"""
        if self.client_type == 'Async':
            return self.run_async
        return self.run_sync

    async def run_async(self):
        """run pick request menu according to the chosen client"""
        while self.run:
            # pass the client object and the first list to "pick request menu"
            await self.pick_request(self.main_options, "first_list", self.client)

    def run_sync(self):
        """run "pick request menu" for sync client"""
        while self.run:
            self.pick_request(self.main_options, "first_list", self.client)

    def pick_request(self, options: list, which_list: str, client_object):
        """ display the first menu options to the user and switch the chosen operation """
        print("Please choose Your Option:")

        for i, element in enumerate(options):
            print(f"{i + 1}) {element}")

        j = input("Enter number: ")
        try:
            if 0 < int(j) <= len(options):
                # pass the chosen operation and the chosen client object
                return self.switch_option(which_list, int(j), client_object)

        except Exception as err:
            print(err)
            raise err

    def pick_item_type(self):
        """display menu of possible item types"""
        print("Please choose Your Option:")
        for i, element in enumerate(self.items_list):
            print(f"{i + 1}) {element}")

        j = input("Enter number: ")
        try:
            if 0 < int(j) <= len(self.items_list):
                match int(j):
                    case 1:
                        return "Epic"
                    case 2:
                        return "Bug"
                    case 3:
                        return "Task"
                    case 4:
                        return "Feature"
                    case 5:
                        return "Impediment"
                    case 6:
                        return "Test Case"
                    case 7:
                        return "Product Backlog Item"

        except:
            pass

    def switch_option(self, which_list, option, client_object):
        """switch chosen menus' operation"""
        match which_list:
            # case "first list" displays the available operations that can be made on project level
            # then calls the chosen objects' method according to the chosen operation
            case "first_list":
                match option:
                    case 1:
                        name = input("please enter project name: ")
                        description = input("project description: ")
                        return client_object.create_project(name, description)
                    case 2:
                        return client_object.list_projects()
                    case 3:
                        return self.pick_request(self.get_options, "second_list", client_object)
                    case 4:
                        project_id = input("project id: ")
                        return client_object.delete_project(project_id)
                    case 5:
                        self.run = False
            # case "second list" displays the available operations
            # that can be made on project items' level
            case "second_list":
                match option:
                    case 1:
                        item_type = self.pick_item_type()
                        project_name = input("project name: ")
                        item_name = input("item name: ")
                        return client_object.create_item(project_name, item_name, item_type)
                    case 2:
                        project_name = input("project name: ")
                        list_of_input = input("Items Ids: ")
                        item_ids_as_string = str(list_of_input)
                        item_ids_as_string = item_ids_as_string.replace(' ', ',')
                        return client_object.list_items(project_name, item_ids_as_string)

                    case 3:
                        project_name = input("project name: ")
                        item_id = input("item id: ")
                        description = input("description: ")
                        return client_object.update_item(project_name, item_id, description)
                    case 4:
                        project_name = input("project name: ")
                        item_id = input("item id: ")
                        return client_object.get_item(project_name, item_id)
                    case 5:
                        project_name = input("project name: ")
                        item_id = input("item id: ")
                        return client_object.delete_item(project_name, item_id)
