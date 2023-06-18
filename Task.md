
Azure Client API 
--

Create Azure Client API CLI.
use httpx for GET/POST RestAPI operation.
all needed data: https://learn.microsoft.com/en-us/rest/api/azure/devops/core/?view=azure-devops-rest-6.0


Phase 1: Pyhton CLI API
--

* Authorization:
  * Get API token from Azure devops RestAPI
  * Create a configuration file `settings.ini` and store the key there.
  * Read the key from the config file and do the authoraztion on the begining of the program.
  * Use DataClasses to store the settings & Error & Success Respones.

* CLI: Using Sync Httpx
  * Show welcome message and list of operation. 
  * Create/List/Get/Delete Azure Project.
    * if user chooses create will need to provide a project name.
    * if user chooses List will need to list all Azure projects for the user.
    * if user chooses get will need to list info about the project and list a new list of operation.
  
  * Create/List/Update/Get/Delete Work items:
    * Create a work items ( Task, Bug, ...) for the selected project.
    * https://learn.microsoft.com/en-us/rest/api/azure/devops/processes/work-item-types/list?view=azure-devops-rest-6.0&tabs=HTTP
    * List all work items for the selected project.
    * Update an item.
    * Delete an item.
    * Get an item.


Phase 2: Pyhton CLI API With Async httpx client.
--

  * Write the same program with Httpx Async call and utils it using asyncio or anyio.
  * Use OOP concepts to structure and write these classes.

Phase 3: Telegram Bot API.
--

* send an notification on an every op.

Required Files.
-- 
These files are required for all Future tasks as well.

* Unit-Testing ( pytest ).
* Achievement file.
* PyDoc3
* Pylint
* venv
* requirements.txt
* __init__.py files


