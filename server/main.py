from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketState

class WebsocketManager:
    def __init__(self):
        self.actives = []
    
    async def connect(self, websocket:WebSocket):
        if websocket not in self.actives:
            self.actives.append(websocket)
        websocket.accept()
    
    async def disconnect(self, websocket:WebSocket):
        if websocket not in self.actives:
            raise ValueError(f"{websocket} not in actives.")
        self.actives.remove(websocket)
    
    async def send_text(self, websocket:WebSocket, text:str):
        if websocket not in self.actives:
            raise ValueError(f"Send error: {websocket} not in actives.")
        websocket.send_text(data=text)

    async def broadcast(self, text:str):
        for conn in self.actives:
            conn.send_text(text)        

app = FastAPI()
websocket_manager = WebsocketManager()

@app.websocket("/ws/chat")
async def chat(websocket:WebSocket):
    websocket_manager.connect(websocket)
    while websocket.client_state == WebSocketState.CONNECTED:
        bytes_data:bytes = await websocket.receive_bytes()
        