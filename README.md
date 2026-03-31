# WhatsApp Flows (REST + Webhooks) — FastAPI

Proyecto base para integrar **WhatsApp Cloud API** con:
- **Webhook**: verificación `GET /webhook` y recepción `POST /webhook`
- **API REST**: endpoints para **enviar texto** y **disparar un Flow**

## Requisitos
- Python 3.10+ (recomendado 3.11/3.12)

## Configuración
1) Crea tu `.env` a partir del ejemplo:

- Copia `.env.example` a `.env` y completa:
  - `WHATSAPP_PHONE_NUMBER_ID`
  - `WHATSAPP_ACCESS_TOKEN`
  - `WEBHOOK_VERIFY_TOKEN`
  - (opcional) `META_APP_SECRET`

## Instalación

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Salud:
- `GET http://localhost:8000/health`

Docs Swagger:
- `GET http://localhost:8000/docs`

## Webhook (Meta)

Configura en el panel de Meta la URL pública:
- `https://TU-DOMINIO/webhook`

Y el **Verify Token** igual a `WEBHOOK_VERIFY_TOKEN`.

Meta hará:
- `GET /webhook?hub.mode=subscribe&hub.challenge=...&hub.verify_token=...`
- `POST /webhook` con eventos.

## Enviar un texto (REST)

```bash
curl -X POST http://localhost:8000/api/send-text ^
  -H "Content-Type: application/json" ^
  -d "{\"to\":\"51999999999\",\"body\":\"Hola desde API\"}"
```

## Disparar un Flow (REST)

```bash
curl -X POST http://localhost:8000/api/send-flow ^
  -H "Content-Type: application/json" ^
  -d "{\"to\":\"51999999999\",\"flow_token\":\"TU_FLOW_TOKEN\",\"flow_id\":null,\"flow_action\":\"navigate\",\"flow_action_payload\":null}"
```

## Siguiente paso (tu lógica)
En `POST /webhook` (archivo `main.py`) agrega el parseo de `entry/changes` para:
- detectar mensajes entrantes
- responder automáticamente
- abrir un Flow según palabra clave/estado de usuario

