from google.cloud import storage
from google.cloud import secretmanager
from google.oauth2 import service_account
import json

# Initialize the Secret Manager client


def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": secret_name})
    secret_payload = response.payload.data.decode("UTF-8")
    return secret_payload

# Load service account credentials


def authenticate_with_service_account_from_secret(project_id, secret_id):
    service_account_key_json = access_secret_version(project_id, secret_id)
    print(service_account_key_json)
    with open("CREDENTIALS_FILE.json", "w") as f:
        f.write(service_account_key_json)
    service_account_info = json.loads(service_account_key_json)

    # Create credentials from the service account key JSON
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info)

    return credentials


# Example usage
project_id = "forward-pad-429200-d1"
secret_id = "new-secret-manager"

credentials = authenticate_with_service_account_from_secret(
    project_id, secret_id)

# Use the credentials to authenticate with Google Cloud services
# Example: Create a client for Google Cloud Storage
storage_client = storage.Client(credentials=credentials)
buckets = list(storage_client.list_buckets())
print(buckets)
