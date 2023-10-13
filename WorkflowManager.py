import Activity
import ActiticyExtraction
import ActorsExtraction
import WorkflowExtraction
import Process_Map_Creator
import json

# E2E request chains and json processing to extract workflow model 
# from plain processtext

class WorkflowManager:
    def __init__(self):
        pass

    def create_WorkflowModel(self, process, image_path, model_choice, reset_state=False):
        if reset_state:
            # Initialize variables if reset_state is True
            activities_labeled = None
            is_valid = False
            act_actors_labeled = None
            activities_mapped = None
            workflowAsText = None
            WorkflowModel_dict = None

        max_retries = 3
        retries = 0

        while retries < max_retries:
            # Extract activities from process text
            activities_labeled = ActiticyExtraction.extract_activities(process)

            # Validate the extracted activities
            is_valid = ActiticyExtraction.is_valid_response(activities_labeled)

            if is_valid:
                break
            
            retries += 1
        
        if not is_valid:
            return "JsonError - please be more specific in your process description and follow the recommendations."

        # Assign actors to extracted activities
        act_actors_labeled = ActorsExtraction.assign_actors(process, activities_labeled)

        # Create an Activities class object and map extracted data
        activities_obj = Activity.Activities()
        activities_mapped = activities_obj.from_label_json(act_actors_labeled)

        # Choose the model to use
        if model_choice == 'gpt-3.5-turbo':
            # Create workflow request and map the response into a WorkflowModel
            workflowAsText = WorkflowExtraction.extract_workflow(process, activities_mapped.to_json())
        elif model_choice == 'llama2-70b-chat':
            workflowAsText = WorkflowExtraction.extract_workflow_openai(process, activities_mapped.to_json())

        ## transform json string to dict, currently it is a string in json format
        try:
            WorkflowModel_dict = json.loads(workflowAsText)
        except json.JSONDecodeError:
            WorkflowModel_dict = WorkflowExtraction.extract_json_from_string(workflowAsText)

        ## save bpmn visualization if successful
        try:
            Process_Map_Creator.generate_process_map(WorkflowModel_dict, image_path)
        except Exception as e:
            print(f"Error generating process map: {e}")
        
        return workflowAsText, activities_mapped
