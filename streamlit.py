import streamlit as st
from PIL import Image
import WorkflowManager
import random
import os

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

If possible, a process diagram will be created and displayed. 

**Limitations**: 
Currently the approach only supports small and straightforward processes. Including Activities (Tasks), Actors (Lanes), and Gateways (just exclusive ones ATM).
Sentences should be short and written in present tense - "Actor A is performing task B". Examplary process text to orientate which "complexity" could work: 
*A Customer places an order. Then the Warehouse checks the payment of the order. If the payment is successful, the warehouse ships the order. Otherwise the warehouse rejects the order.*
""")

# Place other elements in the second column (col2)
with coly:
    user_input = st.text_area('Enter some plain process description here:', 'Type Here')
    model_choice = st.selectbox('Choose a Model:', ['llama2-70b-chat', 'gpt-3.5-turbo'])
    # ... rest of your code
    col1, col2 = st.columns(2)

    if col2.button('Clear Input'):
        st.rerun() # TODO to be improved

    if col1.button('Extract workflow'):

        print (model_choice)
        ### extract workflow model and activities labeled with actors
        manager = WorkflowManager.WorkflowManager()

        image_path = f"generated_processes/process-{random.randint(100, 999)}.png"
        
        WorkflowModelJson, activities_mapped = manager.create_WorkflowModel(user_input, image_path, model_choice=model_choice, reset_state=True)

        if os.path.exists(image_path):
            # Display the image
            st.image(image_path, caption='Your Process', use_column_width=True)

        with colx:
        # Display the workflow as json below the image
            st.json(WorkflowModelJson)

        # Display the activities as json below the image
            st.write("Activities:")
            st.json(activities_mapped.to_json())

