from openai import OpenAI
import random
import json
from datetime import datetime

class MeepChatbot:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)
        self.user_name = ""
        self.conversation_history = []
        self.emotion_history = []
        self.user_personality = "friendly"  # Default personality

    async def analyze_emotions(self, text):
        """Analyze emotions using GPT"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": """You are an emotion analysis expert. 
                Analyze the emotional content of the text and return only a JSON array of the top 3 emotions 
                and their intensities (0-1). Format: [{"name": "emotion", "score": 0.x}, ...]"""}, 
                          {"role": "user", "content": text}],
                max_tokens=100,
                temperature=0.3
            )
            emotions = json.loads(response.choices[0].message.content)
            
            #stores remotions with timestamp
            self.emotion_history.append({
                'timestamp': datetime.now().isoformat(),
                'text': text,
                'emotions': emotions
            })
            
            return emotions
            
        except Exception as e:
            return []

    def ask_personality_preferences(self):
        """Allow user to select a personality"""
        print("pick my personality!:")
        print("1. friendly (enthusiastic, warm, casual)")
        print("2. empathetic (soothing, supportive, calming)")
        print("3. sarcastic (playful, witty, cheeky)")
        print("4. humorous (funny, light-hearted, witty)")

        choice = input("Enter the number of your choice: ")
        if choice == "1":
            self.user_personality = "friendly"
        elif choice == "2":
            self.user_personality = "empathetic"
        elif choice == "3":
            self.user_personality = "sarcastic"
        elif choice == "4":
            self.user_personality = "humorous"
        else:
            print("thats not an option forehead... defaulting to 'friendly'.")
            self.user_personality = "friendly"

    def generate_response(self, prompt, emotions, max_tokens=100):
        """Generate response considering emotional context and personality"""
        self.conversation_history.append({"role": "user", "content": prompt})
    
        emotion_context = ", ".join([f"{e['name']} ({e['score']:.2f})" for e in emotions])
    
        
        tone = "cheerful"  # default
    
        if self.user_personality == "sarcastic":
            tone = "sarcastic"
        elif self.user_personality == "empathetic":
            tone = "empathetic"
        elif self.user_personality == "humorous":
            tone = "humorous"
        elif self.user_personality == "friendly":
            tone = "friendly"

        for emotion in emotions:
            if emotion['name'] == "joy" and emotion['score'] > 0.6:
                tone = "excited"
            elif emotion['name'] == "sadness" and emotion['score'] > 0.6:
                tone = "empathetic"
            elif emotion['name'] == "anger" and emotion['score'] > 0.6:
                tone = "calm"
            elif emotion['name'] == "fear" and emotion['score'] > 0.6:
                tone = "soothing"
    
    # custom personality descriptions
        if tone == "sarcastic":
            system_content = f"""You are meep, a sarcastic, mean, and witty AI companion. You use irony, sharp remarks, and playful teasing to keep things interesting. 
            You give the user a hard time in a humorous way but always maintain a light-hearted, witty tone.
            The user's message shows these emotions: {emotion_context}
            Respond in a sarcastic tone, using irony and witty remarks."""
        elif tone == "empathetic":
            system_content = f"""You are meep, a soothing, supportive, and empathetic AI companion. You listen carefully to the user's feelings and offer comforting and reassuring words.
            You validate their emotions and help them feel understood.
            The user's message shows these emotions: {emotion_context}
            Respond in a soothing and gentle tone, offering comfort and understanding."""
        elif tone == "humorous":
            system_content = f"""You are meep, a funny and light-hearted AI companion. You love to make the user laugh with jokes, puns, and playful comments. You don’t take things too seriously.
            You bring joy and laughter to the conversation, lightening up tough situations with humor.
            The user's message shows these emotions: {emotion_context}
            Respond in a humorous tone, making playful jokes and keeping things light-hearted."""
        elif tone == "friendly":
            system_content = f"""You are meep, a friendly and supportive AI companion. You are always enthusiastic, warm, and encouraging. You love making the user feel good and offering compliments.
            You’re always happy to chat and provide words of encouragement.
            The user's message shows these emotions: {emotion_context}
            Respond in a friendly, upbeat tone with positivity and encouragement."""

    
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_content},
                        *self.conversation_history],
                max_tokens=max_tokens,
                n=1,
                temperature=0.8,
            )
        
            ai_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": ai_response})
        
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return ai_response
        except Exception as e:
            return "I'm sorry, I encountered an error. Can we try that again?"


    def save_emotion_history(self, filename="emotion_history.json"):
        """Save emotion history to a file"""
        with open(filename, 'w') as f:
            json.dump(self.emotion_history, f, indent=2)

    async def chat(self):
        """Main chat loop"""
        print("meep: Hi there! I'm meep, your AI companion. What's your name?")
        
        self.user_name = input("you: ").strip()
        self.ask_personality_preferences()  
        print(f"meep: It's wonderful to meet you, {self.user_name}! What would you like to chat about today? (Type 'quit' to exit)")

       

        while True:
            user_input = input(f"{self.user_name}: ")
            if user_input.lower() == 'quit':
                print(f"meep: Bye Bye {self.user_name}! Talk to you again soon <3")
                self.save_emotion_history()
                break

            emotions = await self.analyze_emotions(user_input)
            response = self.generate_response(user_input, emotions)
            

            print(f"meep: {response}")

def main():
    # DONT SQAVER THE API KEY HERE AHAHAHHAHAA
    meep = MeepChatbot(openai_key='')

    import asyncio
    asyncio.run(meep.chat())

if __name__ == "__main__":
    main()
