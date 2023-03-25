import openai

import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")

text = """The COVID-19 pandemic has had a major impact on the world, causing widespread illness and death, as well as economic and social disruption. As of March 2021, there have been over 120 million confirmed cases of COVID-19 and over 2.6 million deaths worldwide. The pandemic has also led to school closures, job losses, and mental health issues for many people.
Despite the challenges posed by the pandemic, there has been progress in the development and distribution of COVID-19 vaccines. Several vaccines have been approved for emergency use, and many countries are working to vaccinate their populations as quickly as possible. However, there are concerns about vaccine distribution and vaccine hesitancy, particularly in low- and middle-income countries.
Overall, the COVID-19 pandemic has highlighted the importance of public health preparedness and international cooperation in responding to global health crises."""
word_count = len(text.split())
print(f"Input Words:{word_count}")
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Summarize the following text:\n\n" + text,
        temperature=0.5,
        max_tokens = int(word_count*0.75),
        n=1,
        stop=None,
    )

    summary = response.choices[0].text.strip()
    return summary

summary = summarize_text(text)
print(summary)
print(f"Summary words:{len(summary.split())}")