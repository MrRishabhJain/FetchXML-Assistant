import json
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI


def read_file(file_path, is_json=False):
  with open(file_path, 'r') as file:
    if is_json:
      return json.load(file)
    return file.read()

def create_client_and_assistant(instruction_file, tools_file):

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    
    client = AzureOpenAI(
        azure_endpoint = "https://openai-pva.openai.azure.com/", #os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-02-15-preview",
        azure_ad_token_provider=token_provider
    )

    assistant = client.beta.assistants.create(
    model="gpt-4o-mini", # replace with model deployment name.
    instructions=read_file(instruction_file),
    tools=read_file(tools_file, is_json=True),
    )

    return client, assistant.id
