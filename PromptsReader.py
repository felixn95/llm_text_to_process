from enum import Enum

class TextFiles(Enum):
    WORKFLOW_PREPROMPT = "prompts/workflow_preprompt.txt"
    WORKFLOW_POSTPROMPT = "prompts/workflow_postprompt.txt"
    WORKFLOW_SYSTEMPROMPT = "prompts/workflow_systemprompt.txt"

    ACTIVITIES_PREPROMPT = "prompts/activities_preprompt.txt"
    ACTIVITIES_POSTPROMPT = "prompts/activities_postprompt.txt"
    ACTIVITIES_SYSTEMPROMPT = "prompts/activities_systemprompt.txt"

    ACTORS_PREPROMPT = "prompts/actors_preprompt.txt"
    ACTORS_POSTPROMPT = "prompts/actors_postprompt.txt"
    ACTORS_SYSTEMPROMPT = "prompts/actors_systemprompt.txt"

    PROCESS_1 = "prompts/process_1.txt"

    act_json = "prompts/act_json.txt"
    workflow_example = "prompts/workflow_example.txt"

# Function to return the contents of the text file as string
def read_text_file(file_path):
    with open(file_path, 'r') as text_file:
        return text_file.read()