from model import *
    
cb = CerebrasChatbot()
while True:
    prompt = input()
    print(cb.prompt(prompt))
    print("\n")
