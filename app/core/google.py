from google.cloud import storage
from google.auth.credentials import AnonymousCredentials
from app.core.config import settings

from cachetools import cached, TTLCache

class Google:
    """
    Class Google
    """

    def get_storage_client(self):
        """
        Get storage client
        :return: Storage client
        """
        if settings.environment != "local":
            return storage.Client(
                project=settings.gcp_project,
            )

        if not settings.google_application_credentials:
            return storage.Client(
                credentials=AnonymousCredentials(),
                client_options={
                    "api_endpoint": settings.gcs_api_access_endpoint
                },
            )

        return storage.Client()
