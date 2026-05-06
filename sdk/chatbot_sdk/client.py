import requests


class ChatBot:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def send(self, message, session_id=None):
        payload = {"message": message}
        if session_id:
            payload["session_id"] = session_id
        resp = requests.post(f"{self.base_url}/api/chat/", json=payload)
        resp.raise_for_status()
        return resp.json()

    def history(self, session_id):
        resp = requests.get(f"{self.base_url}/api/history/{session_id}/")
        resp.raise_for_status()
        return resp.json()

    def clear(self, session_id):
        resp = requests.delete(f"{self.base_url}/api/session/{session_id}/")
        resp.raise_for_status()
        return resp.json()

    def health(self):
        resp = requests.get(f"{self.base_url}/api/health/")
        resp.raise_for_status()
        return resp.json()
