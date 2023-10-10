import streamlit as st
from PIL import Image
import WorkflowManager
import random
import os

# Streamlit code
st.title('Text to process playground')

user_input = st.text_area('Enter some plain process description here. Please take care to use a straightforward and clear process with short sentences. :', 'Type Here')

col1, col2 = st.columns(2)

if col2.button('Clear Input'):
    st.rerun() # TODO to be improved

if col1.button('Extract workflow'):
    
    ### extract workflow model and activities labeled with actors
    manager = WorkflowManager.WorkflowManager()

    image_path = f"generated_processes/process-{random.randint(100, 999)}.png"
    
    workflow_modelJson, activities_mapped = manager.create_workflow_model(user_input, image_path, reset_state=True)

    if os.path.exists(image_path):
        # Display the image
        st.image(image_path, caption='Your Process', use_column_width=True)

    # Display the workflow as json below the image
    st.json(workflow_modelJson)
