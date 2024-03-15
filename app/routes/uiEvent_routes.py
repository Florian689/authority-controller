from fastapi import APIRouter, Response as FastAPIResponse, Depends
from fastapi.responses import JSONResponse
import httpx
import json
from ..modules.idData_processing import verify_voter_registration
from uuid import uuid4
from ..modules.session_manager import backend, SessionData, cookie, verifier
from ..modules.credential_functions import send_credential_offer

router = APIRouter()

@router.get('/generate-invitation')
async def generate_invitation(response: FastAPIResponse):
    async with httpx.AsyncClient() as client:
        httpx_response = await client.post('http://172.17.0.1:8021/connections/create-invitation')
        
        # Ensure the httpx response is successful before proceeding
        if httpx_response.status_code != 200:
            return JSONResponse(content={"error": "Failed to get invitation"}, status_code=httpx_response.status_code)

        invitation_data = httpx_response.json()
        invitation_url = invitation_data.get('invitation_url')
        if not invitation_url:
            return JSONResponse(content={"error": "Invitation URL not found"}, status_code=500)
        print("Invitation: ", json.dumps(invitation_data))
        print("Invitation URL: ", invitation_url)

        # Create a session and store the connection_id
        session_id = uuid4()
        session_data = SessionData(connection_id=invitation_data.get('connection_id'))
        await backend.create(session_id, session_data)
        cookie.attach_to_response(response, session_id)

        #Generate the http response
        response.set_cookie(
            key="session_cookie",
            value=str(session_id),
            httponly=True,
            samesite="Lax",  # Controls when cookies are sent with requests from external sites
            secure=False,  # Set to False for development. In production, should be True over HTTPS
        )
        content = json.dumps({'invitation_url': invitation_url})
        response.body = content.encode('utf-8')
        response.status_code = 200
        response.media_type = "application/json"

        # Return the Invitation URL and the session_id Cookie
        return response
    
@router.get('/start-eID')
async def startEId(session_data: SessionData = Depends(verifier)):
    if not session_data:
        print("No session data")

    async with httpx.AsyncClient() as client:

        #TODO: eID-Prozess implementieren und User Daten zurückgeben
        # Authentisierungsanfrage an eID-Server
        # eID-Server baut verbindung zu AusweisApp 2 auf
        # Authentizität des Diensteanbierters (diese Software) und des Ausweises wird überprüft
        # Ausweisende Person bestätigt Übermittlung der Daten durch Eingabe der PIN
        # Ausweisdaten werden an eID-Server übermittelt
        # eID-Server schickt Authentisierungsantwort und Ausweisdaten an den Dienst (diese Software)
        # Authentisierungsantwort und Ausweisdaten auslesen und enscheiden, ob Authentisierung erfolgreich war
        # Antwort an den Nutzer, mit Ergebnis der Ausweisprüfung
        # im Positiv-Fall -> diese Funktion gibt die Ausweisdaten zurück

        # Hardcoded response for demonstration
        if True: #set to false for negative authentication
            result = {
                "success": True,
                "data": {
                    "surname": "Bauer",
                    "first_name": "Max",
                    "date_of_birth": "1985-07-12",
                    "city_code": "10115",
                    "city": "Berlin",
                    "street": "Hauptstrasse",
                    "house_number": "1",
                }
            }
        else: 
            result = {
                "success": False,
            }
        #Hardcoded response end
        
        if result["success"]:
            #Check if Voter has an entry in the voters register
            verification_success = verify_voter_registration(result["data"])
            if verification_success:
                print("Verification successfull")
                connection_id = session_data.connection_id
                success, message = await send_credential_offer(connection_id)
                if not success:
                    print(message)
                return JSONResponse(content={'success': True, 'message': "Ihre Daten wurden erfolgreich mit dem Wählerverzeichnis abgeglichen. Ihr digitaler Wahlschein wird nun an Ihr Wallet gesendet. Bitte überprüfen Sie ihr Wallet und akzeptieren Sie die Zusendung."})
            else:
                print("Error: Voters Register Verification not successful.")
                return JSONResponse(content={'success': False, 'message': "Leider konnte kein Eintrag zu Ihrer Person im Wählerverzeichnis gefunden werden."})
        else:
            print("Error: eID-Service not successful")
            return JSONResponse(content={'success': False, 'message': "Authentifizierung fehlgeschlagen. Bitte versuchen Sie es erneut!"})