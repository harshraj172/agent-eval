# python score-trajectory.py --input_file ./data/alfworld/agentlm-7B.jsonl

import argparse
import json
import re
from tqdm.auto import tqdm
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from utils.openai_prompts import messages

def get_score(idx, trajectory, messages, model):
    # instruction = trajectory[0]['content'].strip()
    history = [f"User: {ds['content'].strip()}\n" if ds['role'] == 'user' else f"Agent: {ds['content'].strip()}\n" for ds in trajectory[:idx]]
    history = '\n'.join(history).strip()
    history = f"<history>{history}</history>"
    response = f"<response>{trajectory[idx]['content']}</response>"
    user = f"<user>{trajectory[idx+1]['content'] if idx < len(trajectory)-1 else '  '}</user>"
    
    human_message = [HumanMessage(content=\
    """
    History: {}

    Agent: {}
    User: {}""".format(history, response, user))]
    output = model.predict_messages(messages + human_message).content
    match = re.search(r'score: (\d+)/', output.lower())
    score = match.group(1) if match else "Error: Score not found"
    return score

def load_jsonl(file_path):
    dict_list = []
    with open(file_path, 'r') as file:
        for line in file:
            json_object = json.loads(line)
            dict_list.append(json_object)
    return dict_list

def score_conversation(conversation, messages, model):
    scores = {idx: "" for idx in range(len(conversation['output']['history']))}
    for idx, turn in enumerate(conversation['output']['history']):
        if turn['role'] == 'agent' and idx != 1:
            scores[idx] = get_score(idx, conversation['output']['history'], messages, model)
    return scores

def save_jsonl(dict_list, filename):
    with open(filename, 'w') as outfile:
        for dict in dict_list:
            json_line = json.dumps(dict)
            outfile.write(json_line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Score conversation trajectories using OpenAI model.')
    parser.add_argument('--input_file', type=str, help='The input jsonl file containing the conversations.')
    args = parser.parse_args()

    model = ChatOpenAI(model="gpt-4-0613")
    model.temperature = 0.1
    
    conversations = load_jsonl(args.input_file)
    scores = []
    for conversation in tqdm(conversations):
        scores.append(score_conversation(conversation, messages, model))
        save_jsonl(scores, f"./data/{args.input_file.split('/')[-2]}/{args.input_file.split('/')[-1].replace('.jsonl', '')}-scored_gpt4.jsonl")

    print(f"Conversations have been scored and saved")
