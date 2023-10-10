import Activity
import Actiticy_Extraction
import Actors_Extraction
import Workflow_Extraction
import Process_Map_Creator
import json

# E2E request chains and json processing to extract workflow model 
# from plain processtext

class WorkflowManager:
    def __init__(self):
        pass

    def create_workflow_model(self, process, image_path, reset_state=False):
        if reset_state:
            # Initialize variables if reset_state is True
            activities_labeled = None
            is_valid = False
            act_actors_labeled = None
            activities_mapped = None
            workflowAsText = None
            workflow_model_dict = None

        max_retries = 3
        retries = 0

        while retries < max_retries:
            # Extract activities from process text
            activities_labeled = Actiticy_Extraction.extract_activities(process)

            # Validate the extracted activities
            is_valid = Actiticy_Extraction.is_valid_response(activities_labeled)

            if is_valid:
                break
            
            retries += 1
        
        if not is_valid:
            return "JsonError - please be more specific in your process description and follow the recommendations."

        # Assign actors to extracted activities
        act_actors_labeled = Actors_Extraction.assign_actors(process, activities_labeled)

        # Create an Activities class object and map extracted data
        activities_obj = Activity.Activities()
        activities_mapped = activities_obj.from_label_json(act_actors_labeled)

        # Create workflow request and map the response into a WorkflowModel
        workflowAsText = Workflow_Extraction.extract_workflow_openai(process, activities_mapped.to_json())

        ## transform json string to dict, currently it is a string in json format
        try:
            workflow_model_dict = json.loads(workflowAsText)
        except json.JSONDecodeError:
            workflow_model_dict = Workflow_Extraction.extract_json_from_string(workflowAsText)

        ## save bpmn visualization if successful
        try:
            Process_Map_Creator.generate_process_map(workflow_model_dict, image_path)
        except Exception as e:
            print(f"Error generating process map: {e}")
        
        return workflowAsText, activities_mapped
