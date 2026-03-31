from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from app.config import settings
from app.webhook_security import verify_meta_signature
from app.whatsapp_client import WhatsAppClient


app = FastAPI(title="WhatsApp Flows (REST + Webhooks)", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}



# Webhook de Meta (verificación)

@app.get("/webhook")
def webhook_verify(
    hub_mode: Optional[str] = None,
    hub_challenge: Optional[str] = None,
    hub_verify_token: Optional[str] = None,
) -> Any:
    """
    Meta enviará query params:
    - hub.mode
    - hub.challenge
    - hub.verify_token
    FastAPI los mapea a hub_mode/hub_challenge/hub_verify_token.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.webhook_verify_token:
        return int(hub_challenge or "0")
    raise HTTPException(status_code=403, detail="Webhook verification failed")


@app.post("/webhook")
async def webhook_receive(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(default=None, alias="X-Hub-Signature-256"),
) -> Dict[str, str]:
    raw = await request.body()
    if not verify_meta_signature(raw, x_hub_signature_256, settings.meta_app_secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()

   
    _ = payload
    return {"received": "true"}



# REST API para enviar mensajes

class SendTextIn(BaseModel):
    to: str = Field(..., description="Número destino en formato internacional, ej: 51999999999")
    body: str


class SendFlowIn(BaseModel):
    to: str
    flow_token: str = Field(..., description="Flow token generado/gestionado por tu integración")
    flow_id: Optional[str] = Field(default=None, description="Opcional: ID del Flow")
    flow_action: str = Field(default="navigate", description="Acción del flow (según configuración)")
    flow_action_payload: Optional[Dict[str, Any]] = None


@app.post("/api/send-text")
async def api_send_text(data: SendTextIn) -> Dict[str, Any]:
    client = WhatsAppClient()
    return await client.send_text(to=data.to, body=data.body)


@app.post("/api/send-flow")
async def api_send_flow(data: SendFlowIn) -> Dict[str, Any]:
    client = WhatsAppClient()
    return await client.send_flow(
        to=data.to,
        flow_token=data.flow_token,
        flow_id=data.flow_id,
        flow_action=data.flow_action,
        flow_action_payload=data.flow_action_payload,
    )

