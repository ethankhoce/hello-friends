# how to run
source venv/bin/activate
streamlit run Home.py

# Hello Friends - Migrant Worker Rights Assistant

A production-ready Streamlit application providing guidance and support for migrant workers in Singapore.

## Features

- 🤝 **Multilingual Support**: English, Tamil, Bengali, Tagalog, Bahasa Indonesia
- 📁 **PDF Upload**: Admin panel for uploading documents to enhance knowledge base
- 💬 **Interactive Chat**: AI-powered chatbot for answering rights-related questions
- 📋 **Structured Responses**: Clear, non-legal summaries with actionable steps
- 🔗 **Resource Links**: Direct access to MOM, NGOs, and emergency contacts
- 🎨 **Accessible UI**: Large buttons, clear copy, and friendly tone

## Login Credentials

**Username:** `admin`  
**Password:** `HelloFriends2024!`

> **Note:** The application requires login authentication. Use the credentials above to access all features.

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run Home.py
   ```

3. **Access the App**
   Open your browser to `http://localhost:8501` and log in with the credentials above.

## Project Structure

```
hellofriends/
├── Home.py                # Main Streamlit application
├── kb/
│   └── rights_sg.yaml    # Singapore migrant worker rights knowledge base
├── rag/
│   ├── uploads/          # Directory for uploaded PDFs
│   └── README.md         # RAG implementation guide
├── utils/
│   ├── i18n.py          # Internationalization utilities
│   ├── kb_loader.py     # Knowledge base loader
│   ├── prompts.py       # Prompt management
│   └── filters.py       # Response filtering and formatting
├── assets/
│   └── logo.svg         # Application logo
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Knowledge Base

The application includes a curated knowledge base covering:

- 💰 **Payment Rights**: Salary, overtime, deductions
- 📄 **Document Rights**: Passport retention, identity documents
- 🏥 **Medical Rights**: Healthcare access, sick leave, work injuries
- 😴 **Rest Rights**: Working hours, rest days, holidays
- 🏠 **Accommodation**: Living standards, safety requirements
- 👔 **Employment**: Contract changes, employer transfers

## API Integration Ready

The application is designed to easily integrate with external APIs:

- **Current**: Simple keyword matching with local knowledge base
- **Future**: RAG with embeddings and LLM integration (OpenAI, etc.)
- **Stub Function**: `generate_response()` in `app.py` ready for enhancement

## Emergency Contacts

- **Police**: 999 (crimes, accidents, immediate danger)
- **Fire/Medical**: 995 (fires, medical emergencies, rescue)
- **MOM Hotline**: 6438 5122 (employment issues)
- **HOME**: 6341 5535 (migrant worker support)
- **TWC2**: 6297 7561 (worker assistance)

## Development

### Adding New Rights

1. Edit `kb/rights_sg.yaml`
2. Add new rights with proper categories
3. Include contacts and actionable steps
4. Restart the application

### Adding New Languages

1. Edit `utils/i18n.py`
2. Add translations for new language
3. Update language selection in `app.py`

### RAG Integration

1. Implement PDF text extraction
2. Add vector embeddings generation
3. Integrate with vector database
4. Connect to LLM API
5. Update `generate_response()` function

## Disclaimer

This application provides general guidance only and does not constitute legal advice. For specific legal matters, please consult a qualified lawyer or contact MOM directly.

## License

This project is designed to help migrant workers access information about their rights in Singapore. Please use responsibly and refer users to appropriate authorities for legal matters.
