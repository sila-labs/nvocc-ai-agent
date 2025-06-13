# app/services/maersk_token.py

import time
import requests
import os

class MaerskTokenManager:
    def __init__(self, scope="maersk.com"):
        self.token_url = "https://identity.maersk.com/connect/token"
        self.client_id = os.getenv("MAERSK_CLIENT_ID")
        self.client_secret = os.getenv("MAERSK_CLIENT_SECRET")
        self.scope = scope
        self.access_token = None
        self.token_expiry = 0

        if not self.client_id or not self.client_secret:
            raise ValueError("Missing Maersk client credentials in environment variables")

    def _fetch_token(self):
        print("[MaerskTokenManager] Fetching new OAuth token from Maersk...")
        response = requests.post(
            self.token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": self.scope,
            },
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch token: {response.status_code} - {response.text}")

        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.token_expiry = time.time() + token_data["expires_in"] - 60  # 1-min buffer

    def get_token(self):
        if not self.access_token or time.time() >= self.token_expiry:
            self._fetch_token()
        return self.access_token

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.get_token()}"}
