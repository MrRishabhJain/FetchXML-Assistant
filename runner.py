import json
import time
from setup import create_client_and_assistant
import custom_tools

client, assistant_id = create_client_and_assistant("fetchXML.md", "tools.json")
status_map = {
    "in_progress": "Thinking...",
    "completed": "",
    "requires_action": "Using tools...",
    "queued": "Waiting...",
}
print()
user_name = "rishjain"
print(f"Hey @{user_name}! Fetch XML Assistant here. What are you looking for?")
print()
# Create a thread
thread = client.beta.threads.create()
while True:
    prompt = input(f"{user_name} >> ")
    print()
    # Add a user question to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    # Looping until the run completes or fails
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread.id)
            print(messages.data[0].content[0].text.value)
        
        elif run.status == 'requires_action':
            print(status_map[run.status])
            # The assistant requires calling some functions
            # and submit the tool outputs back to the run
            if run.required_action.type == 'submit_tool_outputs':
                tool_outputs = []
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.type == 'function':
                        args = json.loads(tool_call.function.arguments)
                        if tool_call.function.name == 'get_all_entity_names':
                            org_url = args["org_url"]
                            print("Searching across entities on", org_url)
                            output = custom_tools.get_all_entity_names(org_url)
                        
                        elif tool_call.function.name == 'get_entity_metadata':
                            org_url = args["org_url"]
                            entity_name = args["entity_name"]
                            print("Fetching metadata for:", entity_name)
                            output = custom_tools.get_entity_metadata(org_url, entity_name)
                            
                        elif tool_call.function.name == 'run_fetchxml_query':
                            fetch_xml_query = args["fetch_xml_query"]
                            org_url = args["org_url"]
                            print("Testing the generated query...")
                            output = custom_tools.run_fetchxml_query(fetch_xml_query, org_url)
                        
                        tool_outputs.append(
                            {
                                "tool_call_id": tool_call.id,
                                "output": output
                            }
                        )
                            
                
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        else:
            print(status_map[run.status])
        print()
