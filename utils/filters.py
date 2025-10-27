"""
Response filtering and formatting utilities for Hello Friends app
"""

from typing import Dict, List, Optional
import re

class ResponseFilter:
    """Handles response filtering and formatting for the chatbot"""
    
    def __init__(self):
        self.disclaimer_text = "⚠️ **Disclaimer:** This information is for general guidance only and does not constitute legal advice. For specific legal matters, please consult a qualified lawyer or contact MOM directly."
    
    def format_response(self, query: str, relevant_rights: List[Dict]) -> str:
        """Format a response based on query and relevant rights"""
        
        if not relevant_rights:
            return self._format_no_results_response()
        
        # Use the first relevant right as primary response
        primary_right = relevant_rights[0]
        
        # Extract key information
        summary = primary_right.get('summary', 'No summary available')
        details = primary_right.get('details', 'No details available')
        contacts = primary_right.get('contacts', [])
        
        # Format the response
        response = f"""
## 📋 {primary_right.get('title', 'Information')}

**Summary:** {summary}

**Your Rights in Singapore:**
{self._extract_rights_from_details(details)}

**What You Can Do Now:**
{self._extract_actions_from_details(details)}

**Helpful Contacts:**
{self._format_contacts(contacts)}

{self.disclaimer_text}
        """
        
        # Add additional relevant rights if available
        if len(relevant_rights) > 1:
            response += "\n\n---\n\n"
            response += "**Related Information:**\n"
            for right in relevant_rights[1:3]:  # Show max 2 additional rights
                response += f"- [{right.get('title', 'Information')}]({right.get('id', '#')})\n"
        
        return response.strip()
    
    def _extract_rights_from_details(self, details: str) -> str:
        """Extract rights information from details text"""
        lines = details.split('\n')
        rights_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('**Your Rights:**') or line.startswith('**Rights:**'):
                continue
            elif line.startswith('**') and '**' in line[2:]:
                if any(keyword in line.lower() for keyword in ['right', 'entitle', 'should', 'can']):
                    rights_lines.append(line)
            elif line.startswith('- ') and any(keyword in line.lower() for keyword in ['right', 'entitle', 'should', 'can']):
                rights_lines.append(line)
        
        if rights_lines:
            return '\n'.join(rights_lines[:5])  # Limit to 5 rights
        else:
            return "Please refer to the detailed information below for your specific rights."
    
    def _extract_actions_from_details(self, details: str) -> str:
        """Extract actionable steps from details text"""
        lines = details.split('\n')
        action_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('**What You Can Do:**') or line.startswith('**Actions:**'):
                continue
            elif line.startswith('**') and '**' in line[2:]:
                if any(keyword in line.lower() for keyword in ['do', 'action', 'step', 'contact', 'report']):
                    action_lines.append(line)
            elif line.startswith('- ') and any(keyword in line.lower() for keyword in ['do', 'action', 'step', 'contact', 'report']):
                action_lines.append(line)
            elif re.match(r'^\d+\.', line):  # Numbered list items
                action_lines.append(line)
        
        if action_lines:
            return '\n'.join(action_lines[:5])  # Limit to 5 actions
        else:
            return "Please refer to the detailed information below for specific steps you can take."
    
    def _format_contacts(self, contacts: List[Dict]) -> str:
        """Format contact information"""
        if not contacts:
            return "No specific contacts available. Please contact MOM at 6438 5122 for general assistance."
        
        formatted_contacts = []
        for contact in contacts[:3]:  # Limit to 3 contacts
            name = contact.get('name', 'Unknown')
            phone = contact.get('phone', '')
            description = contact.get('description', '')
            
            contact_text = f"**{name}**"
            if phone:
                contact_text += f" - {phone}"
            if description:
                contact_text += f" ({description})"
            
            formatted_contacts.append(contact_text)
        
        return '\n'.join(formatted_contacts)
    
    def _format_no_results_response(self) -> str:
        """Format response when no relevant rights are found"""
        return f"""
## ❓ No Specific Information Found

**Summary:** We couldn't find specific information for your query, but we can still help.

**What You Can Do Now:**
1. **Contact MOM directly** at 6438 5122 for employment-related issues
2. **Call HOME** at 6341 5535 for general migrant worker support
3. **Contact TWC2** at 6297 7561 for assistance with work-related problems
4. **Try rephrasing your question** with more specific details

**Emergency Contacts:**
- **Police:** 999 (for crimes, accidents, immediate danger)
- **Fire/Medical:** 995 (for fires, medical emergencies, rescue)

{self.disclaimer_text}
        """
    
    def sanitize_response(self, response: str) -> str:
        """Sanitize response text for safe display"""
        # Remove any potentially harmful HTML/script tags
        response = re.sub(r'<script.*?</script>', '', response, flags=re.DOTALL | re.IGNORECASE)
        response = re.sub(r'<[^>]*>', '', response)  # Remove HTML tags
        
        # Limit response length
        if len(response) > 2000:
            response = response[:2000] + "...\n\n*Response truncated for readability*"
        
        return response
    
    def add_source_attribution(self, response: str, sources: List[str]) -> str:
        """Add source attribution to response"""
        if not sources:
            return response
        
        attribution = "\n\n**Sources:**\n"
        for source in sources:
            attribution += f"- {source}\n"
        
        return response + attribution
    
    def format_error_response(self, error_message: str) -> str:
        """Format an error response"""
        return f"""
## ⚠️ Error

**Something went wrong:** {error_message}

**Please try again or contact support:**
- **MOM Hotline:** 6438 5122
- **HOME:** 6341 5535

{self.disclaimer_text}
        """
