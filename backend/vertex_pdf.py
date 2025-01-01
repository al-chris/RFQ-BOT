import vertexai

from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update porject_id and location
vertexai.init(project="rfq-bot-434420", location="us-central1")

model = GenerativeModel("gemini-1.5-flash-001")

prompt = """
You are a very professional document summarization specialist.
Please summarize the given document.
"""

pdf_file = Part.from_uri(
    uri="gs://vertex-ai-samples-data/document-ai/loan-agreement.pdf",
    mime_type="application/pdf",
)

contents = [pdf_file, prompt]

response = model.generate_content(contents)
print(response.text)