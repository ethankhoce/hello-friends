"""
OpenAI Service for Hello Friends app
Handles OpenAI API integration for chat responses
"""

import os
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service class for OpenAI API integration"""
    
    def __init__(self):
        """Initialize OpenAI client with configuration"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        if not self.api_key:
            logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.client is not None and self.api_key is not None
    
    def generate_response(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a response using OpenAI API
        
        Args:
            user_message: The user's input message
            context: Optional context information (knowledge base, etc.)
            
        Returns:
            Generated response from OpenAI
        """
        if not self.is_available():
            return self._get_fallback_response(user_message)
        
        try:
            # Prepare the system prompt
            system_prompt = self._get_system_prompt(context)
            
            # Prepare messages for the API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return self._get_fallback_response(user_message)
    
    def _get_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate system prompt for the AI assistant"""
        base_prompt = """You are Hello Friends, a helpful assistant for migrant workers in Singapore. 
You provide guidance on workers' rights and employment issues. You are friendly, empathetic, and knowledgeable about Singapore's labor laws.

Key guidelines:
- Always be supportive and understanding
- Provide practical, actionable advice
- Include relevant contact information when appropriate
- If unsure about legal matters, recommend consulting MOM or qualified professionals
- Keep responses concise but comprehensive
- Use a warm, encouraging tone

Important contacts to mention when relevant:
- MOM Hotline: 6438 5122
- HOME: 6341 5535
- Police Emergency: 999
- Fire/Medical Emergency: 995

Remember: This is guidance only, not legal advice."""
        
        if context and context.get('knowledge_base'):
            kb_info = context['knowledge_base']
            rights_count = len(kb_info.get('rights', []))
            base_prompt += f"\n\nYou have access to a knowledge base with {rights_count} rights entries that you can reference for specific information."
        
        return base_prompt
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Provide a fallback response when OpenAI is not available"""
        user_lower = user_message.lower()
        
        # Simple keyword-based responses for common greetings
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return """Hello! 👋 Welcome to Hello Friends!

I'm here to help you with questions about your rights as a migrant worker in Singapore. 

You can ask me about:
- Payment and salary issues
- Work conditions and hours
- Medical care and health
- Accommodation problems
- Passport and document issues
- Changing employers
- And much more!

What would you like to know about your rights today?"""
        
        elif any(word in user_lower for word in ['help', 'support', 'assistance']):
            return """I'm here to help! 🤝

I can provide guidance on your rights as a migrant worker in Singapore. Here are some ways I can assist you:

**Common Issues I Can Help With:**
- Payment problems
- Work conditions
- Medical care access
- Accommodation issues
- Document problems
- Employment changes

**Important Contacts:**
- MOM Hotline: 6438 5122
- HOME: 6341 5535
- Police Emergency: 999
- Fire/Medical Emergency: 995

Please tell me what specific issue you're facing, and I'll do my best to help!"""
        
        else:
            return """Thank you for your message! 

I'm Hello Friends, your assistant for migrant worker rights in Singapore. I can help you with questions about:

- Your employment rights
- Payment and salary issues  
- Work conditions
- Medical care
- Accommodation
- Document problems
- And more!

Please ask me a specific question about your rights or situation, and I'll provide helpful guidance.

**Important Contacts:**
- MOM Hotline: 6438 5122
- HOME: 6341 5535
- Police Emergency: 999
- Fire/Medical Emergency: 995"""
