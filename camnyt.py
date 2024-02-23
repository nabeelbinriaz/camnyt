import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
openai_api_key = os.environ.get("OPENAI_API_KEY")
def gpt(query):
  URL = "https://api.openai.com/v1/chat/completions"
  data='''
  Membership Features
  1)Kill the Ads:
  When you’re a member, the ads go away, giving you more open space to chat and watch.
  2) Gender Filter:
  Filter who you randomly connect to by gender. Get the exact experience you want.
  3) Intro Message:
  Introduce yourself, say hello or add any intro message you prefer and it will be sent each time you connect a new person
  4)VIP Badge:
  Being a verified member gives you more credibility with other CamNyt users.
  5) Gain Followers:
  Grow your social media following and reconnect with friends by adding your Instagram, Snap or Onlyfans id to send each time you connect to a new person.
  6) Private Chat:
  Private Chat is encrypted and unmoderated.
  7) Location Filter:
  Connect to random people in over 200 countries around the world with ease.
  8) Hide Your Location
  You can hide your location if you want to stay more private.
  9) 24/7 Live Support: 
  Access priority customer service via live chat with agents online 24 hours a day, 7 days a week


  Membership Details:
  1)6 Month:
  $14.99/month
  rebills every 6 months at $89.94
  2)1 Month:
  $19.99/Month
  rebills monthly at $19.99
  3)1 Week
  $7.99/week
  rebills weekly at $7.99
  '''
  payload = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "system","content": f"You are a user support bot providing answers for user query.\n\n Give your answers in context of follwoing data:\n\n{data}"},{"role": "user", "content":  f"user query:{query}."}],
  "temperature" : 0.8,
  "top_p":1.0,
  "n" : 1,
  "stream": False,
  "presence_penalty":0,
  "frequency_penalty":0,
  }

  headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {openai_api_key}"
  }

  response = requests.post(URL, headers=headers, json=payload, stream=False)
  res=response.json()
  subjects = res['choices'][0]['message']['content']
  return subjects

@app.post("/chat-bot/")
async def get_subjects(query: str = Form(...)):
  answer=gpt(query)
  return JSONResponse(content={"anwser": answer
                                 })
  
  
