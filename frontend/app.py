import streamlit as st
from st_audiorec import st_audiorec
import base64
import asyncio
import websockets
import json

st.set_page_config(page_title="Agentic Interview Bot")

st.title("🎙️ Agentic AI Interviewer")

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

# record audio
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")
    # base64 encode the raw wav
    b64_audio = base64.b64encode(wav_audio_data).decode("utf-8")

    async def talk_to_backend(audio_data):
        uri = "ws://backend:8000/interview/ws"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"audio": audio_data}))
            reply = await websocket.recv()
            reply_data = json.loads(reply)

            reply_text = reply_data.get("reply", "")
            reply_audio_b64 = reply_data.get("reply_audio", "")
            if reply_audio_b64:
                audio_bytes = base64.b64decode(reply_audio_b64)
                st.audio(audio_bytes, format="audio/mpeg")

            # show text
            st.session_state["conversation"].append({
                "question": reply_text
            })
            st.write(f"**Interviewer:** {reply_text}")

    asyncio.run(talk_to_backend(b64_audio))
