from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.agents.interview_agent import InterviewAgent
from app.utils.session import SessionManager
from app.utils.stt import transcribe_audio
from app.utils.tts import synthesize_speech

import base64

router = APIRouter(prefix="/interview")
agent = InterviewAgent()
session_mgr = SessionManager()

@router.websocket("/ws")
async def interview_ws(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket.client[1]
    state = session_mgr.init_session(session_id)

    try:
        while True:
            data = await websocket.receive_json()

            if "text" in data:
                text = data["text"]
            elif "audio" in data:
                audio_b64 = data["audio"]
                # decode base64
                audio_bytes = base64.b64decode(audio_b64)
                # save to file
                with open("temp.wav", "wb") as f:
                    f.write(audio_bytes)
                # transcribe
                text = transcribe_audio("temp.wav")
            else:
                text = ""

            reply, new_state = agent.process(text, state)
            state = new_state
            session_mgr.update_session(session_id, new_state)

            # TTS
            speech_b64 = synthesize_speech(reply)

            await websocket.send_json({
                "reply": reply,
                "reply_audio": speech_b64,
                "state": state
            })


    except WebSocketDisconnect:
        session_mgr.clear_session(session_id)
        print(f"Connection closed for {session_id}")
