import streamlit as st
from PIL import Image
import random
import os
from WorkflowManager import WorkflowManager, ModelChoice
import Activity

# Use the full width of the page
st.set_page_config(layout='wide')

st.title('Text to process playground')


# Display the instructions and limitations
colx, coly = st.columns([1, 2])  # Create a 1:2 ratio for the columns

# Place markdown in the first column (col1)
with colx:
    st.markdown(""" 
After inserting a process text, the app tries to extract the workflow (as defined in WorkflowModel.py).

Since the extraction happens in 3 steps (Actitvites->Actors->Workflow), it takes ~60 seconds to complete.

**One the left side, the extracted Actitvites with assigned Actors are displayed.**
                                 
**If possible, a workflow model will be displayed below the input field.**
                
Also, a diagram will be created and displayed if possible. 

**Limitations**: 
Currently the approach only supports small and straightforward processes. Including Activities (Tasks), Actors (Lanes), and Gateways (just exclusive ones ATM).
Sentences should be short and written in present tense - "Actor A is performing task B". Examplary process text to orientate which "complexity" could work: 
*A Customer places an order. Then the Warehouse checks the payment of the order. If the payment is successful, the warehouse ships the order. Otherwise the warehouse rejects the order.*
""")

# Place other elements in the second column (col2)
with coly:
    user_input = st.text_area('Enter some plain process description here:', 'Type Here')
    model_choice = st.selectbox('Choose a Model:', [ModelChoice.GPT_3_5_TURBO, ModelChoice.LLAMA2_70B_CHAT])
    # ... rest of your code
    col1, col2 = st.columns(2)

    if col2.button('Clear Input'):
        st.rerun() # TODO to be improved

    if col1.button('Extract workflow'):

        print (model_choice)
        ### extract workflow model and activities labeled with actors
        manager = WorkflowManager()

        image_path = f"generated_processes/process-{random.randint(100, 999)}.png"
        
        activities_labeled, is_valid = manager.extract_activities(user_input, model_choice=model_choice)

        act_actors_labeled = manager.assign_actors(user_input, activities_labeled, model_choice=model_choice)

        # Check the results and already display the activities with assigned actors
        if is_valid:
            with colx:
                st.write("Activities with assigned actors:")
                st.json(act_actors_labeled)
        else:
            st.write("JsonError - please be more specific in your process description and follow the recommendations.")

        if is_valid:
            activities_obj = Activity.Activities()
            activities_mapped = activities_obj.from_label_json(act_actors_labeled)
            workflow = manager.create_workflow_with_input(user_input, activities_mapped.to_json(), model_choice=model_choice, image_path=image_path)

        # Display the image if creation was successful
        if os.path.exists(image_path):
            st.image(image_path, caption='Your Process', use_column_width=True)

        with coly:
        # Display the workflow as json below (should also be displayed if no image was created, but a workflow was extracted)
            st.json(workflow)

