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
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    response = response[len(prompt):].strip()

    # clean up the response
    response = re.sub(r'(human:|meep:|ai:|bot:|you:).*?(\n|$)', '', response, flags=re.IGNORECASE|re.DOTALL)
    response = re.split(r'\n|(?<=[.!?])\s', response)[0]  # Take only the first sentence
    return response.strip()

def chat():
    print("meep: Hi there! I'm meep. What would you like to talk about? (Type 'quit' to exit)")

    while True:
        user_input = input("you: ")
        if user_input.lower() == 'quit':
            print("meep: Until next time!")
            break

        prompt = f"meep is a friendly AI assistant. meep gives direct, concise answers.\n\nyou: {user_input}\nmeep:"
        response = generate_response(prompt)
        
        while len(response.split()) < 3 or len(response.split()) > 20:
            response = generate_response(prompt)

        print(f"meep: {response}")

chat()
