import streamlit as st
import os
import re
import json
import argparse
import pandas as pd
from tqdm.auto import tqdm
from getpass import getpass 
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from utils.fastchat import FastChatAgent


def get_score_openai(idx, trajectory, messages):
    history = [f"User: {ds['content'].strip()}\n" if ds['role'] == 'user' else f"Agent: {ds['content'].strip()}\n" for ds in trajectory[:idx]]
    history = '\n'.join(history).strip()
    history = f"<history>{history}</history>"
    response = f"<response>{trajectory[idx]['content']}</response>"
    user = f"<user>{trajectory[idx+1]['content'] if idx < len(trajectory)-1 else '  '}</user>"
    
    human_message = [HumanMessage(content=\
    """
    History: {}

    Agent: {}
    User: {}
    """.format(history, response, user))]
    print(messages)
    print(human_message)
    output = model.predict_messages(messages + human_message).content
    match = re.search(r"Score:\s*(\d+)", output)
    score = match.group(1) if match else "Error: Score not found"
    return output

def get_score_rulebased(idx, trajectory, messages):
    aaa = "Action: Operation\n```sql"
    aa = "Action: Operation"
    a = "Action:"

    bbb = 'Action: Answer\nFinal Answer: ['
    bb = 'Action: Answer'
    b = 'Action:'
    
    if (aaa in response or aa in response or a in response) or\
        (bbb in response or bb in response or b in response):
        score = 2
        
    if invalid_action or multiple_actions:
        score = 1
    if incorrect_action_format:
        score = 2 
    if "Action: Operation\n```sql" in response or 'Final Answer: ["' in response:
        score = 3
    if score == 3 and sql_code_correct:
        score = 4

    return score

def get_score_hf(idx, trajectory, messages):
    history = [f"User: {ds['content'].strip()}\n" if ds['role'] == 'user' else f"Agent: {ds['content'].strip()}\n" for ds in trajectory[:idx]]
    history = '\n'.join(history).strip()
    response = trajectory[idx]['content']
    user = trajectory[idx+1]['content'] if idx < len(trajectory)-1 else ' '

    messages[1].content = messages[1].content.replace("<HISTORY_HERE>", history).replace("<AGENT_RESPONSE_TO_SCORE>", response).replace("<USER_RESPONSE>", user)
    
    output = model.predict_messages(messages).content
    
    # Extract the score from the generated text. Adjust regex as needed.
    match = re.search(r"Feedback:.*?(\d)", output)
    score = match.group(1) if match else "Error: Score not found"
    return output

def save_conversations(conversations, filename="conversations.jsonl"):
    with open(filename, 'w') as outfile:
        for conversation in conversations:
            json_line = json.dumps(conversation)
            outfile.write(json_line + '\n')
            
if __name__ == "__main__":
    # Set page config to use wide layout
    st.set_page_config(layout="wide")
    
    # UI toggle for selecting model_type
    model_type = st.selectbox("**Choose the evaluator type:**", ("human", "openai", "huggingface"))
    task = st.selectbox("**Choose the task:**", ("dbbench", "os-interaction", "knowledgegraph", "alfworld", "mind2web"))
    if task == "dbbench":
        task_idx = 2
    elif task == "os-interaction":
        task_idx = ""
    elif task == "knowledgegraph":
        task_idx = ""
    elif task == "alfworld":
        task_idx = ""
    elif task == "mind2web":
        task_idx = ""
    else:
        raise NotImplementedError
        
    if model_type == "huggingface": 
        from utils.hf_prompts import messages
        # Initialize the model
        model_name = 'kaist-ai/Prometheus-13b-v1.0'
        controller_address = None
        worker_address = "https://djmgoc1kei6phd-8880.proxy.runpod.net"
        temperature = 0.1
        max_new_tokens = 512
        top_p = 0.5
        model = FastChatAgent(model_name, controller_address=controller_address, worker_address=worker_address, 
                            temperature=temperature , max_new_tokens=max_new_tokens, top_p=top_p)
        get_score = get_score_hf
    elif model_type == "openai":
        from utils.openai_prompts import messages
        model = ChatOpenAI(model="gpt-3.5-turbo")
        model.temperature = 0.1
        get_score = get_score_openai
    elif model_type == "human":
        model, get_score = None, None
    else:
        raise NotImplementedError

    st.title(f"AgentEval")
    
    # File uploader for user to upload their JSONL file
    uploaded_file = st.file_uploader("Choose a JSONL file", type="jsonl")
    if uploaded_file is not None:
        # Function to load conversations from uploaded JSONL
        def load_conversations(uploaded_file):
            conversations = [] 
            for line in uploaded_file:
                json_object = json.loads(line)
                conversations.append(json_object)
            return conversations

        if "-scored_" in uploaded_file.name:
            if 'all_scores' not in st.session_state: st.session_state.all_scores = load_conversations(uploaded_file)
            uploaded_file = open(f"./data/{task}/" + uploaded_file.name.split("-scored_")[0] + ".jsonl", "r")
            conversations = load_conversations(uploaded_file)
        else: 
            conversations = load_conversations(uploaded_file)

        # Navigation state
        if 'index' not in st.session_state:
            st.session_state.index = 0

        # Current conversation
        current_conversation = conversations[st.session_state.index]
        
        if 'all_scores' not in st.session_state:
            st.session_state.all_scores = []
            for conversation in conversations:
                st.session_state.all_scores.append({idx: "" for idx in range(len(conversation['output']['history']))})
        if 'scores' not in st.session_state:
            st.session_state.scores = {int(k): v for k, v in st.session_state.all_scores[st.session_state.index].items()}

        # Update index function for navigation
        def update_index(increment):
            st.session_state.index += increment
            st.session_state.index %= len(conversations)  # Wrap around to loop through conversations
            st.session_state.scores = {int(k): v for k, v in st.session_state.all_scores[st.session_state.index].items()}

        # Display the groundtruth at the top of every conversation
        dev_list = []
        with open(f"./data/{task}/dev.jsonl", 'r') as file:
            for line in file:
                dev_list.append(json.loads(line))
        for dev in dev_list:
            if dev['description'] in current_conversation['output']['history'][task_idx]['content']:
                st.write(f"### Groundtruth: ```{dev['label']}```")
        
        row = st.container()
        with row: 
            col1, col2 = st.columns([5, 5])  # Adjust the ratio as needed
            
            with col1:
                st.header("Agent")
                
            with col2:
                st.header("Evaluator")
                
        # Display each turn with its evaluation in a side-by-side layout
        for i, turn in enumerate(current_conversation['output']['history']):
            row = st.container()
            with row:
                col1, col2 = st.columns([5, 5])
                with col1:
                    st.text_area(turn['role'].upper(), value=turn['content'], key=f"turn_{i}")
                
                with col2:
                    if turn['role'] == 'user': 
                        st.write("")  # Placeholder or leave empty
                    else:
                        if model_type == "human":
                            with st.container():
                                # Initialize with an empty string if not present
                                if i not in st.session_state.scores:
                                    st.session_state.scores[i] = ""
                                # Display an editable text area with a label indicating it's for scoring
                                score_input = st.text_area("", value=st.session_state.scores[i], key=f"score_input_{i}")
                                st.session_state.scores[i] = score_input
                        else:
                            # Display a play symbol as a button for scoring
                            play_button = st.button("▶️", key=f"play_btn_{i}")
                            if play_button:
                                # Calculate and display the score upon clicking the play symbol
                                st.session_state.scores[i] = get_score(i, current_conversation['output']['history'], messages)

                        # Display the score if it has been calculated
                        if i in st.session_state.scores:
                            st.write(st.session_state.scores[i])
        st.session_state.all_scores[st.session_state.index] = st.session_state.scores

        # Button to save the input to a pickle file
        _, col2, _ = st.columns([3, 3, 3])
        with col2:
            # Interface to input the file name
            file_path = st.text_input("Enter the name of the file to save to (with .jsonl extension):")
            if st.button('Save to jsonl file'):
                if file_path:
                    # Saving data to the specified jsonl file
                    with open(file_path, "w") as file:
                        for line in st.session_state.all_scores:
                            json_line = json.dumps(line)
                            file.write(json_line + '\n')
                    st.success("conversation saved")
                else:
                    st.error("Please enter a file name.")
            
        # Navigation buttons
        st.write("")  # Add some space
        col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 2.5])
        with col1:
            st.button("<-Previous", on_click=update_index, args=(-1,))
        with col3:
            # Display the current example number and total
            st.write(f"{st.session_state.index + 1} of {len(conversations)}")
        with col4:
            st.button("Next->", on_click=update_index, args=(1,))
    else:
        st.write("Please upload a JSONL file to begin.")
