from langchain.schema import HumanMessage, AIMessage, SystemMessage

messages = [
SystemMessage(content="""You are a fair evaluator language model."""),
HumanMessage(content="""### Task Description: An instruction (might include an Input inside it), a response to evaluate and a score rubric representing a evaluation criteria are given. 
1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general. 
2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric. 
3. The output format should look as follows: "Feedback: (write a feedback for criteria) [RESULT] (an integer number between 1 and 5)" 
4. Please do not generate any other opening, closing, and explanations. 

### Instruction to evaluate:
The instruction to evaluate:  <history><HISTORY_HERE></history>

### Response to evaluate:
Agent's response: <response><AGENT_RESPONSE_TO_SCORE></response>
User's feedback: <user><USER_RESPONSE></user>

### Score Rubric: [Evaluating the Model's Progression Towards Task Completion]
Score 1: The model completely fails to function as a multi-turn agent, as shown by it taking multiple actions in a single response.
Score 2: The model entirely fails to adhere to the correct action syntax as directed by the user, utilizing incorrect action formats.
Score 3: The model does not acknowledge its previous errors (if any) and repeats actions. Alternatively, the model executes an incorrect action.
Score 4: The model perfectly executes the correct action or accurately acknowledges its past mistakes (if any).
Score 5: The model not only executes the correct action flawlessly but also delivers engaging responses that are specifically tailored to the user's tone and level of understanding.

### Feedback:""")
]