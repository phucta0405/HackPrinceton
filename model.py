import replicate
import os
from cerebras.cloud.sdk import Cerebras

class Chatbot:
    def __init__(self,model="meta/meta-llama-3-8b-instruct"):
        self.model = model
    
    def prompt(self, prompt):
        for i in replicate.run(
            f"{self.model}",
            input={
                "top_k": 50,
                "top_p": 1,
                "prompt": f"{prompt}",
                "decoding": "top_p",
                "max_length": 50,
                "temperature": 0.75,
                "repetition_penalty": 1.2
            }
        ):
            yield i

#upgraded chatbot with message memory
class CerebrasChatbot:
    def __init__(self):
        self.client = Cerebras(
            # This is the default and can be omitted
            api_key="csk-xd8t5rj64mmk6j969t2hn26henttx5xc3jhh3jt9m9px8rkm",
        )
        self.messages = []
    
    def prompt(self,prompt):
        self.messages.append({
                    "role": "user",
                    "content": f"{prompt}",
                })
        stream = self.client.chat.completions.create(
            messages=self.messages,
            model="llama3.1-8b",
            stream = True,
        )
        st = ""
        
        for i in stream:
            st+=f"{i.choices[0].delta.content} "
            yield i.choices[0].delta.content or ""
            
        self.messages.append({
                    "role": "assistant",
                    "content": f"{st}",
                })
