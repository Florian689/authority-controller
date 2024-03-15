import httpx
import re
import json

async def get_issuer_did(client):
    try:
        response = await client.get('http://host.docker.internal:8023/wallet/did/public')
        response.raise_for_status()
        data = response.json()
        did = f"{data['result']['did']}"
        return did
    except httpx.HTTPError as err:
        print(f"Error fetching issuer DID: {err}")
        return None

async def get_cred_def_id(client, did):
    try:
        response = await client.get('http://host.docker.internal:8023/credential-definitions/created')
        response.raise_for_status()
        data = response.json()
        # Filter and sort the definitions
        filtered = [cred_def for cred_def in data['credential_definition_ids'] if cred_def.startswith(did) and cred_def.endswith('Wahlschein')]
        if not filtered:
            return None
        # Extract version numbers and sort
        def extract_version(cred_def_id):
            return int(re.search(r":(\d+):", cred_def_id).group(1))
        return sorted(filtered, key=extract_version, reverse=True)[0]
    except httpx.HTTPError as err:
        print(f"Error fetching credential definition ID: {err}")
        return None

async def get_schema_info(client, did):
    try:
        response = await client.get('http://host.docker.internal:8023/schemas/created')
        response.raise_for_status()
        data = response.json()
        # Filter and sort the schemas
        filtered = [schema_id for schema_id in data['schema_ids'] if schema_id.startswith(did) and 'Wahlschein' in schema_id]
        if not filtered:
            return None, None
        # Extract version numbers and sort
        def extract_version(schema_id):
            return schema_id.split(':')[-1]
        sorted_schemas = sorted(filtered, key=extract_version, reverse=True)
        latest_schema = sorted_schemas[0]
        version = latest_schema.split(':')[-1]
        return latest_schema, version
    except httpx.HTTPError as err:
        print(f"Error fetching schema information: {err}")
        return None, None

async def send_credential_offer_v2(connection_id):
    async with httpx.AsyncClient() as client:
        issuer_did = await get_issuer_did(client)
        if not issuer_did:
            return False, "issuer_did hat den Wert None"

        cred_def_id = await get_cred_def_id(client, issuer_did)

        if not cred_def_id:
            return False, "cred_def_id hat den Wert None"

        schema_id, schema_version = await get_schema_info(client, issuer_did)
        if not schema_id or not schema_version:
            return False, "schema_id und/oder schema_version hat den Wert None"

        post_body = {
            #"auto_issue": False,
            #"auto_remove": True,
            "auto_remove": False,
            "connection_id": connection_id,
            "credential_preview": {
                "@type": "issue-credential/2.0/credential-preview",
                "attributes": [
                    {"name": "wahlkreis", "value": "12345"},
                    {"name": "id", "value": "6789"}
                ]
            },
            "filter": {
                "indy": {
                    "cred_def_id": cred_def_id,
                    "issuer_did": issuer_did,
                    "schema_id": schema_id,
                    "schema_issuer_did": issuer_did,
                    "schema_name": "Wahlschein",
                    "schema_version": schema_version
                }
            },
            "trace": False
        }

        json_data = json.dumps(post_body)

        try:
            response = await client.post('http://host.docker.internal:8023/issue-credential-2.0/send-offer', data=json_data, headers={'accept': 'application/json', 'Content-Type': 'application/json'})
            response.raise_for_status()
            if response.json().get('state') == 'offer-sent':
                print("Offer successfully sent.")
            else:
                print(f"Error: State of response from send-offer request: {response.json().get('state')}. Should be: 'offer-sent'")
            return True, None
        except httpx.HTTPError as err:
            return False, f"Error sending POST request: {err}"

async def send_credential_offer(connection_id):
    async with httpx.AsyncClient() as client:
        issuer_did = await get_issuer_did(client)
        if not issuer_did:
            return False, "issuer_did hat den Wert None"

        cred_def_id = await get_cred_def_id(client, issuer_did)

        if not cred_def_id:
            return False, "cred_def_id hat den Wert None"

        schema_id, schema_version = await get_schema_info(client, issuer_did)
        if not schema_id or not schema_version:
            return False, "schema_id und/oder schema_version hat den Wert None"

        post_body = {
            "auto_issue": True,
            "auto_remove": True,
            "comment": "string",
            "connection_id": connection_id,
            "cred_def_id": cred_def_id,
            "credential_preview": {
                "@type": "issue-credential/1.0/credential-preview",
                "attributes": [
                    {"name": "wahlkreis", "value": "12345"},
                    {"name": "id", "value": "6789"}
                ]
            },
            "trace": True
        }

        json_data = json.dumps(post_body)

        try:
            response = await client.post('http://host.docker.internal:8023/issue-credential/send-offer', data=json_data, headers={'accept': 'application/json', 'Content-Type': 'application/json'})
            response.raise_for_status()
            if response.json().get('state') == 'offer-sent':
                print("Offer successfully sent.")
            else:
                print(f"Error: State of response from send-offer request: {response.json().get('state')}. Should be: 'offer-sent'")
            return True, None
        except httpx.HTTPError as err:
            return False, f"Error sending POST request: {err}"

#Issue Credential if '--no-auto' is set
async def issue_credential(cred_ex_id):
    async with httpx.AsyncClient() as client:
        http_url = f"http://host.docker.internal:8023/issue-credential-2.0/records/{cred_ex_id}/issue"
        body_content = {}
        try:
            response = await client.post(http_url, json=body_content, headers={'accept': 'application/json', 'Content-Type': 'application/json'})
            response.raise_for_status()
            return "POST 'issue-credential-2.0' request sent successfully"
        except httpx.HTTPError as err:
            return f"Error sending POST 'issue-credential-2.0' request: {err}"