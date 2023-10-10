import json

### Classes for storing workflow informations to create a bpmn-diagram from it 

class Node:
    def __init__(self, id, actor_id=None, actor_label=None):
        self.id = id
        self.actor_id = actor_id
        self.actor_label = actor_label


class Task(Node):
    def __init__(self, id, label, successor, predecessor, actor_id=None, actor_label=None):
        super().__init__(id, actor_id, actor_label)
        self.label = label
        self.successor = successor
        self.predecessor = predecessor


class Gateway(Node):
    def __init__(
        self,
        type,
        id,
        condition=None,
        successor_true=None,
        successor_false=None,
        predecessor=None,
        predecessor_true=None,
        predecessor_false=None,
        successor=None,
        actor_id=None,
        actor_label=None,
    ):
        super().__init__(id, actor_id, actor_label)
        self.type = type
        self.condition = condition
        self.successor_true = successor_true
        self.successor_false = successor_false
        self.predecessor = predecessor
        self.predecessor_true = predecessor_true
        self.predecessor_false = predecessor_false
        self.successor = successor


class WorkflowModel:
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.tasks = []
        self.gateways = []

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        model = cls()

        workflow_data = json_dict.get("WorkflowModel", {})

        # Create start and end nodes
        start_data = workflow_data.get("start-node", {})
        model.start_node = Node(start_data.get("id"), start_data.get("actor_id"), start_data.get("actor_label"))
        
        end_data = workflow_data.get("end-node", {})
        model.end_node = Node(end_data.get("id"), end_data.get("actor_id"), end_data.get("actor_label"))

        # Create tasks
        for task_data in workflow_data.get("tasks", []):
            model.tasks.append(Task(
                task_data["id"],
                task_data["label"],
                task_data["successor"],
                task_data["predecessor"],
                task_data.get("actor_id"),
                task_data.get("actor_label")
            ))

        # Create gateways
        for gateway_data in workflow_data.get("gateways", []):
            model.gateways.append(Gateway(
                gateway_data["type"],
                gateway_data["id"],
                gateway_data.get("condition"),
                gateway_data.get("successor_true"),
                gateway_data.get("successor_false"),
                gateway_data.get("predecessor"),
                gateway_data.get("predecessor_true"),
                gateway_data.get("predecessor_false"),
                gateway_data.get("successor"),
                gateway_data.get("actor_id"),
                gateway_data.get("actor_label")
            ))

        return model

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
