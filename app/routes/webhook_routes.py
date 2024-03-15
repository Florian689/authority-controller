from fastapi import APIRouter, Request
import httpx
from .websocket_routes import active_websockets
from ..modules.credential_functions import issue_credential

router = APIRouter()

@router.post('/topic/connections/')
async def webhook_topic_connections(request: Request):
    data = await request.json()
    print(f"Webhook received on path /webhook/topic/connections: {data.get('state')}")
    # Acccept DidComm connection from Voter
    if data.get('state') == 'request':
        connection_id = data.get('connection_id')
        if connection_id:
            url = f'http://172.17.0.1:8021/connections/{connection_id}/accept-request'
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json={})
                if response.status_code == 200:
                    print(f"Request accepted for connection ID: {connection_id}")
                else:
                    print(f"Failed to accept request for connection ID: {connection_id}, Status Code: {response.status_code}")
        else:
            print("Webhook data with 'state':'request' does not contain 'connection_id' or it is None.")
    # Update UI when DidComm Connection was successfull
    elif data.get('state') == 'active':
        print("Connection to Voter Wallet successfull")
        for ws in active_websockets:
            await ws.send_text("update_ui_conn_suc")

    return {"detail": "Webhook received"}

@router.post('/topic/issue_credential_v2_0/')
async def webhook_issue_credential_v20(request: Request):
    data = await request.json()
    state = data.get('state')
    print(f"Webhook received on path /webhook/topic/issue_credential_v2_0/ with state: {state}")
    if state == 'request-received':
        message = await issue_credential(data.get('cred_ex_id'))
        print(message)
    return {"detail": "Webhook received"}

@router.post('/topic/issue_credential/')
async def webhook_issue_credential_v10(request: Request):
    data = await request.json()
    state = data.get('state')
    print(f"Webhook received on path /webhook/issue_credential/ with state: {state}")
    if state == 'credential_issued':
        print("Credential issued successfully")
        for ws in active_websockets:
            await ws.send_text("update_ui_cred_issued")
    else:
        print(f"Webhook received on path /webhook/issue_credential/ with state: {state}")
    return {"detail": "Webhook received"}

@router.post('/{path:path}')
async def webhook_general_listener(request: Request, path: str):
    data = await request.json()
    print(f"Webhook received on path /webhook/{path}") #: {data}")
    # Add processing logic here
    return {"detail": "Webhook received"}
