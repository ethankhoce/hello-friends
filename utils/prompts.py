"""
Prompt management utilities for Hello Friends app
"""

from typing import Dict, List, Optional
import re

class PromptManager:
    """Manages prompts and query processing for the chatbot"""
    
    def __init__(self):
        self.example_prompts = [
            "I have not been paid for two months",
            "My employer keeps my passport",
            "I am sick but not allowed to see a doctor",
            "I need a rest day",
            "My accommodation is overcrowded",
            "I want to change employer"
        ]
        
        self.keyword_mappings = {
            'payment': ['paid', 'salary', 'wage', 'money', 'payment', 'pay', 'unpaid'],
            'passport': ['passport', 'document', 'identity', 'id', 'papers'],
            'medical': ['sick', 'doctor', 'medical', 'health', 'hospital', 'ill', 'injury'],
            'rest': ['rest', 'day off', 'holiday', 'break', 'weekend', 'off'],
            'accommodation': ['accommodation', 'housing', 'room', 'bed', 'living', 'dormitory'],
            'employer': ['employer', 'boss', 'company', 'workplace', 'manager', 'supervisor'],
            'hours': ['hours', 'overtime', 'work time', 'working', 'shift'],
            'contract': ['contract', 'agreement', 'terms', 'conditions']
        }
    
    def get_example_prompts(self) -> List[str]:
        """Get list of example prompts for the UI"""
        return self.example_prompts
    
    def categorize_query(self, query: str) -> List[str]:
        """Categorize a query based on keywords"""
        query_lower = query.lower()
        categories = []
        
        for category, keywords in self.keyword_mappings.items():
            if any(keyword in query_lower for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ['general']
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from a query"""
        query_lower = query.lower()
        keywords = []
        
        for category, category_keywords in self.keyword_mappings.items():
            for keyword in category_keywords:
                if keyword in query_lower:
                    keywords.append(keyword)
        
        return keywords
    
    def normalize_query(self, query: str) -> str:
        """Normalize a query for better matching"""
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', query.strip())
        
        # Convert to lowercase for consistency
        normalized = normalized.lower()
        
        # Remove common stop words (basic list)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = normalized.split()
        filtered_words = [word for word in words if word not in stop_words]
        
        return ' '.join(filtered_words)
    
    def is_emergency_query(self, query: str) -> bool:
        """Check if the query indicates an emergency situation"""
        emergency_keywords = [
            'emergency', 'urgent', 'help', 'danger', 'dangerous', 'hurt', 'injured',
            'accident', 'fire', 'police', 'ambulance', 'hospital', 'serious'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in emergency_keywords)
    
    def get_response_template(self, query_type: str) -> str:
        """Get a response template based on query type"""
        templates = {
            'payment': """
## 💰 Payment Issue

**Summary:** {summary}

**Your Rights in Singapore:**
{rights}

**What You Can Do Now:**
{actions}

**Helpful Contacts:**
{contacts}

**Important:** Always keep records of your work and payments. Report non-payment to MOM within 6 months.
            """,
            'passport': """
## 📄 Passport Issue

**Summary:** {summary}

**Your Rights in Singapore:**
{rights}

**What You Can Do Now:**
{actions}

**Helpful Contacts:**
{contacts}

**Important:** Keeping someone's passport without permission is illegal in Singapore.
            """,
            'medical': """
## 🏥 Medical Issue

**Summary:** {summary}

**Your Rights in Singapore:**
{rights}

**What You Can Do Now:**
{actions}

**Helpful Contacts:**
{contacts}

**Important:** Your health and safety are protected under Singapore law.
            """,
            'general': """
## ℹ️ General Information

**Summary:** {summary}

**Your Rights in Singapore:**
{rights}

**What You Can Do Now:**
{actions}

**Helpful Contacts:**
{contacts}

**Important:** For specific legal matters, please consult MOM or a qualified lawyer.
            """
        }
        
        return templates.get(query_type, templates['general'])
    
    def format_emergency_response(self) -> str:
        """Format an emergency response"""
        return """
## 🚨 Emergency Situation

**If this is an emergency, please call immediately:**

- **Police:** 999 (for crimes, accidents, immediate danger)
- **Fire/Medical:** 995 (for fires, medical emergencies, rescue)
- **MOM Hotline:** 6438 5122 (for employment issues)

**Stay safe and get help immediately if you are in danger.**

For non-emergency issues, please ask your question again and we'll provide detailed guidance.
        """
