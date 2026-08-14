from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
def AI_Response():
    pass
df = pd.read_csv("weather_last_30_days.csv")
messagebyuser=df.to_string()

prompt = f"""
You are a weather data analyst.

Analyze the following weather data from the last 30 days.

Weather data:
{messagebyuser}


"""
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
#   api_key = os.environ["API_KEY"],
    api_key=os.getenv("API_KEY")
)

completion = client.chat.completions.create(
  model="nvidia/nemotron-3-super-120b-a12b",
  messages=[
      {
          
    "role":"user",
    "content":prompt
       
       }],
  temperature=1,
  top_p=0.95,
  max_tokens=16384,
  extra_body={"chat_template_kwargs":{"enable_thinking":True},"reasoning_budget":16384},
  stream=True
)



for chunk in completion:
  if not chunk.choices:
    continue
  reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
  if reasoning:
    print(reasoning, end="")
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")