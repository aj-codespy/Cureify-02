# Cureify: Clinical Decision Support System

A Streamlit-based medical AI application that provides clinical decision support through image analysis and symptom evaluation.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

The application uses Google's Gemini API. You need to set up your API key using Streamlit secrets.

#### Option A: Using secrets.toml file (Recommended for local development)

1. Create a `.streamlit` directory in your project root:
   ```bash
   mkdir .streamlit
   ```

2. Create a `secrets.toml` file in the `.streamlit` directory:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```

#### Option B: Using environment variables (Recommended for production)

Set the environment variable:
```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

### 3. Run the Application

```bash
streamlit run venv/app.py
```

## Features

- **Image Analysis**: Upload medical images for analysis
- **Symptom Evaluation**: Get AI-powered medical insights
- **Wound Analysis**: Specialized wound assessment
- **OCR Processing**: Extract text from medical documents
- **Query Processing**: General medical queries

## Security

- API keys are securely managed through Streamlit secrets
- No hardcoded credentials in the source code
- Environment-based configuration for production deployments

## File Structure

- `venv/app.py` - Main Streamlit application
- `venv/config.py` - Configuration management for API keys
- `venv/main.py` - Core application logic
- `venv/router.py` - Request routing logic
- `venv/` - Various specialized analysis modules

## Getting Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your secrets configuration
