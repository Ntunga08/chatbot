# Chatbot API

A Django-based chatbot API powered by Google AI (Gemini) that provides intelligent conversational responses.

## Features

- 🤖 **Google AI Integration**: Powered by Gemini Pro model
- 💬 **Conversation Context**: Maintains conversation history for contextual responses
- 🌐 **RESTful API**: Clean REST endpoints for easy integration
- 🎨 **Modern UI**: Beautiful web interface for testing
- 🔒 **Secure**: CSRF protection and proper error handling

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Google AI API Key
Create a `.env` file in the project root and add your Google AI API key:
```bash
echo "GOOGLE_AI_API_KEY=your_api_key_here" > .env
```

**Important**: Never commit your API key to version control. The `.env` file is already in `.gitignore`.

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Start the Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Web Interface**: http://localhost:8000/
- **API Health Check**: http://localhost:8000/api/health/

## API Endpoints

### Chat Interface
- **URL**: `/`
- **Method**: `GET`
- **Description**: Web interface for testing the chatbot

### Simple Chat
- **URL**: `/api/chat/`
- **Method**: `POST`
- **Body**:
```json
{
    "message": "Hello, how are you?"
}
```

### Chat with Context
- **URL**: `/api/chat/with-context/`
- **Method**: `POST`
- **Body**:
```json
{
    "message": "What did I just ask you?",
    "conversation_history": []
}
```

### Health Check
- **URL**: `/api/health/`
- **Method**: `GET`
- **Response**:
```json
{
    "status": "healthy",
    "message": "Chatbot API is running with Google AI (Gemini)"
}
```

## Usage Examples

### Using cURL
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a joke"}'
```

### Using JavaScript/Fetch
```javascript
const response = await fetch('/api/chat/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        message: 'Hello, how are you?'
    })
});

const data = await response.json();
console.log(data.response);
```

## Project Structure

```
chatbot/
├── app_name/
│   ├── templates/
│   │   └── app_name/
│   │       └── chat.html          # Web interface
│   ├── views.py                   # API views
│   ├── urls.py                    # App URLs
│   └── ...
├── chatbot/
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URLs
│   └── ...
├── requirements.txt               # Dependencies
├── manage.py                      # Django management
└── README.md                      # This file
```

## Security Notes

- For production, use environment variables to store your API key
- CORS is enabled for all origins in development
- CSRF protection is enabled for POST requests

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing message)
- `429`: Too Many Requests (quota exceeded)
- `500`: Internal Server Error (API issues)

## License

This project is open source and available under the MIT License. 