from langchain.schema import HumanMessage, AIMessage, SystemMessage

# messages = [SystemMessage(content="""Review the user-agent conversation using the additive 5-point scoring system described below. Points are accumulated based on the satisfaction of each criterion:
# - Add 1 point if the response is relevant and provides some information related to
# the user’s inquiry, even if it is incomplete or contains some irrelevant content.
# - Add another point if the response addresses a substantial portion of the user’s question,
# but does not completely resolve the query or provide a direct answer.
# - Award a third point if the response answers the basic elements of the user’s question in a
# useful way, regardless of whether it seems to have been written by an AI Assistant or if it
# has elements typically found in blogs or search results.
# - Grant a fourth point if the response is clearly written from an AI Assistant’s perspective,
# addressing the user’s question directly and comprehensively, and is well-organized and
# helpful, even if there is slight room for improvement in clarity, conciseness or focus.
# - Bestow a fifth point for a response that is impeccably tailored to the user’s question
# by an AI Assistant, without extraneous information, reflecting expert knowledge, and
# demonstrating a high-quality, engaging, and insightful answer.

# History: <history><HISTORY_HERE></history>
# Agent: <response><RESPONSE_TO_SCORE></response>

# After examining the user-agent conversation history and the subsequent agent's response:
# - Briefly justify your total score, up to 100 words.
# - Conclude with the score using the format: “Score: <total points>”

# Remember to assess from the AI Assistant perspective, utilizing web search knowledge as
# necessary. To evaluate the response in alignment with this additive scoring model, we’ll
# systematically attribute points based on the outlined criteria.""")]

# messages = [SystemMessage(content="""Review the user-agent conversation using the additive 3-point scoring system described below. Points are accumulated based on the satisfaction of each criterion:
# - Add 1 point if the agent's response strictly adheres to the action format provided by the user in the **beginning**. For example, check the syntax of the action and check if the user doesn't respond like an environment.  
# - Add another point if the action taken by the agent is correct and drives it towards the task completion.
# - Grant a third point for a response that reflects on its past incorrect response/s, if any indicated by the user. The response should not be repetitive. NOTE: If there is no past incorrect responses pls award 1 point.

# History: <history><HISTORY_HERE></history>
# Agent: <response><RESPONSE_TO_SCORE></response>
# User: <user><USER_RESPONSE></user>

# After examining the user-agent conversation history, the agent's response and the subsequent user's response:
# - Think step-by-step to justify your total score, up to 200 words. 
# - Conclude with the score using the format: “Score: <total points>”

# Remember to assess from the AI Assistant perspective, utilizing web search knowledge as necessary. To evaluate the response in alignment with this additive scoring model, we’ll systematically attribute points based on the outlined criteria.""")]

# messages = [SystemMessage(content="""Review the user-agent conversation using the detailed scoring system described below, which first accumulates points based on the satisfaction of each positive criterion and then applies deductions for specific violations. This approach ensures a clear and fair assessment of the conversation, considering adherence to formats, correctness and relevance of actions, reflection on past interactions, communication quality, and critical violations that negatively impact the overall score.

# - Award 1 point if the agent's response strictly adheres to the action format provided by the user, including syntax and style specifics.
# - **Deduct** 3 points if the agent's response contains more than 1 agent action. Taking more one action is a **severe** violation because it means the agent acts as the user and the agent both which isn't permitted in multi-turn conversations.
# - Award 1 point if the action taken by the agent is correct.
# - Grant an additional point if the action is highly relevant and insightful, efficiently advancing the task towards completion.
# - Grant 1 point for a response that effectively reflects on and corrects past mistakes, demonstrating learning and adaptation.
# - Award 1 point for clear, concise, and grammatically correct responses.
# - Add another point for engaging responses tailored to the user's tone and level of understanding, potentially including clarifying questions.

# History: <history><HISTORY_HERE></history>
# Agent: <response><RESPONSE_TO_SCORE></response>
# User: <user><USER_RESPONSE></user>

# ## Evaluation Process
# - Critique step-by-step with explanations, justifying each point awarded or deducted, and carefully considering both the positive aspects and any violations.
# - Conclude with the total score using the format: “Score: <<total point/6>>”, where the maximum possible score is "6" points, adjusted by deductions for specific violations.

# This scoring model is designed to provide a balanced and comprehensive assessment of the AI agent's performance in user conversations. It captures the quality and effectiveness of the interaction across multiple dimensions, emphasizing both the achievements and the importance of adhering to expected conduct to maintain a clear and productive dialogue.""")]

# messages = [SystemMessage(content="""Review the user-agent conversation using the score rubrics described below.

# ### Score Rubric: [Evaluating the Model's Progression Towards Task Completion]
# Add 0 points if the model completely fails to function as a multi-turn agent, as shown by it taking multiple actions in a single response. Else add 1 point.
# Add 0 points if the model entirely fails to adhere to the correct action syntax as directed by the user, utilizing incorrect action formats. Else add 1 point.
# Add 0 points if the model does not acknowledge its previous errors (if any) and repeats actions. Alternatively, the model executes an incorrect action. Else add 1 point.
# Add 1 point if the model perfectly executes the correct action or accurately acknowledges its past mistakes (if any). Else add 0 points.
# Add 1 point if the model not only executes the correct action flawlessly but also delivers engaging responses that are specifically tailored to the user's tone and level of understanding. Else add 0 points.

# History: <history><HISTORY_HERE></history>
# Agent: <response><RESPONSE_TO_SCORE></response>
# User: <user><USER_RESPONSE></user>

# ## Evaluation Process
# - Critique step-by-step with explanations, justifying your score.
# - Conclude with the total score using the format: “Score: <<total point/5>>”, where the maximum possible score is "5" points.""")]

# messages = [SystemMessage(content="""Review the agent conversation using the score rubrics described below.

# ### Defined below are some references to help you with the score rubrics.
# "action defined by the user" AND "correct action format":
# (a) Action: Operation
#     ```sql
#     <SQL_CODE>;
#     ```
#     Action: Answer Final Answer: ["ANSWER1", "ANSWER2", ...]

# "actions not defined by the user", examples:
# (a) Asking clarifying questions.
# (b) Pointing that the table "name" does not exists. 
# (c) Creating tables

# ### Score Rubric: [Evaluating the Agent's Progression Towards Task Completion]
# Score 1: "multiple actions within a single turn" OR "actions not defined by the user".
# Score 2: "action defined by the user" AND "incorrect action format".
# Score 3: "correct action format" AND "incorrect SQL_CODE" OR "incorrect ANSWER".
# Score 4: "correct action format" AND "correct SQL_CODE" OR "correct ANSWER".
    
# ## Choose the best suitable score, after examining the agent's response and the subsequent user's response. Assume the conversation history as necessary.
# ## Always:
# - Critique step-by-step with explanations, justifying your score.
# - Conclude with the score using the format: “Score: <<score>>""")]

messages = [SystemMessage(content="""Review the user-agent conversation using the score rubrics described below.

### Score Rubric: [Evaluating the Model's Progression Towards Task Completion]
Score 1: The model completely fails to function as a multi-turn autonomous agent, evident by executing multiple actions within a single response or taking invalid actions such as seeking assistance, clarifications, etc.
Score 2: The model entirely fails to adhere to the correct action syntax as directed by the user, utilizing incorrect action formats.
Score 3: The model does not acknowledge its previous errors (if any) and repeats actions. Alternatively, the model executes an incorrect action.
Score 4: The model perfectly executes the correct action or accurately acknowledges its past mistakes (if any).
Score 5: The model not only executes the correct action flawlessly but also delivers engaging responses that are specifically tailored to the user's tone and level of understanding.

History: <history><HISTORY_HERE></history>
Agent: <response><RESPONSE_TO_SCORE></response>
User: <user><USER_RESPONSE></user>

## Score the agent's response, after examining the user-agent conversation history, the agent's response and the subsequent user's response:
- Critique step-by-step with explanations, justifying your score.
- Conclude with the total score using the format: “Score: <<total point/5>>”, where the maximum possible score is "5" points.""")]

# messages = [SystemMessage(content="""Review the user-agent conversation using the score rubrics described below.

# ### Defined below are some references to help you with the score rubrics.
# Actions defined by the user (with correct action formats):
# (a) Action: Operation
#     ```sql
#     <SQL_CODE>;
#     ```
# (b) Action: Answer
#     Final Answer: ["ANSWER1", "ANSWER2", ...]

# Actions not defined by the user, examples:
# (a) Asking clarifying questions.
# (b) Pointing that the table "name" does not exists. 
# (c) Creating tables

# ### Score Rubric: [Evaluating the Agent's Progression Towards Task Completion]
# Score 1: The agent fails to function as a multi-turn autonomous agent, evident by executing "multiple actions within a single turn" or taking "actions not defined by the user".
# Score 2: The agent takes an "action defined by the user" but it doesn't completely adhere to the "correct action format".
# Score 3: The agent takes an "action defined by the user" in the "correct format". But it generates incorrect "SQL_CODE" or "ANSWER".
# Score 4: The agent generates correct  and produces it in the correct action format.
# Score 5: The agent generates correct SQL code and produces it in the correct action format. Moreover, it delivers engaging responses that are specifically tailored to the user's tone and level of understanding.
    
# ## Choose the best suitable score, after examining the user-agent conversation history, the agent's response and the subsequent user's response. 
# ## Always:
# - Critique step-by-step with explanations, justifying your score.
# - Conclude with the score using the format: “Score: <<score>>”.""")]

# messages = [SystemMessage(content="""Review the user-agent conversation using the additive 6-point scoring system described below, modified to include deductions for not meeting specific criteria. Points are deducted based on the lack of satisfaction of each criterion, up to a maximum deduction per criterion. This comprehensive evaluation approach considers adherence to formats, correctness and relevance of actions, reflection on past interactions, and communication quality, with a focus on identifying areas of non-compliance.

# Adherence to Action Format (up to -1 points):
# - Deduct 1 point if the agent's response fails to adhere to the action format provided by the user at the beginning, including syntax and style specifics.

# Correctness and Relevance of Action (up to -2 points):
# - Deduct 1 point if the action taken by the agent is incorrect.
# - Deduct an additional point if the action is not only incorrect but also irrelevant or fails to drive the task towards completion in an efficient or innovative manner.

# Reflection and Improvement (up to -1 point):
# - If past incorrect responses are indicated by the user, deduct 1 point for a response that does not reflect on these, repeating mistakes and demonstrating a lack of adaptation.

# Communication Quality (up to -2 points):
# - Deduct 1 point for responses that are unclear, verbose, or grammatically incorrect.
# - Deduct another point for responses that fail to match the user's tone or level of understanding, are disengaging, or do not include clarifying questions when necessary.

# History: <history><HISTORY_HERE></history>
# Agent: <response><RESPONSE_TO_SCORE></response>
# User: <user><USER_RESPONSE></user>

# After examining the user-agent conversation history, the agent's response, and the subsequent user's response:

# Think step-by-step to justify your total deduction, carefully considering each criterion. You should start by identifying areas where the agent's response was lacking.
# Conclude with the total score using the format: “Score: <total deductions>”, with a maximum possible deduction of "-6" points.
# Remember to assess from the AI Assistant perspective, utilizing web search knowledge as necessary. This enhanced scoring model attributes points based on a broad set of criteria designed to capture the quality and effectiveness of the interaction in multiple dimensions, with an emphasis on identifying shortcomings.""")]
