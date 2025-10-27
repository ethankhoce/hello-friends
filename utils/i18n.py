"""
Internationalization (i18n) utilities for Hello Friends app
"""

from typing import Dict, List, Optional
import json
from pathlib import Path

class I18nManager:
    """Manages internationalization for the Hello Friends app"""
    
    def __init__(self):
        self.current_language = "en"
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translation files"""
        translations = {
            "en": {
                "app_title": "Hello Friends",
                "app_subtitle": "Trusted guidance for migrant-worker rights in Singapore. Not legal advice.",
                "admin_panel": "Admin Panel",
                "upload_files": "Upload PDF files for knowledge base",
                "language": "Language",
                "statistics": "Statistics",
                "chat_assistant": "Chat Assistant",
                "quick_questions": "Quick questions you can ask:",
                "ask_rights": "Ask about your rights...",
                "clear_chat": "Clear Chat",
                "finding_info": "Finding information for you...",
                "knowledge_base_entries": "Knowledge Base Entries",
                "uploaded_documents": "Uploaded Documents"
            },
            "ta": {  # Tamil
                "app_title": "வணக்கம் நண்பர்களே",
                "app_subtitle": "சிங்கப்பூரில் குடியேறுபவர் உரிமைகளுக்கான நம்பகமான வழிகாட்டுதல். சட்ட ஆலோசனை அல்ல.",
                "admin_panel": "நிர்வாக பேனல்",
                "upload_files": "அறிவு தளத்திற்கு PDF கோப்புகளை பதிவேற்றவும்",
                "language": "மொழி",
                "statistics": "புள்ளிவிவரங்கள்",
                "chat_assistant": "அரட்டை உதவியாளர்",
                "quick_questions": "நீங்கள் கேட்கக்கூடிய விரைவான கேள்விகள்:",
                "ask_rights": "உங்கள் உரிமைகளைப் பற்றி கேளுங்கள்...",
                "clear_chat": "அரட்டையை அழிக்கவும்",
                "finding_info": "உங்களுக்கான தகவலைத் தேடுகிறேன்...",
                "knowledge_base_entries": "அறிவு தள உள்ளீடுகள்",
                "uploaded_documents": "பதிவேற்றப்பட்ட ஆவணங்கள்"
            },
            "bn": {  # Bengali
                "app_title": "হ্যালো বন্ধুরা",
                "app_subtitle": "সিঙ্গাপুরে অভিবাসী কর্মীদের অধিকারের জন্য বিশ্বস্ত নির্দেশনা। আইনি পরামর্শ নয়।",
                "admin_panel": "অ্যাডমিন প্যানেল",
                "upload_files": "জ্ঞান ভান্ডারের জন্য PDF ফাইল আপলোড করুন",
                "language": "ভাষা",
                "statistics": "পরিসংখ্যান",
                "chat_assistant": "চ্যাট সহায়ক",
                "quick_questions": "আপনি জিজ্ঞাসা করতে পারেন এমন দ্রুত প্রশ্ন:",
                "ask_rights": "আপনার অধিকার সম্পর্কে জিজ্ঞাসা করুন...",
                "clear_chat": "চ্যাট সাফ করুন",
                "finding_info": "আপনার জন্য তথ্য খুঁজছি...",
                "knowledge_base_entries": "জ্ঞান ভান্ডার এন্ট্রি",
                "uploaded_documents": "আপলোড করা নথি"
            },
            "tl": {  # Tagalog
                "app_title": "Kumusta mga Kaibigan",
                "app_subtitle": "Mapagkakatiwalaang gabay para sa mga karapatan ng migrant worker sa Singapore. Hindi legal na payo.",
                "admin_panel": "Admin Panel",
                "upload_files": "Mag-upload ng PDF files para sa knowledge base",
                "language": "Wika",
                "statistics": "Mga Estadistika",
                "chat_assistant": "Chat Assistant",
                "quick_questions": "Mabilis na mga tanong na maaari mong itanong:",
                "ask_rights": "Magtanong tungkol sa inyong mga karapatan...",
                "clear_chat": "I-clear ang Chat",
                "finding_info": "Naghahanap ng impormasyon para sa inyo...",
                "knowledge_base_entries": "Knowledge Base Entries",
                "uploaded_documents": "Mga Na-upload na Dokumento"
            },
            "id": {  # Bahasa Indonesia
                "app_title": "Halo Teman-teman",
                "app_subtitle": "Panduan terpercaya untuk hak-hak pekerja migran di Singapura. Bukan nasihat hukum.",
                "admin_panel": "Panel Admin",
                "upload_files": "Upload file PDF untuk knowledge base",
                "language": "Bahasa",
                "statistics": "Statistik",
                "chat_assistant": "Asisten Chat",
                "quick_questions": "Pertanyaan cepat yang bisa Anda tanyakan:",
                "ask_rights": "Tanyakan tentang hak-hak Anda...",
                "clear_chat": "Hapus Chat",
                "finding_info": "Mencari informasi untuk Anda...",
                "knowledge_base_entries": "Entri Knowledge Base",
                "uploaded_documents": "Dokumen yang Diunggah"
            }
        }
        return translations
    
    def get_text(self, key: str, language: Optional[str] = None) -> str:
        """Get translated text for a given key"""
        lang = language or self.current_language
        return self.translations.get(lang, self.translations["en"]).get(key, key)
    
    def set_language(self, language: str):
        """Set the current language"""
        if language in self.translations:
            self.current_language = language
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def get_language_name(self, language_code: str) -> str:
        """Get the display name for a language code"""
        language_names = {
            "en": "English",
            "ta": "Tamil",
            "bn": "Bengali", 
            "tl": "Tagalog",
            "id": "Bahasa Indonesia"
        }
        return language_names.get(language_code, language_code)
