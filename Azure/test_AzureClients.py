import asyncio
import json
import pytest

from AsyncClient import AsyncClient
from SyncClient import SyncClient
import TelegramBot

import random
import string

bot = TelegramBot.TelegramBot()

sync_client = SyncClient(bot)
async_client = AsyncClient(bot)

project_id = None
item_id = None


@pytest.fixture
def random_name():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


@pytest.fixture
def random_item_type():
    items_list = ['Epic', 'Bug', 'Task', 'Feature', 'Impediment', 'Test Case', 'Product Backlog Item']
    return random.choice(items_list)


@pytest.fixture(scope="session")
def event_loop():
    # create event loop for the session and use it across all tests
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def test_create_project_with_sync(random_name):
    name = desc = random_name
    assert sync_client.create_project(name, desc).status_code == 202


def test_list_projects_with_sync():
    response = sync_client.list_projects()
    parse_json = json.loads(response.text)
    global project_id
    project_id = parse_json['value'][0]['id']
    assert response.status_code == 200


def test_create_project_item_with_sync_client(random_name, random_item_type):
    response = sync_client.create_item(project_id, item_name=random_name, item_type=random_item_type)
    parse_json = json.loads(response.text)
    global item_id
    item_id = parse_json['id']
    assert response.status_code == 200


def test_list_project_items_with_sync_client():
    response = sync_client.list_items(project_id, item_id)
    assert response.status_code == 200


def test_update_project_item(random_name):
    response = sync_client.update_item(project_id, item_id, random_name)
    parse_json = json.loads(response.text)
    response_updated_value = parse_json['fields']['System.History']
    assert response_updated_value == random_name


def test_get_project_item_with_sync_client():
    response = sync_client.get_item(project_id, item_id)
    parse_json = json.loads(response.text)
    response_item_id = parse_json['id']
    assert response_item_id == item_id


def test_delete_project_item_with_sync_client():
    response = sync_client.delete_item(project_id, item_id)
    assert response.status_code == 200


def test_delete_project_with_sync_client():
    response = sync_client.delete_project(project_id)
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_create_project_with_async_client(random_name):
    name = desc = random_name
    response = await async_client.create_project(name, desc)
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_list_projects_with_async_client():
    response = await async_client.list_projects()
    parse_json = json.loads(response.text)
    assert response.status_code == 200
    global project_id
    project_id = parse_json['value'][0]['id']


@pytest.mark.asyncio
async def test_create_project_item_with_async_client(random_name):
    response = await async_client.create_item(project_id, item_name=random_name, item_type='Task')
    parse_json = json.loads(response.text)
    global item_id
    item_id = parse_json['id']
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_project_items_with_async_client():
    response = await async_client.list_items(project_id, item_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_project_item_with_async_client(random_name):
    response = await async_client.update_item(project_id, item_id, random_name)
    parse_json = json.loads(response.text)
    response_updated_value = parse_json['fields']['System.History']
    assert response_updated_value == random_name


@pytest.mark.asyncio
async def test_get_project_item_with_async_client():
    response = await async_client.get_item(project_id, item_id)
    parse_json = json.loads(response.text)
    response_item_id = parse_json['id']
    assert response_item_id == item_id


@pytest.mark.asyncio
async def test_delete_project_item_with_async_client():
    response = await async_client.delete_item(project_id, item_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_project_with_async_client():
    response = await async_client.delete_project(project_id)
    assert response.status_code == 202
