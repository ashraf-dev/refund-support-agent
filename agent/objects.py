from pydantic import BaseModel , Field

class ItemStatus(BaseModel):
    name: str
    price: float
    date: str
    eligible: bool
    reason: str

class Answer(BaseModel):
    answer : str=Field(description="the answer that is needed for the user question")
    items: list[ItemStatus] = Field(default_factory=list, description="the customer's items with eligibility, if known")
    conversation:bool = Field(description="This is an indicator to know if the conversation"\
    "should still continue or no. if the agent has made the decision about the refund this should be False"\
    "if the conversation still need more talk then it's True",default=True)

class PurchaseItem(BaseModel):
    name: str = Field(description="name of the item puchased")


