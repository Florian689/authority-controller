from uuid import UUID
from pydantic import BaseModel
from fastapi import HTTPException, Request
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier

# Session Data Model
class SessionData(BaseModel):
    connection_id: str

# Session Cookie Parameters
cookie_params = CookieParameters()

# Session Cookie Frontend
cookie = SessionCookie(
    cookie_name="session_cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="YOUR_SECURE_SECRET_KEY",  # Replace with your secure secret key
    cookie_params=cookie_params,
)

# Session Backend
backend = InMemoryBackend[UUID, SessionData]()

# Session Verifier
class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(self, backend: InMemoryBackend[UUID, SessionData], cookie_name: str):
        super().__init__()
        self._backend = backend
        self._cookie_name = cookie_name
        self._auto_error = True
        self._auth_http_exception = HTTPException(status_code=403, detail="Invalid session")

    async def __call__(self, request: Request) -> SessionData:
        session_id = request.cookies.get(self._cookie_name)
        session_id_uuid = UUID(session_id)
        if session_id_uuid is None:
            print("BasicVerifier: No session ID found")
            if self._auto_error:
                raise self._auth_http_exception
            return None
        try:
            session_data = await self._backend.read(session_id_uuid)
            if session_data is None:
                print("BasicVerifier: No session data found")
                if self._auto_error:
                    raise self._auth_http_exception
                return None
            return session_data
        except Exception as e:
            print(f"Error during session data retrieval: {e}")
            raise self._auth_http_exception

verifier = BasicVerifier(backend=backend, cookie_name="session_cookie")