import replicate


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
