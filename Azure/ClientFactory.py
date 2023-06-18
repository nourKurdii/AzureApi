import AsyncClient
from SyncClient import SyncClient


class ClientFactory:
    """client factory to create the appropriate client object"""
    @staticmethod
    def create_client(client_type, bot):
        if client_type is None:
            return None
        if client_type == "Sync":
            return SyncClient(bot)
        if client_type == "Async":
            return AsyncClient.AsyncClient(bot)
