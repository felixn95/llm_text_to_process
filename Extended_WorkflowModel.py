from Workflow_Model import WorkflowModel
from Workflow_Model import Node
from Workflow_Model import Task


class Extended_WorkflowModel(WorkflowModel):
    def __init__(self, wf_model):
        self.__dict__ = wf_model.__dict__.copy()

    def add_actor_info_to_tasks(self, activities_obj):
    # Assuming activities_obj.activities contains the list of Activity objects
        actor_info_map = {
            activity.id: {
                "actor_id": activity.actor_id,
                "actor_label": activity.actor_label
            }
            for activity in activities_obj.activities
        }

        for task in self.tasks:
            if task.id in actor_info_map:
                task.actor_id = actor_info_map[task.id]['actor_id']
                task.actor_label = actor_info_map[task.id]['actor_label']


# Add actor_id and actor_label to the Task class as optional attributes
Task.__init__ = (
    lambda self, id, label, successor, predecessor, actor_id=None, actor_label=None: (
        Node.__init__(self, id),
        setattr(self, "label", label),
        setattr(self, "successor", successor),
        setattr(self, "predecessor", predecessor),
        setattr(self, "actor_id", actor_id),
        setattr(self, "actor_label", actor_label),
    )
)
