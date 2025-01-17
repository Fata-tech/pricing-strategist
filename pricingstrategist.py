import streamlit as st
import openai
from datetime import datetime

# ---------------------------
# Replace these with your own OpenAI API key or relevant keys
# ---------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"

# ---------------------------
# Session State Initialization
# ---------------------------
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

if "user_feedback" not in st.session_state:
    st.session_state["user_feedback"] = []

# ---------------------------
# Mock data for competitor & market research
# In real scenario, you’d fetch or dynamically update this data
# ---------------------------
COMPETITOR_DATA = {
    "BlasterX": {
        "features": ["Remote monitoring", "AI scheduling", "Basic cost analytics"],
        "pricing": "Moderate",
        "reviews": ["Good enough", "Lacks advanced analytics"]
    },
    "BlastPro": {
        "features": ["Advanced cost analytics", "Multi-language support", "API integration"],
        "pricing": "Higher",
        "reviews": ["Great analytics but expensive", "UI could be improved"]
    }
}

MARKET_TRENDS = [
    "Increasing adoption of automation in blasting operations",
    "Growing emphasis on safety compliance",
    "Demand for real-time analytics and remote management"
]

# ---------------------------
# Helper functions
# ---------------------------
def generate_agent_response(user_prompt, conversation_history=None):
    """
    Uses OpenAI (or another LLM) to generate a natural, humanlike response 
    in the voice of a product manager for blasting software.
    """
    if conversation_history is None:
        conversation_history = []

    # Example: Using GPT-3.5 or GPT-4 in "chat" format
    messages = [
        {"role": "system", "content": "You are an empathetic, humanlike Product Manager for industrial blasting software. Offer helpful and professional guidance."}
    ]

    # Add conversation history
    for entry in conversation_history:
        messages.append({"role": entry["role"], "content": entry["content"]})

    # Add the new user prompt
    messages.append({"role": "user", "content": user_prompt})

    # Call OpenAI's Chat Completion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=messages,
        temperature=0.8,
        max_tokens=200
    )

    # Extract the assistant's message
    assistant_reply = response["choices"][0]["message"]["content"]
    
    return assistant_reply.strip()

def competitor_analysis(competitor_data):
    """
    Returns a mock competitor analysis summary from COMPETITOR_DATA.
    """
    summaries = []
    for competitor, data in competitor_data.items():
        summary = f"**{competitor}**:\n- Features: {', '.join(data['features'])}\n- Pricing: {data['pricing']}\n- Reviews: {', '.join(data['reviews'])}\n"
        summaries.append(summary)
    return "\n".join(summaries)

def market_research_insights(market_trends):
    """
    Returns a mock market trends summary from MARKET_TRENDS.
    """
    return "• " + "\n• ".join(market_trends)

def store_user_feedback(feedback_text):
    """
    Store user feedback for later analysis.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["user_feedback"].append({"timestamp": timestamp, "feedback": feedback_text})

# ---------------------------
# Streamlit UI
# ---------------------------
def main():
    st.title("AI-Powered Humanlike Product Manager Agent for Blasting Software")
    st.write("Speak or type your queries to explore new features, share feedback, or learn about competitor and market insights.")

    # --- Voice Input / Output (Pseudo-Implementation) ---
    # NOTE: For real STT/TTS integration, you would:
    # 1. Capture audio from user (e.g., using streamlit_webrtc or st_audiorec).
    # 2. Convert audio to text via a STT API (e.g., Google Cloud Speech, IBM Watson, etc.).
    # 3. Generate AI response text (below).
    # 4. Convert AI response text back to audio using TTS (e.g., ElevenLabs, Google TTS).
    # 5. Stream or play that audio response back to the user in Streamlit.
    #
    # For demonstration, we’re focusing on text-based input/output below.

    # Display conversation history
    for entry in st.session_state["conversation_history"]:
        if entry["role"] == "user":
            st.markdown(f"**User:** {entry['content']}")
        else:
            st.markdown(f"**AI Product Manager:** {entry['content']}")
    
    # Text input
    user_input = st.text_input("Your question or feedback here:", "")
    
    # Buttons for quick commands (optional)
    col1, col2, col3 = st.columns(3)
    if col1.button("Show Competitor Analysis"):
        # Summarize competitor data
        summary = competitor_analysis(COMPETITOR_DATA)
        st.write(summary)
    if col2.button("Show Market Research"):
        insights = market_research_insights(MARKET_TRENDS)
        st.write(insights)
    if col3.button("Clear Chat"):
        st.session_state["conversation_history"] = []
        st.experimental_rerun()
    
    # Submit user input
    if st.button("Send") and user_input:
        # Store user's query
        st.session_state["conversation_history"].append({"role": "user", "content": user_input})
        
        # Generate response
        ai_response = generate_agent_response(user_input, st.session_state["conversation_history"])
        
        # Store AI response in conversation history
        st.session_state["conversation_history"].append({"role": "assistant", "content": ai_response})
        
        # Display newly generated response
        st.markdown(f"**AI Product Manager:** {ai_response}")
    
    st.write("---")

    # User feedback section
    st.subheader("Submit Additional Feedback")
    feedback_text = st.text_area("Let us know your thoughts or pain points regarding the blasting software:")
    if st.button("Submit Feedback"):
        if feedback_text.strip():
            store_user_feedback(feedback_text)
            st.success("Feedback submitted! Thank you.")
        else:
            st.warning("Please enter some feedback before submitting.")

    # Display stored feedback
    st.write("### Collected Feedback")
    if len(st.session_state["user_feedback"]) > 0:
        for item in st.session_state["user_feedback"]:
            st.write(f"**{item['timestamp']}:** {item['feedback']}")
    else:
        st.write("No feedback submitted yet.")

    st.write("---")
    st.write("*This is a demo. For real STT/TTS, multi-language support, and real-time data integration, connect your APIs in the code.*")

if __name__ == "__main__":
    main()
