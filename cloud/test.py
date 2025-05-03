from google import genai
from google.genai import types
import base64

def generate():
  client = genai.Client(
      vertexai=True,
      project="spellpop",
      location="us-central1",
  )

  msg1_text1 = types.Part.from_text(text="""Introduction[edit]
Apophenia can be considered a commonplace effect of brain function. Taken to an extreme, however, it can be a symptom of psychiatric dysfunction, for example, as a symptom in schizophrenia,[7] where a patient sees hostile patterns (for example, a conspiracy to persecute them) in ordinary actions.
Apophenia is also typical of conspiracy theories, where coincidences may be woven together into an apparent plot.[8]
Examples[edit]Pareidolia[edit]
Main article: Pareidolia


\"The Organ Player\": an example of pareidolia in Neptune's Grotto, Sardinia
Pareidolia is a type of apophenia involving the perception of images or sounds in random stimuli.
A common example is the perception of a face within an inanimate object—the headlights and grill of an automobile may appear to be \"grinning\". People around the world see the \"Man in the Moon\".[9] People sometimes see the face of a religious figure in a piece of toast or in the grain of a piece of wood. There is strong evidence that psychedelic drugs tend to induce or enhance pareidolia.[10]

Pareidolia usually occurs as a result of the fusiform face area—which is the part of the human brain responsible for seeing faces—mistakenly interpreting an object, shape or configuration with some kind of perceived \"face-like\" features as being a face.""")

  model = "gemini-2.0-flash-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        msg1_text1
      ]
    ),
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    print(chunk.text, end="")

generate()
