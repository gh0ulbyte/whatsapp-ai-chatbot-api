from __future__ import annotations

from typing import Any, Dict, Optional
import httpx

from .config import settings


class WhatsAppClient:
    def __init__(self) -> None:
        if not settings.whatsapp_phone_number_id:
            raise RuntimeError("Falta WHATSAPP_PHONE_NUMBER_ID en el entorno.")
        if not settings.whatsapp_access_token:
            raise RuntimeError("Falta WHATSAPP_ACCESS_TOKEN en el entorno.")

        self.base_url = (
            f"https://graph.facebook.com/{settings.whatsapp_api_version}"
            f"/{settings.whatsapp_phone_number_id}"
        )
        self.headers = {
            "Authorization": f"Bearer {settings.whatsapp_access_token}",
            "Content-Type": "application/json",
        }

    async def send_text(self, to: str, body: str) -> Dict[str, Any]:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(f"{self.base_url}/messages", headers=self.headers, json=payload)
            r.raise_for_status()
            return r.json()

    async def send_flow(
        self,
        to: str,
        flow_token: str,
        *,
        flow_id: Optional[str] = None,
        flow_action: str = "navigate",
        flow_action_payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
   
        interactive: Dict[str, Any] = {
            "type": "flow",
            "body": {"text": "Continuemos en el formulario."},
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_token": flow_token,
                    "flow_action": flow_action,
                },
            },
        }
        if flow_id:
            interactive["action"]["parameters"]["flow_id"] = flow_id
        if flow_action_payload:
            interactive["action"]["parameters"]["flow_action_payload"] = flow_action_payload

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": interactive,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(f"{self.base_url}/messages", headers=self.headers, json=payload)
            r.raise_for_status()
            return r.json()

