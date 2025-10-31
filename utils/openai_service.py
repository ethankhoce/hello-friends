"""
OpenAI Service for Hello Friends app
Handles OpenAI API integration for chat responses
"""

import os
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

try:
    import streamlit as st  # type: ignore
    try:
        from streamlit.errors import StreamlitSecretNotFoundError  # type: ignore
    except ModuleNotFoundError:
        StreamlitSecretNotFoundError = Exception  # type: ignore[assignment]
except ModuleNotFoundError:  # Streamlit not installed (e.g., during local tests)
    st = None  # type: ignore
    StreamlitSecretNotFoundError = Exception  # type: ignore[assignment]


# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service class for OpenAI API integration"""
    
    def __init__(self):
        """Initialize OpenAI client with configuration"""
        secrets = self._load_streamlit_secrets()
        openai_config = secrets.get("openai", {})

        # Support both nested secrets (openai.api_key) and flat secrets (OPENAI_API_KEY)
        self.api_key = (
            os.getenv("OPENAI_API_KEY")
            or openai_config.get("api_key")
            or secrets.get("OPENAI_API_KEY")
        )
        self.model = (
            os.getenv("OPENAI_MODEL")
            or openai_config.get("model")
            or secrets.get("OPENAI_MODEL")
            or "gpt-3.5-turbo"
        )
        self.max_tokens = int(
            os.getenv("OPENAI_MAX_TOKENS")
            or openai_config.get("max_tokens")
            or secrets.get("OPENAI_MAX_TOKENS", 1000)
        )
        self.temperature = float(
            os.getenv("OPENAI_TEMPERATURE")
            or openai_config.get("temperature")
            or secrets.get("OPENAI_TEMPERATURE", 0.7)
        )
        
        if not self.api_key:
            logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

        self.last_error: Optional[str] = None

    def _load_streamlit_secrets(self) -> Dict[str, Any]:
        """Safely load Streamlit secrets if available."""
        if st is None:
            return {}

        try:
            return {key: value for key, value in st.secrets.items()}  # type: ignore[attr-defined]
        except (AttributeError, RuntimeError, StreamlitSecretNotFoundError):
            # Streamlit secrets unavailable outside Streamlit runtime
            return {}
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.client is not None and self.api_key is not None

    def get_status(self) -> Dict[str, Any]:
        """Return diagnostic information about the OpenAI client."""
        return {
            "api_key_present": bool(self.api_key),
            "client_initialized": self.client is not None,
            "model": self.model,
            "last_error": self.last_error,
        }
    
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
            logger.info("OpenAI service unavailable, using fallback for message: %s", user_message)
            self.last_error = "OpenAI client unavailable"
            return self._get_fallback_response(user_message)
        
        try:
            # Prepare the system prompt
            system_prompt = self._get_system_prompt(context)
            
            # Prepare messages for the API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            logger.info(
                "Calling OpenAI ChatCompletion model=%s max_tokens=%s temperature=%s user_message=%s",
                self.model,
                self.max_tokens,
                self.temperature,
                user_message,
            )
            logger.debug("OpenAI ChatCompletion payload: %s", messages)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            reply = response.choices[0].message.content.strip()
            logger.info("OpenAI ChatCompletion response: %s", reply)
            if hasattr(response, "usage") and response.usage is not None:
                usage = response.usage
                logger.info(
                    "OpenAI usage - prompt_tokens=%s completion_tokens=%s total_tokens=%s",
                    getattr(usage, "prompt_tokens", None),
                    getattr(usage, "completion_tokens", None),
                    getattr(usage, "total_tokens", None),
                )
            self.last_error = None
            return reply
            
        except Exception as e:
            logger.exception("Error calling OpenAI API")
            self.last_error = str(e)
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
        
        # Add knowledge base context
        if context and context.get('knowledge_base'):
            kb_info = context['knowledge_base']
            rights_count = len(kb_info.get('rights', []))
            base_prompt += f"\n\nYou have access to a knowledge base with {rights_count} rights entries that you can reference for specific information."
        
        # Add RAG context if available
        if context and context.get('retrieved_context'):
            retrieved_text = context['retrieved_context']
            base_prompt += f"\n\nRelevant information from uploaded documents:\n{retrieved_text}\n\nUse this information to provide accurate, specific guidance."
        
        # Add relevant rights context
        if context and context.get('relevant_rights'):
            rights = context['relevant_rights']
            if rights:
                base_prompt += f"\n\nRelevant rights information:\n"
                for right in rights[:3]:  # Limit to first 3 rights
                    title = right.get('title', 'Unknown')
                    summary = right.get('summary', 'No summary available')
                    base_prompt += f"- {title}: {summary}\n"
        
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
