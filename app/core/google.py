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

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def access_token_to_gcs_signed_url(self):
        """
        Get access token
        :return: Access token
        """
        if not settings.gcp_service_account_email:
            return None

        client = iam_credentials_v1.IAMCredentialsClient()

        name = path_template.expand(
            "projects/{project}/serviceAccounts/{service_account}",
            project="-",
            service_account=settings.gcp_service_account_email,
        )

        scope = [
            "https://www.googleapis.com/auth/devstorage.read_write",
            "https://www.googleapis.com/auth/iam",
        ]

        response = client.generate_access_token(name=name, scope=scope)
        return response.access_token
