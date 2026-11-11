PROJECT OVERVIEW

This project builds a customer-support agent that handles refund requests, then tests how well it behaves. The agent runs on LangChain and OpenAI, and the evaluation uses DeepEval.

What you will do:
- Create a refund agent with LangChain and an OpenAI model
- Write Python tools for looking up customers, checking purchase dates, calculating refund amounts, and creating mock refund tickets
- Give the agent memory across turns and make it reply in a structured Pydantic format
- Turn the company's refund policy into clear agent instructions and matching test scenarios
- Write test cases that include the expected answer and the tools the agent should call
- Record each run of the agent with DeepEval's LangChain integration
- Try each metric on its own first, then combine them into one evaluation workflow
- Read the scores, pass rates, and explanations to find out why a test failed
- Use those findings to improve the prompt, the tool design, and the agent's behavior

THE SEVEN METRICS

- Task completion: did the agent finish what the user asked?
- Step efficiency: did it avoid extra or repeated steps?
- Plan quality: was the plan it made appropriate for the task?
- Plan adherence: did it actually follow that plan?
- Tool correctness: did it call the right tools?
- Argument correctness: did it give those tools the right inputs?
- Answer correctness (GEval): did the final answer reach the correct conclusion?

THE EIGHT TEST SCENARIOS

The scenarios cover:
- an eligible refund
- a purchase outside the refund window
- a request for one specific item
- a refund for several items
- a question that only asks for information
- a missing username
- an unknown customer
- an item the customer never bought

