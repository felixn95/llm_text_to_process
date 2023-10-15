import Activity
import ActiticyExtraction
import ActorsExtraction
import WorkflowExtraction
import Process_Map_Creator
import json

class WorkflowManager:
    def __init__(self):
        pass

    def extract_activities(self, process, max_retries=3, model_choice="gpt-3.5-turbo"):
        activities_labeled = None
        is_valid = False

        for _ in range(max_retries):
            if model_choice == ModelChoice.GPT_3_5_TURBO:
                activities_labeled = ActiticyExtraction.extract_activities_openai(process)
            elif model_choice == ModelChoice.LLAMA2_70B_CHAT:
                activities_labeled = ActiticyExtraction.extract_activities_llama2(process)
            is_valid = ActiticyExtraction.is_valid_response(activities_labeled)

            if is_valid:
                break

        return activities_labeled, is_valid

    def assign_actors(self, process, activities_labeled, model_choice="gpt-3.5-turbo"):
        if model_choice == ModelChoice.GPT_3_5_TURBO:
            act_actors_labeled = ActorsExtraction.assign_actors_openai(process, activities_labeled)
        elif model_choice == ModelChoice.LLAMA2_70B_CHAT:
            act_actors_labeled = ActorsExtraction.assign_actors_llama2(process, activities_labeled)
        return act_actors_labeled

    def create_workflow_model(self, process, image_path, model_choice, reset_state=False):
        if reset_state:
            activities_labeled = None
            is_valid = False
            act_actors_labeled = None
            activities_mapped = None
            workflowAsText = None
            WorkflowModel_dict = None

        activities_labeled, is_valid = self.extract_activities_llama2(process, model_choice=model_choice)

        if not is_valid:
            return "JsonError - please be more specific in your process description and follow the recommendations."

        act_actors_labeled = self.assign_actors(process, activities_labeled, model_choice=model_choice)

        activities_obj = Activity.Activities()
        activities_mapped = activities_obj.from_label_json(act_actors_labeled)

        if model_choice == ModelChoice.GPT_3_5_TURBO:
            workflowAsText = WorkflowExtraction.extract_workflow_openai(process, activities_mapped.to_json())
        elif model_choice == ModelChoice.LLAMA2_70B_CHAT:
            workflowAsText = WorkflowExtraction.extract_workflow_llama2(process, activities_mapped.to_json())

        try:
            WorkflowModel_dict = json.loads(workflowAsText)
        except json.JSONDecodeError:
            WorkflowModel_dict = WorkflowExtraction.extract_json_from_string(workflowAsText)

        try:
            Process_Map_Creator.generate_process_map(WorkflowModel_dict, image_path)
        except Exception as e:
            print(f"Error generating process map: {e}")

        return workflowAsText, activities_mapped
    
    def create_workflow_with_input(self, activities_mapped, process, model_choice="gpt-3.5-turbo", image_path="generated_processes/process-XXX.png"):
        if model_choice == ModelChoice.GPT_3_5_TURBO:
            workflowAsText = WorkflowExtraction.extract_workflow_openai(process, activities_mapped)
        elif model_choice == ModelChoice.LLAMA2_70B_CHAT:
            workflowAsText = WorkflowExtraction.extract_workflow_llama2(process, activities_mapped)

        try:
            WorkflowModel_dict = json.loads(workflowAsText)
        except json.JSONDecodeError:
            WorkflowModel_dict = WorkflowExtraction.extract_json_from_string(workflowAsText)
        
        try:
            Process_Map_Creator.generate_process_map(WorkflowModel_dict, image_path)
        except Exception as e:
            print(f"Process Image Generation unfortunately failed: {e}")

        return workflowAsText
    
class ModelChoice:
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    LLAMA2_70B_CHAT = "llama2-70b-chat"
