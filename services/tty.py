from gtts import gTTS
import base64, io

def get_audio_html(text):
    fp = io.BytesIO()
    gTTS(text=text, lang='en').write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    return f'<audio autoplay src="data:audio/mp3;base64,{b64}">'