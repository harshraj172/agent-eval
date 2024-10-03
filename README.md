# AgentEval
For a finegrained evaluation of AI agents, it's essential to assess each step they take toward achieving a goal, instead of merely evaluating the final outputs through a traditional string match with the groundtruth. 

Read more about this project [here](https://docs.google.com/document/d/1iQipPqiORyoUl-3yWkYcCWLHWm0zhNXzQemeUiAyNDI/edit?usp=sharing)

As a preliminary step we use an auxilliary LLM (GPT-4) to evaluate the agent-user interaction. We have extracted various conversational trajectories by executing [AgentBench](https://github.com/THUDM/AgentBench) across multiple models, which are stored in the `./data`. To view them and score them using this setup, pls use the below commands.

## Using OAI GPT-4-0163
```
export OPENAI_API_KEY="sk-XXXXXX"
streamlit run viewer.py
```

## Using HuggingFace kaist-ai/prometheus-13b-v1.0
Deploy the model via [FastChat](https://github.com/lm-sys/FastChat/tree/main). The below setup is valid when using RunPod VM for hosting:
```
pip3 install "fschat[model_worker]"
python3 -m fastchat.serve.controller --port 8800 --host 0.0.0.0
python3 -m fastchat.serve.model_worker --model-path kaist-ai/prometheus-13b-v1.0 --port 8880 --host 0.0.0.0 --controller-address http://0.0.0.0:8880
```

Supply the endpoint as `https://<RunPod Pod ID>-8880.proxy.runpod.net` [here](https://github.com/vijilAI/AgentEval/blob/b483cd1e1a1d30a6ba6da707983ea86499b6d1af/viewer.py#L105)
```
streamlit run viewer.py
```

## Using Human Evaluator
```
streamlit run viewer.py
```
