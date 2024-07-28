from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse

app = FastAPI()

@app.post("/answer_call", response_class=PlainTextResponse)
async def answer_call():
    response = VoiceResponse()
    response.say("Hello, this is a call from your FastAPI server.", voice="alice")
    response.pause(length=2)
    response.say("Goodbye!", voice="alice")
    return str(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
