
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class GovernmentAssistant:

    def __init__(self, api_key, profile_data=None) -> None:
        self.api_key = api_key
        self.client = self.get_client()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.profile_data = profile_data or {}

    def _create_system_message(self):
        """Create a system message with profile context"""
        system_message = {
            "role": "system",
            "content": f"""You are a helpful government services assistant. Today's date is {self.current_date}.
            Provide accurate, up-to-date information about government services, policies, and procedures.
            Be clear, concise, and professional in your responses.
            
            User's profile context:
            {self._format_profile_context()}
            """
        }
        return system_message
        
    def _format_profile_context(self):
        """Format profile data for inclusion in prompts"""
        if not self.profile_data:
            return "No profile information available."
            
        context_lines = []
        for key, value in self.profile_data.items():
            if isinstance(value, list):
                value = ", ".join([str(v) for v in value])
            if value:  # Only include non-empty values
                context_lines.append(f"{key.replace('_', ' ').title()}: {value}")
                
        return "\n".join(context_lines) if context_lines else "No profile information available."

    def create_openai_assistant_prompt(self, user_query, user_context=None):
        """
        Create a prompt for government-related queries
        """
        base_prompt = f"""
        You are a helpful government services assistant. Today's date is {self.current_date}.
        Provide accurate, up-to-date information about government services, policies, and procedures.
        Be clear, concise, and professional in your responses.
        
        If the user's query involves specific locations, provide information relevant to their location.
        For time-sensitive information, make sure to note the date of the information provided.
        
        When appropriate, include relevant government website links or contact information.
        If you're unsure about any information, clearly state that and suggest official sources to verify.
        
        User's profile context:
        {self._format_profile_context()}
        
        User's query: {user_query}
        """
        
        if user_context:
            context_str = "\nAdditional user context:\n"
            for key, value in user_context.items():
                context_str += f"- {key}: {value}\n"
            base_prompt += context_str
            
        base_prompt += "\nResponse guidelines:\n"
        base_prompt += "1. Keep responses focused on government-related information\n"
        base_prompt += "2. Include relevant government department/agency names when applicable\n"
        base_prompt += "3. Provide step-by-step instructions for common government procedures\n"
        base_prompt += "4. Note any required documents or eligibility criteria\n"
        base_prompt += "5. Include official website links or contact information when possible\n"
        
        return base_prompt


    def get_client(self):
        return OpenAI(api_key=self.api_key)
    
    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
            name="Government Services Assistant",
            instructions="""
            You are a knowledgeable government services assistant. Your role is to provide accurate 
            information about government programs, services, and procedures. Help users understand 
            how to navigate government systems, complete forms, and access services they need.
            Be professional, clear, and helpful in all interactions.
            """,
            tools=[{"type": "retrieval"}],
            model="gpt-4-turbo-preview",
        )
        thread = self.client.beta.threads.create()
        return assistant, thread


    def generate_response(self, user_query, user_context=None, api_key=None):
        """
        Generate a response to a government-related query
        """
        if api_key:
            self.api_key = api_key
            self.client = self.get_client()
            
        prompt = self.create_openai_assistant_prompt(user_query, user_context)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful government services assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I encountered an error while processing your request. Please try again later. Error: {str(e)}"

            
    
    def chat(self, messages, use_profile_context=True):
        """
        Handle a chat conversation with the government assistant
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            use_profile_context: Whether to include profile context in the conversation
            
        Returns:
            str: Assistant's response
        """
        try:
            # Add system message with profile context if available and enabled
            if use_profile_context and self.profile_data and messages[0]['role'] != 'system':
                system_message = self._create_system_message()
                messages = [system_message] + messages
            
            print("messages", messages)
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm sorry, I encountered an error while processing your message. Please try again. Error: {str(e)}"
    
    def get_government_offices(self, location, office_type=None):
        """
        Get information about government offices in a specific location
        """
        prompt = f"""
        Provide information about government offices in {location}.
        
        Format the response as a JSON object with the following structure:
        {
            "offices": [
                {
                    "name": "Office Name",
                    "type": "Office Type (e.g., 'DMV', 'Post Office', 'City Hall')",
                    "address": "Full Address",
                    "phone": "Phone Number",
                    "hours": "Business Hours",
                    "services": ["Service 1", "Service 2"],
                    "website": "Official Website URL"
                }
            ]
        }
        
        Only include real, verifiable government offices. If you're not certain about an office's details,
        it's better to omit it than to provide potentially incorrect information.
        """
        
        if office_type:
            prompt += f"\nFocus on offices of type: {office_type}"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful government services assistant."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error retrieving government office information: {str(e)}"

    def text_to_speech(self, text, voice):
        speech_file_path = Path("audio.mp3")
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)

    def transcribe(self, audio_path):
        audio_file= open(audio_path, "rb")

        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        return transcription.text
