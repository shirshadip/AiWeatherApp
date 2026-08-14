from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["AI_API_KEY"]
)



def AI_Response(prompt, system_prompt):

    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=1,
        top_p=0.95,
        max_tokens=16384,

        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": True
            },
            "reasoning_budget": 16384
        },

        stream=True
    )

    for chunk in completion:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        reasoning = getattr(delta, "reasoning_content", None)

        if reasoning:
            yield {
                "type": "reasoning",
                "content": reasoning
            }

        if delta.content is not None:
            yield {
                "type": "content",
                "content": delta.content
            }
            
            
            
if __name__=="__main__":
            
  system_prompt = """
  You are an expert weather data analyst.
  Analyze weather datasets accurately.
  Never fabricate missing information.
  """

  df = pd.read_csv("weather_last_30_days.csv")
  messagebyuser = df.to_string()

  prompt = f"""
  You are a weather data analyst.

  Analyze the following weather data from the last 30 days.

  Weather data:
  {messagebyuser}

  Provide a clear and useful analysis.
  """

  # Consume the stream
  for chunk in AI_Response( prompt , system_prompt):
      if chunk["type"] == "reasoning":
          print(chunk["content"], end="", flush=True)

      elif chunk["type"] == "content":
          print(chunk["content"], end="", flush=True)