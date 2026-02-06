import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    """
    Client for Groq Cloud API.
    Provides extremely fast and reliable inference using Llama 3.
    """
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        # Using Llama 3 70B for high intelligence and speed on Groq
        # Fallback to 8B if desired, but 70B is excellent and free tier supports it.
        self.model_id = os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")
        
        self.client = Groq(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate text response using Groq API.
        
        Args:
            prompt (str): The input prompt.
            
        Returns:
            str: The generated text.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_id,
                temperature=0.7,
                max_tokens=1024,
            )
            
            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error calling Groq API: {e}"

if __name__ == "__main__":
    try:
        client = LLMClient()
        print(client.generate("Hello, confirm you are working."))
    except Exception as e:
        print(f"Initialization Error: {e}")
