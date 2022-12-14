from google.cloud import storage
from google.oauth2 import service_account

import config

credentials = service_account.Credentials.from_service_account_file(config.GCP_CONFIG['KEY_PATH'])


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = storage_client.bucket(config.GCP_CONFIG['bucket_name'])
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
