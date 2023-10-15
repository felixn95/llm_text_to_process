import json

# Helper class for activity information, used to store the information during the request chains
class Activity:
    def __init__(self, id, label, actor_label, actor_id):
        self.id = id
        self.label = label
        self.actor_label = actor_label
        self.actor_id = actor_id

    def to_json(self):
        return json.dumps(self.__dict__)

class Activities:
    def __init__(self):
        self.activities = []

    def add_activity(self, activity):
        self.activities.append(activity)

    def to_json(self):
        return json.dumps([activity.__dict__ for activity in self.activities])
    
    # Map into actitvities object after received actor labels
    def from_label_json(self, json_str):
        data = json.loads(json_str)
        counter = 1
        for item in data["Activities"]:
            activity = Activity(f"T{counter}", item["activity-label"], item["actor-label"], item["actor-id"])
            self.add_activity(activity)
            counter += 1
        return self
    
    # filter for workflow request (to not overload context with information)
    def to_filtered_json(self):
        filtered_activities = [{"id": activity.id, "label": activity.label} for activity in self.activities]
        return json.dumps({"Activities": filtered_activities})
    
    

