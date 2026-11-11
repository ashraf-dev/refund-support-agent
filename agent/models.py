from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model=init_chat_model(model="gpt-5.4-mini") # gpt-5.4-mini gpt-6-luna الارخص حاليا

#test
#response=model.invoke("tell me something about moon")
#print(response.content)
