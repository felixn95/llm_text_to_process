from processpiper import ProcessMap, ActivityType, EventType, GatewayType

## Deterministic try to create a visualizable process diagram with processpiper (no AI/LLM involved)

def generate_process_map(process_structure, path):
    process_structure = process_structure['WorkflowModel']
    with ProcessMap("Text to Process Playground", colour_theme="BLUEMOUNTAIN") as my_process_map:
        with my_process_map.add_pool("Company") as pool:
            
            # Create lanes for each unique actor
            lanes = {}
            for actor in set(task['actor_id'] for task in process_structure['tasks']):
                actor_label = next(task['actor_label'] for task in process_structure['tasks'] if task['actor_id'] == actor)
                lanes[actor] = pool.add_lane(actor_label)
            
            # Create tasks in their respective lanes
            tasks = {}
            for task in process_structure['tasks']:
                tasks[task['id']] = lanes[task['actor_id']].add_element(task['label'], ActivityType.TASK)
            
            # Create gateways in their respective lanes
            gateways = {}
            for gateway in process_structure['gateways']:
                gate_type = GatewayType.EXCLUSIVE if "XOR" in gateway['type'] else GatewayType.INCLUSIVE
                condition = gateway.get('condition', '')  # Use .get() method to handle missing keys
                gateways[gateway['id']] = lanes[gateway['actor_id']].add_element(condition, gate_type)
            
            # Connect tasks and gateways
            for task in process_structure['tasks']:
                if task['successor'] != process_structure['end_node']['id']:
                    tasks[task['id']].connect(tasks[task['successor']] if task['successor'] in tasks else gateways[task['successor']])

            for gateway in process_structure['gateways']:
                current_gateway = gateways[gateway['id']]
                
                if gateway['type'] == "XOR-Split":
                    
                    # Connect to successor_true
                    if gateway['successor_true']:
                        successor_element = tasks if gateway['successor_true'] in tasks else gateways
                        current_gateway.connect(successor_element[gateway['successor_true']])
                    
                    # Connect to successor_false
                    if gateway['successor_false']:
                        successor_element = tasks if gateway['successor_false'] in tasks else gateways
                        current_gateway.connect(successor_element[gateway['successor_false']])
                        
                # else:  # XOR-Join -> outcommented for now since connections already happened in connect tasks and gateways
                    
                #     # Connect from predecessor_true
                #     if gateway['predecessor_true']:
                #         predecessor_element = tasks if gateway['predecessor_true'] in tasks else gateways
                #         predecessor_element[gateway['predecessor_true']].connect(current_gateway)
                    
                #     # Connect from predecessor_false
                #     if gateway['predecessor_false']:
                #         predecessor_element = tasks if gateway['predecessor_false'] in tasks else gateways
                #         predecessor_element[gateway['predecessor_false']].connect(current_gateway)

            
            # Connect start and end nodes
            start = lanes[process_structure['start_node']['actor_id']].add_element('Start', EventType.START)

            # For the start node, find the task or gateway that has the start node's ID as its predecessor
            next_element_after_start = None
            for task in process_structure['tasks']:
                if task['predecessor'] == process_structure['start_node']['id']:
                    next_element_after_start = tasks.get(task['id'])
                    break

            if next_element_after_start:
                start.connect(next_element_after_start)

            end = lanes[process_structure['end_node']['actor_id']].add_element('End', EventType.END)

            # For the end node, find the task or gateway with the end node's ID as its successor
            previous_element_before_end = None
            for task in process_structure['tasks']:
                if task['successor'] == process_structure['end_node']['id']:
                    previous_element_before_end = tasks[task['id']]
                    break
            if not previous_element_before_end:
                for gateway in process_structure['gateways']:
                    if gateway.get('successor') and gateway['successor'] == process_structure['end_node']['id']:
                        previous_element_before_end = gateways[gateway['id']]
                        break

            
            previous_element_before_end.connect(end)

        my_process_map.draw()
        my_process_map.save(path)