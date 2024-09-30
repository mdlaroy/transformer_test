from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re

model_name = "gpt2-large"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

def generate_response(prompt, max_new_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
    with torch.no_grad():
        output = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=max_new_tokens,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.5,  
            pad_token_id=tokenizer.eos_token_id,
        )

    full_response = tokenizer.decode(output[0], skip_special_tokens=True)
    response = full_response[len(prompt):].strip()
    
    # remove any dialogue-like patterns and keep only the content
    response = re.sub(r'^(human:|meep:|ai:|bot:)\s*', '', response, flags=re.IGNORECASE)
    response = re.split(r'\n|(?<=[.!?])\s', response)[0]  # take only the first sentence
    
    return response.strip()

def chat():
    conversation_history = []
    context_window = 15 
    print("meep: Hi there! I'm meep. What would you like to talk about? (Type 'quit' to exit)")
    
    while True:
        user_input = input("you: ")
        if user_input.lower() in ['quit']:
            print("meep: until next time!")
            break

        conversation_history.append(f"you: {user_input}")
        context = "\n".join(conversation_history[-context_window:])
        prompt = f"The following is a conversation with an AI companion named meep. meep is helpful, creative, clever, and very friendly.\n\n{context}\nmeep:"
        
        response = generate_response(prompt)
        while len(response.split()) < 3 or response.lower() in ["no", "yes", "hello", "hi"]:
            response = generate_response(prompt)
        
        print(f"meep: {response}")
        
        conversation_history.append(f"meep: {response}")

chat()
