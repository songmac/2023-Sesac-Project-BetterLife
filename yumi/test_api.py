import os
from dotenv import load_dotenv
import panel as pn
import time
import openai
import asyncio

# Load .env
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

# Set API key
openai.api_key = api_key

async def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, get_completion_sync, messages, model, temperature, max_tokens)
    return response

def get_completion_sync(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=["종료", "나가기"]
    )
    return response.choices[0].message.content

# Boost chatbot response speed with asynchronous tasks
async def interact_with_model(context):
    response = await get_completion_from_messages(context)
    return response

# Context for OpenAI training
context = [
    {'role': 'assistant',
     'content': """
      You are a chatbot designed to recommend suitable exercise programs to users.
      Begin by greeting the user and asking two specific questions.
      Only collect responses to the designated questions.
      Once all questions have been answered, conclude with a farewell message.

      Ask the following questions to the user in order:

      1. What is your age?
      2. Choose your exercise goal. (1: Physical training, 2: Cardiovascular training)
    """
    }
]

# Display chatbot questions and user responses using the panel library
async def collect_messages(_):
    start_time = time.time()
    prompt = inp.value_input
    inp.value = ''  # Reset user input
    # Add user content to context
    context.append({'role': 'user', 'content': f"{prompt}"})
    # Get OpenAI response
    response = await interact_with_model(context)
    end_time = time.time()
    context.append({'role': 'system', 'content': f"{response}"})
    print("User input: ", prompt)
    # Display on the panel
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('ExerciseCoach:', pn.pane.Markdown(response, width=600, styles={'background-color': '#f0fcd4'})))
    print("Elapsed time: ", end_time - start_time)
    return pn.Column(*panels)

# Create chatbot interface
pn.extension()

panels = []

# User input text field
inp = pn.widgets.TextInput(value="Hello!", placeholder='Type here')
# Input button
button_conversation = pn.widgets.Button(name="Submit")
# Display conversation
interactive_conversation = pn.bind(collect_messages, button_conversation)
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

# Show dashboard
dashboard.show()
