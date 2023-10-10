# LLM_text_to_process

Prototypical approach to generate a process model workflow and diagram from a plain process description. 

The workflow extractions happen in three sequential steps (Activities -> Actors -> Workflow) using the llama2 model (https://huggingface.co/meta-llama/Llama-2-70b) and/or gpt-3.5-turbo from OPENAI (https://platform.openai.com/docs/models/gpt-3-5). 

The visualization (workflow -> model) is a deterministic approach using the process piper library to draw BPMN diagrams (https://github.com/csgoh/processpiper/). 

After requirements are installed, the app can be started (location is the root folder):

```
streamlit run streamlit.py
```

After inserting a process text, the app tries to extract the workflow (as defined in Workflow_Model.py)

Also, if possible, a process diagram will be created and displayed. 

NOTE: Place your Replicate and OpenAI API-Tokens in the .env file of the root folder. 

Limitations: 
Currently, the approach only supports small and straightforward processes. Including Activities (Tasks), Actors (Lanes), and Gateways (just exclusive ones ATM).
The sentences should be short and written in present tenses - "Actor A is performing task B". 

Exemplary process text to orientate which "complexity" might work: 
A Customer places an order. Then the Warehouse checks the payment of the order. If the payment is successful, the warehouse ships the order. Otherwise the warehouse rejects the order.
