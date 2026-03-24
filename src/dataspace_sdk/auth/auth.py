from typing import Dict, Optional

import httpx

class TokenAuth(httpx.Auth):

    def __init__(self, token: str):
        self._token = token

    def auth_flow(self, request: httpx.Request):
        request.headers["Authorization"] = f"Bearer {self._token}"
        yield request

class BasicLoginAuth(httpx.Auth):

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
        self._token: str | None = None

    def _fetch_token(self) -> str:
        response = httpx.get(
            f"{self._auth_base_url}{self._login_path}",
            auth=(self._username, self._password),
        )
        response.raise_for_status()
        return response.json()["token"]

    def auth_flow(self, request: httpx.Request):
        if self._token is None:
            self._token = self._fetch_token()

        request.headers["Authorization"] = f"Bearer {self._token}"
        response = yield request

        if response.status_code == 401:
            self._token = self._fetch_token()
            request.headers["Authorization"] = f"Bearer {self._token}"
            yield request