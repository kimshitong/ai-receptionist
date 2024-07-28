from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather

app = FastAPI()


@app.post("/answer_call", response_class=PlainTextResponse)
async def answer_call():
    response = VoiceResponse()
    gather = Gather(input="speech", action="/transcribe_speech", method="POST", timeout=5)
    gather.say("Please say something after the beep.", voice="alice")
    response.append(gather)
    response.say("We did not receive any input. Goodbye!", voice="alice")
    return str(response)


@app.post("/transcribe_speech", response_class=PlainTextResponse)
async def transcribe_speech(request: Request):
    form = await request.form()
    speech_result = form.get("SpeechResult")
    print("Transcribed Text: ", speech_result)
    response = VoiceResponse()
    response.say(f"You said: {speech_result}", voice="alice")
    response.say("Goodbye!", voice="alice")
    return str(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
