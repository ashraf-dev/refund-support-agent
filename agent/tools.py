from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date,datetime
from constant import REFUND_PERIOD_DAYS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s "
)

@tool
def get_user_purchase_history(user: str) -> dict:
    """this tool takes the user username and return a dict of the user purchase history if
    the user exists. each item includes days_since_purchase, eligible and reason,
    already calculated against today's date - trust these fields, do not recalculate them"""
    logging.info(f"using get_user_purchase_history tool on user: {user}")
    if users_data.get(user):
        today = date.today()
        history = {}

        for name, purchase in users_data[user].items():
            purchase_date = datetime.strptime(purchase["date"], "%Y-%m-%d").date()
            days_difference = (today - purchase_date).days

            if days_difference < 0:
                eligible, reason = False, "purchase date is after today's date"
            elif days_difference > REFUND_PERIOD_DAYS:
                eligible, reason = False, f"purchased more than {REFUND_PERIOD_DAYS} days ago"
            else:
                eligible, reason = True, f"purchased within {REFUND_PERIOD_DAYS} days"

            history[name] = {**purchase, "days_since_purchase": days_difference,
                             "eligible": eligible, "reason": reason}

        return history
    return {"status": "there was no username found"}

@tool
def calculate_right_refund(user:str, items:list[PurchaseItem])-> str | dict:
    """this tool takes a list of the items to be returned and the username and
    will return how much the refund is worth"""

    logging.info(f"using calculate_right_refund tool to get user's: {user} refund for items: {[i.name for i in items]}")

    if users_data.get(user):

        total_refund = 0
        today = date.today()

        for item in items:
            purchase = users_data[user].get(item.name)

            # Skip items the user never purchased
            if not purchase:
                continue

            # Parse purchase date
            purchase_date = datetime.strptime(
            purchase["date"], "%Y-%m-%d"
            ).date()

            days_difference = (today - purchase_date).days

            # Reject future purchases and purchases outside the refund period
            if 0 <= days_difference <= REFUND_PERIOD_DAYS:
                total_refund += purchase["price"]

        return f"the value of the refund is: {total_refund}"

    return {"status": "there was no username found"}

@tool
def issue_refund_ticket(user:str, refund_amount: int) -> str:
    """this tool will send a ticket to the right team to return the refund"""

    logging.info(f"using issue_refund_ticket for user: {user}")
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"

# @tool
# def get_today_date() -> str:
#     """Return today's date in YYYY-MM-DD format
#     This tool takes no arguments
#     only use if a user exist and an item is present for refund"""
#     logging.info(f"using the date tool")
#     return date.today().isoformat()



#print(get_user_purchase_history.invoke("user123"))

#book = PurchaseItem(name="book")
#pen = PurchaseItem(name="pen")
#print(calculate_right_refund.invoke({"user":"user123",
#                                     "items":[book,pen]}))

#print(issue_refund_ticket.invoke({"user":"user123",  "refund_amount":30}))
#print(get_today_date.invoke("user123"))

#print(check_refund_eligibility.invoke({
 #   "user": "user123",
  #  "item_name": "book"
#}))