from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from django.conf import settings

# Configure Google AI
genai.configure(api_key=settings.GOOGLE_AI_API_KEY)

# Initialize the model - using Flash for higher free tier limits
model = genai.GenerativeModel('gemini-1.5-flash')

def chat_interface(request):
    """
    Serve the chat interface HTML page
    """
    return render(request, 'app_name/chat.html')

@api_view(['POST'])
def chat(request):
    """
    Chat API endpoint that processes user messages and returns AI responses
    """
    try:
        data = request.data
        message = data.get('message', '')
        
        if not message:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate response using Google AI
        response = model.generate_content(message)
        
        return Response({
            'message': message,
            'response': response.text,
            'status': 'success'
        })
        
    except Exception as e:
        error_message = str(e)
        
        # Handle quota errors
        if '429' in error_message and 'quota' in error_message.lower():
            return Response({
                'error': 'API quota exceeded. Please try again later.',
                'details': 'The Google AI API has reached its free tier limits.',
                'status': 'quota_exceeded'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # Handle other errors
        return Response({
            'error': 'AI service temporarily unavailable. Please try again.',
            'details': error_message,
            'status': 'api_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def chat_with_context(request):
    """
    Chat API endpoint that maintains conversation context
    """
    try:
        data = request.data
        message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        
        if not message:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create chat session with history
        chat = model.start_chat(history=conversation_history)
        
        # Generate response
        response = chat.send_message(message)
        
        # Update conversation history
        conversation_history.append({
            'role': 'user',
            'parts': [message]
        })
        conversation_history.append({
            'role': 'model',
            'parts': [response.text]
        })
        
        return Response({
            'message': message,
            'response': response.text,
            'conversation_history': conversation_history,
            'status': 'success'
        })
        
    except Exception as e:
        error_message = str(e)
        
        # Handle quota errors
        if '429' in error_message and 'quota' in error_message.lower():
            return Response({
                'error': 'API quota exceeded. Please try again later.',
                'details': 'The Google AI API has reached its free tier limits.',
                'status': 'quota_exceeded'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # Handle other errors
        return Response({
            'error': 'AI service temporarily unavailable. Please try again.',
            'details': error_message,
            'status': 'api_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    """
    return Response({
        'status': 'healthy',
        'message': 'Chatbot API is running with Google AI (Gemini Flash)'
    })
