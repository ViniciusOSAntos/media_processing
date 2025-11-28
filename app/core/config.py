import os
from dataclasses import dataclass


@dataclass
class Settings:
    """
    Class settings project
    """

    api_version = "1.0.0"
    environment = os.getenv("ENVIRONMENT", "local")
    domain_permissions = os.getenv(
        "DOMAIN_PERMISSIONS", "permissions.backstage.dev.globoi.com"
    )
    gcs_api_access_endpoint = os.getenv(
        "GCS_API_ACCESS_ENDPOINT", "http://0.0.0.0:4443"
    )
    google_application_credentials = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", None
    )

    gcp_project = os.getenv("GCP_PROJECT", None)

    gcp_database_name = os.getenv("GCP_DATABASE_NAME", "default")
    gcp_service_account_email = os.getenv("GCP_SERVICE_ACCOUNT_EMAIL", None)

    download_speed = int(os.getenv("DOWNLOAD_SPEED_KBPS", "300"))
    time_multiplier = float(os.getenv("TIME_MULTIPLIER", "2.0"))
    buffer_time = int(os.getenv("BUFFER_TIME_S", "180"))


settings = Settings()
