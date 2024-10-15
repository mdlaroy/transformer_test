from openai import OpenAI
import random
#.\Scripts\Activate.ps1     since you always forget skullemoji


# NOTE TO CHRISTINA! DO NOT SAVE THE API KEY IN THE CODE! IF YOU ARE GOING TO PUSH TO REPO, PLS MAKE SURE TO REMOVE IT

# billing right now is on a pay per use system. i added about 10 bucks to our account. will monitor usage as we go
client = OpenAI(api_key='')




user_name = ""
conversation_history = []

friendly_responses = [
    "I'm so glad you asked that! ",
    "That's a great question, " + user_name,
    "I'm always excited to talk about this! ",
    "You always have the most interesting things to say! "
]

def generate_response(prompt, max_tokens=100):
    global conversation_history
    
    conversation_history.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are meep, a friendly and supportive AI companion. You're enthusiastic, caring, and always eager to chat. You use a warm tone, occasional emojis, and show genuine interest in the user's thoughts and feelings. You remember details about the user's conversation and refer back to them in conversation. Your responses are engaging but concise."},
                *conversation_history
            ],
            max_tokens=max_tokens,
            n=1,
            temperature=0.8,
        )
        
        ai_response = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # only the last 10 exchanges to keep token usg down
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        
        return ai_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, I encountered an error. Can we try that again?"

def chat():
    global user_name
    print("meep: Hi there! I'm meep, your AI companion. What's your name?")
    
    user_name = input("you: ").strip()
    print(f"meep: It's wonderful to meet you, {user_name}! What would you like to chat about today? (Type 'quit' to exit)")
    
    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() == 'quit':
            print(f"meep: Bye Bye {user_name}! Talk to you again soon <3")
            break

        response = generate_response(user_input)
        
        #friendly opener to some responses
        if random.random() < 0.3:  # increase odds of friendly response
            response = random.choice(friendly_responses) + response

        print(f"meep: {response}")

chat()
