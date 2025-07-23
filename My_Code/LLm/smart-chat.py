import ollama
class SmartAgent:
    model_name = "gemma3:1b"
    def __init__(self):
        print("Agent is created")
    def chat(self, history):
        answer = ollama.chat(model=self.model_name, messages=history)
        return answer

if __name__ == "__main__":
    history=[]
    with open("context_prompt.txt", "r") as data:
        history.append({'role':'system', 'content':data.read()}) 
    smart_agent = SmartAgent()

    question=input("Questions?\n")
    while question != 'bye':
        if question != '':
            history.append({'role':'user', 'content':question})
            answer = smart_agent.chat(history)
            print(answer['message']['content'])
            history.append({'role':'agent', 'content':answer['message']['content']})
        else:
            print("Question is empty\n")
        question = input("Questions?\n") 
