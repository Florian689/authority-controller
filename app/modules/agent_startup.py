import httpx
import json
import asyncio

credential_definition_id_global = None
issuer_did_global = None

def get_cred_def_id():
    return credential_definition_id_global

def get_issuer_did():
    return issuer_did_global

async def request_issuer_did():
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get('http://172.17.0.1:8021/wallet/did/public')
            response.raise_for_status()
            data = response.json()
            issuer_did = data['result']['did']
            return issuer_did
        except httpx.HTTPError as err:
            print(f"Error fetching issuer DID: {err}")
            return None

async def check_existing_schema():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get('http://172.17.0.1:8021/schemas/created', headers={'accept': 'application/json'})
        schemas = response.json()['schema_ids']
        for sid in schemas:
            if sid.endswith("Wahlschein:1.0"):
                return sid
        return None

async def create_schema():
    existing_schema_id = await check_existing_schema()
    if existing_schema_id:
        print("Schema already exists:", existing_schema_id)
        return "exists", existing_schema_id
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        post_body = {
            "attributes": ["wahlkreis", "polling_card_token"],
            "schema_name": "Wahlschein",
            "schema_version": "1.0"
        }
        json_data = json.dumps(post_body)
        url = 'http://172.17.0.1:8021/schemas'
        try:
            response = await client.post(url, data=json_data, headers={'accept': 'application/json', 'Content-Type': 'application/json'})
            response.raise_for_status()
            return True, response.json()['schema_id']
        except httpx.HTTPError as err:
            print("Error sending POST request:", err)
            return False, None

async def check_existing_credential_definition(schema_id):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f'http://172.17.0.1:8021/credential-definitions/created?schema_id={schema_id}', headers={'accept': 'application/json'})
        credential_definitions = response.json()['credential_definition_ids']
        for cdid in credential_definitions:
            if cdid.endswith("default"):
                return cdid
        return None

async def create_def(schema_id):
    existing_cred_def_id = await check_existing_credential_definition(schema_id)
    if existing_cred_def_id:
        print("Credential definition already exists:", existing_cred_def_id)
        return "exists", existing_cred_def_id

    async with httpx.AsyncClient(timeout=30.0) as client:
        post_body = {
            "schema_id": schema_id,
            "support_revocation": False,
            "tag": "default"
        }
        json_data = json.dumps(post_body)
        url = 'http://172.17.0.1:8021/credential-definitions'
        try:
            response = await client.post(url, data=json_data, headers={'accept': 'application/json', 'Content-Type': 'application/json'})
            response.raise_for_status()
            return True, response.json()['credential_definition_id']
        except httpx.HTTPError as err:
            print("Error sending POST request:", err)
            return False, None

async def initialize_schema_and_def():
    global credential_definition_id_global
    global issuer_did_global

    issuer_did_global = await request_issuer_did() 

    schema_creation_status, schema_id = await create_schema()

    if not schema_id:
        print("Error: Failed to obtain or find an existing schema_id")
        return

    def_creation_status, credential_definition_id = await create_def(schema_id)

    if not credential_definition_id:
        print("Error: Failed to obtain or find an existing credential_definition_id")
        return

    credential_definition_id_global = credential_definition_id 
    print("Global Credential Definition ID:", credential_definition_id_global)
    print("Global Issuer DID:", issuer_did_global)