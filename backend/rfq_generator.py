
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_rfq_table(email_content):
    # Initialize the model
    model = genai.GenerativeModel('gemini-pro')

    # Create the prompt
    prompt = f"""
    # RFQ Information Extraction Agent

You are an AI agent designed to extract Request for Quotation (RFQ) information from email content. Your task is to analyze the input email and extract specific RFQ details if present.

## Instructions:

1. Read the input email content carefully.
2. Identify if the email contains RFQ information.
3. If RFQ information is present:
   - Extract the following details for each item:
     - Item name
     - Description
     - Quantity
     - Unit
   - Compile the extracted information into a list of dictionaries, where each dictionary represents one item and contains the above fields.
   - Ensure the output can be easily converted into a pandas DataFrame.

4. If no RFQ information is found:
   - Return an empty list of dictionaries that can be converted into an empty pandas DataFrame.

## Output Format:

- For emails with RFQ information:
  ```python
  [
    {{
      "Item_name": "item name",
      "Description": "item description",
      "Quantity": "quantity",
      "Unit": "unit"
    }},
    # Additional items...
  ]
  ```

- For emails without RFQ information:
  ```python
  []
  ```

## Notes:
- Be thorough in your analysis to ensure all relevant RFQ information is captured.
- If any required field is missing for an item, include the field in the dictionary with an empty value or "N/A" as appropriate.
- Maintain consistency in field names and data types across all extracted items.


    {email_content}
    """

    # Generate the response
    response = model.generate_content(prompt)

    return response.text
