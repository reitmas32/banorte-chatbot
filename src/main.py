from openai import OpenAI

client = OpenAI()

audio_file= open("../AwACAgEAAxkBAAOVZwsRww97kDbdCtO82Zei_LJI_HAAAl4GAAJvpllEMpqmB_zrF0o2BA.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)
print(transcription.text)
