"""
Knowledge Base Loader for Hello Friends app
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class KnowledgeBaseLoader:
    """Loads and manages the knowledge base for migrant worker rights"""
    
    def __init__(self, kb_path: str = "kb/rights_sg.yaml"):
        self.kb_path = Path(kb_path)
        self._knowledge_base = None
    
    def load_knowledge_base(self) -> Dict:
        """Load the knowledge base from YAML file"""
        if self._knowledge_base is None:
            try:
                with open(self.kb_path, 'r', encoding='utf-8') as file:
                    self._knowledge_base = yaml.safe_load(file)
                logger.info(f"Loaded knowledge base from {self.kb_path}")
            except FileNotFoundError:
                logger.error(f"Knowledge base file not found: {self.kb_path}")
                self._knowledge_base = self._get_default_kb()
            except yaml.YAMLError as e:
                logger.error(f"Error parsing YAML file: {e}")
                self._knowledge_base = self._get_default_kb()
        
        return self._knowledge_base
    
    def _get_default_kb(self) -> Dict:
        """Return a default knowledge base if file loading fails"""
        return {
            "rights": [
                {
                    "id": "default",
                    "title": "General Information",
                    "categories": ["general"],
                    "summary": "For specific help, please contact MOM or NGOs",
                    "details": "Please contact the Ministry of Manpower at 6438 5122 or NGOs like HOME (6341 5535) for assistance.",
                    "contacts": [
                        {
                            "name": "Ministry of Manpower (MOM)",
                            "phone": "6438 5122",
                            "description": "Government agency for employment matters"
                        }
                    ]
                }
            ],
            "disclaimers": [
                {
                    "text": "This information is for general guidance only and does not constitute legal advice."
                }
            ],
            "emergency_contacts": [
                {
                    "name": "Police Emergency",
                    "phone": "999",
                    "description": "For crimes, accidents, or immediate danger"
                }
            ]
        }
    
    def get_rights_by_category(self, category: str) -> List[Dict]:
        """Get rights that match a specific category"""
        kb = self.load_knowledge_base()
        rights = kb.get('rights', [])
        return [right for right in rights if category in right.get('categories', [])]
    
    def get_right_by_id(self, right_id: str) -> Optional[Dict]:
        """Get a specific right by its ID"""
        kb = self.load_knowledge_base()
        rights = kb.get('rights', [])
        for right in rights:
            if right.get('id') == right_id:
                return right
        return None
    
    def search_rights(self, query: str) -> List[Dict]:
        """Search rights based on query text"""
        kb = self.load_knowledge_base()
        rights = kb.get('rights', [])
        query_lower = query.lower()
        
        matching_rights = []
        for right in rights:
            # Search in title, summary, and details
            if (query_lower in right.get('title', '').lower() or
                query_lower in right.get('summary', '').lower() or
                query_lower in right.get('details', '').lower()):
                matching_rights.append(right)
        
        return matching_rights
    
    def get_emergency_contacts(self) -> List[Dict]:
        """Get emergency contact information"""
        kb = self.load_knowledge_base()
        return kb.get('emergency_contacts', [])
    
    def get_disclaimers(self) -> List[Dict]:
        """Get disclaimer information"""
        kb = self.load_knowledge_base()
        return kb.get('disclaimers', [])
    
    def reload_knowledge_base(self):
        """Force reload the knowledge base from file"""
        self._knowledge_base = None
        return self.load_knowledge_base()
