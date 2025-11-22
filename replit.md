# Overview

This is a Streamlit-based chatbot application powered by Google Gemini AI. The application provides a conversational interface where users can interact with the Gemini 2.5 Flash model through a web-based chat UI. The app maintains conversation context across multiple messages and streams responses in real-time for a more interactive experience.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses Streamlit as the web framework, providing a simple yet effective chat interface. Key architectural decisions include:

**Streamlit Session State for Chat History**
- **Problem**: Need to maintain conversation context across user interactions
- **Solution**: Utilize Streamlit's session state to store message history as a list of dictionaries with role and content
- **Rationale**: Session state persists data across Streamlit reruns, enabling stateful conversations without external storage
- **Pros**: Simple implementation, no database required for basic functionality
- **Cons**: Chat history is lost when session ends or page refreshes

**Chat Message Display Pattern**
- **Problem**: Need to display both historical and new messages in a conversational format
- **Solution**: Iterate through session state messages and use Streamlit's `st.chat_message()` component
- **Rationale**: Provides a familiar chat UI pattern with clear role differentiation
- **Pros**: Built-in UI component with good UX, minimal custom CSS needed
- **Cons**: Limited customization options compared to custom HTML/CSS

**Streaming Response Display**
- **Problem**: Long AI responses create poor user experience with delayed output
- **Solution**: Use placeholder component with incremental updates during streaming
- **Rationale**: Provides immediate feedback and reduces perceived latency
- **Implementation**: Message placeholder updates progressively with streaming chunks, shows cursor (▌) during generation
- **Pros**: Better user experience, shows processing is happening
- **Cons**: Requires careful state management to avoid flickering

## Backend Architecture

**Gemini AI Integration**
- **Problem**: Need to integrate with Google's Gemini AI model
- **Solution**: Use Google's `genai` Python SDK with direct API key authentication
- **Rationale**: Chosen Gemini Developer API over Vertex AI for simpler setup and authentication
- **Pros**: Simpler authentication flow, suitable for prototyping and small-scale applications
- **Cons**: May have different rate limits or features compared to Vertex AI enterprise solution
- **Alternatives Considered**: Vertex AI (more complex setup, enterprise-focused)

**Conversation Context Management**
- **Problem**: Need to send conversation history to maintain context in multi-turn conversations
- **Solution**: Convert session state messages to Gemini's `Content` format with appropriate roles
- **Rationale**: Gemini API requires specific message format with role mapping (user/model)
- **Implementation**: Transform stored messages from simple dicts to typed `Content` objects with `Part` components
- **Pros**: Maintains conversation context, enables coherent multi-turn dialogues
- **Cons**: Message history grows unbounded (no truncation strategy visible)

**Model Selection**
- **Choice**: Using `gemini-2.5-flash` model
- **Rationale**: Latest stable Flash model offers fast responses suitable for chat applications
- **Trade-offs**: Balanced speed and quality, appropriate for conversational use cases

## Configuration Management

**API Key Handling**
- **Problem**: Secure storage and access of Gemini API credentials
- **Solution**: Environment variable `GEMINI_API_KEY` stored as Replit secret
- **Rationale**: Follows security best practices by keeping secrets out of code
- **Pros**: Secure, easily configurable across environments
- **Cons**: Requires proper environment setup in deployment

# Features Implemented

## Core MVP Features
- ✅ Chat interface with message history display and user input field
- ✅ Integration with Google Gemini API for AI responses
- ✅ Conversation context management to maintain chat history
- ✅ Session state management for persistent chat within a session
- ✅ Clean, user-friendly chat UI with message bubbles for user and AI
- ✅ Real-time streaming responses from Gemini
- ✅ Clear chat functionality via sidebar button
- ✅ Message counter showing total messages in conversation

# External Dependencies

## Third-Party Services

**Google Gemini AI API**
- **Purpose**: Large language model for generating conversational responses
- **Integration**: Direct API calls via `google.genai` Python SDK
- **Authentication**: API key-based authentication using Gemini Developer API
- **Model**: gemini-2.5-flash (latest stable fast model)
- **Features Used**: Multi-turn conversation support, streaming responses

## Python Packages

**Streamlit**
- **Purpose**: Web application framework for the chat interface
- **Key Features Used**: 
  - Session state management
  - Chat components (`st.chat_message`, `st.chat_input`)
  - Page configuration
  - Layout management
  - Sidebar controls

**google-genai**
- **Purpose**: Official Google SDK for Gemini API integration
- **Key Components Used**:
  - `genai.Client` for API client initialization
  - `types.Content` and `types.Part` for message formatting
  - Streaming content generation via `generate_content_stream()`

## Environment Variables

**GEMINI_API_KEY**
- Required for authentication with Gemini API
- Must be obtained from Google AI Studio / Gemini Developer Console
- Critical for application functionality
- Stored securely as Replit secret

# Recent Changes

## November 22, 2025
- Initial implementation of Streamlit chatbot with Gemini AI integration
- Configured streaming responses for better user experience
- Added sidebar with clear chat functionality and message counter
- Implemented full conversation context management
- Successfully tested end-to-end functionality with playwright testing
- Updated model from gemini-2.0-flash-exp to gemini-2.5-flash for better stability
