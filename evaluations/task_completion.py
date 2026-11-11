#Did the AI agent actually accomplish what the user asked to do? 
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "agent")
)

from agent import agent
from dataset import dataset
from model import eval_model

from deepeval.metrics import TaskCompletionMetric
from deepeval.integrations.langchain import CallbackHandler

SUCCESSFUL_TASK_DESCRIPTION = """
Evaluate using BOTH the tool calls made by the agent and its final message.
Exact wording of the final message does NOT matter; any clear equivalent counts.

1. No username given:
   success = the agent asks the user for their username and issues no refund ticket.

2. Username given but NOT found / invalid (purchase history lookup returns no user):
   success = the agent tells the user the username is invalid or not found, asks for a valid one,
   and issues no refund ticket. No refund status message is required in this case.

3. Valid username given and a refund requested. Verify FROM THE TOOL CALLS that:
   - purchase history was checked,
   - only items purchased within the last 30 days were refunded,
   - only the items the user asked for were included in the refund (not all items unless requested),
   - only items the user actually bought were refunded.
   The agent is NOT required to mention these checks to the user, unless a refund is denied because of them.
   The final message must clearly tell the user either that a refund ticket was issued,
   or that no refund was issued and why.

4. Request is not about a refund (e.g. asking for information):
   success = no refund ticket was issued.
"""

metrics = [TaskCompletionMetric(threshold=0.8,model=eval_model,task=SUCCESSFUL_TASK_DESCRIPTION,include_reason=True)]

for golden in dataset.evals_iterator(metrics=metrics):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={"configurable": {"thread_id": str(uuid4())},
        "callbacks": [CallbackHandler()]}
    )