from typing import Dict, Optional

import httpx


class Auth:
    def get_headers(self) -> Dict[str, str]:
        raise NotImplementedError

class TokenAuth(Auth):
    def __init__(self, token: str):
        self._token = token

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}"
        }

class BasicLoginAuth(Auth):
    def __init__(
        self,
        auth_base_url: str,
        username: str,
        password: str,
        login_path: str = "/login",
    ):
        self._auth_base_url = auth_base_url.rstrip("/")
        self._username = username
        self._password = password
        self._login_path = login_path
        self._token: Optional[str] = None

    def _fetch_token(self) -> str:
        response = httpx.get(
            f"{self._auth_base_url}{self._login_path}",
            auth=(self._username, self._password),
        )
        response.raise_for_status()
        data = response.json()
        return data["token"]

    def _ensure_token(self):
        if not self._token:
            self._token = self._fetch_token()

    def get_headers(self) -> Dict[str, str]:
        self._ensure_token()
        return {
            "Authorization": f"Bearer {self._token}"
        }