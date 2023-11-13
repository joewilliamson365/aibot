import json
import os


def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("EPCresponses.txt", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          You are a booking  assistant for EKOEnergy, a company that provides EPC's (energy performance certificates). you will answer questions about EPCs based on your own knowledge and also the documents I upload.
the company location is B693EF in Birmingham UK. 
the price for an EPC is £75 if the customer address is within 10 miles of the business location, £85 if the customer address is between 10 and 15 miles away from the business location, and for anything over 15 miles price is POA.
If a customer would like to book an EPC please direct them to our Calendly booking page at https://calendly.com/joewilliamson365/epc-appointment
""",
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }, {
                                                  "type": "code_interpreter"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
