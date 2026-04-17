"""AI Service for generating responses using OpenAI"""
import logging
import re
from typing import Optional, List, Tuple
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.lead import Lead, LeadStatus

logger = logging.getLogger(__name__)


class AIService:
    """Service for generating AI responses using OpenAI"""

    # Intent classification keywords
    HOT_KEYWORDS = [
        "buy", "purchase", "price", "cost", "pricing", "ready", "soon",
        "sign", "contract", "today", "tomorrow", "asap", "urgent",
        "budget", "approve", "decision", "now", "immediately"
    ]
    WARM_KEYWORDS = [
        "interested", "questions", "more info", "tell me", "how does",
        "compare", "demo", "trial", "meeting", "call", "discuss",
        "considering", "looking", "thinking", "maybe"
    ]
    COLD_KEYWORDS = [
        "just looking", "browsing", "curious", "not sure", "maybe later",
        "no rush", "just checking", "not interested", "pass", "unsubscribe"
    ]

    def __init__(self):
        """Initialize OpenAI client"""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured. AI responses will be fallback messages.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.system_prompt = settings.ai_system_prompt

    async def generate_response(
        self,
        lead: Lead,
        user_message: str,
        conversation_history: Optional[List[dict]] = None
    ) -> str:
        """
        Generate an AI response based on the lead's context and message.

        Args:
            lead: The lead object containing context
            user_message: The message from the user
            conversation_history: Previous messages in the conversation

        Returns:
            AI-generated response string
        """
        if not self.client:
            logger.warning("OpenAI client not available, returning fallback response")
            return self._get_fallback_response(lead, user_message)

        try:
            # Detect intent from message
            intent = self._detect_intent(user_message)

            # Build context about the lead
            lead_context = self._build_lead_context(lead)
            intent_context = self._get_intent_context(intent, lead)

            # Build messages for the API call
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": f"Lead Context:\n{lead_context}"},
                {"role": "system", "content": f"Intent Analysis:\n{intent_context}"},
            ]

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    messages.append(msg)

            # Add the user's message
            messages.append({"role": "user", "content": user_message})

            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.6,
                frequency_penalty=0.5,
            )

            ai_response = response.choices[0].message.content.strip()
            logger.info(f"Generated AI response for lead {lead.id} (intent: {intent})")

            return ai_response

        except Exception as e:
            logger.error(f"Error generating AI response: {e}", exc_info=True)
            return self._get_fallback_response(lead, user_message)

    async def generate_followup_message(self, lead: Lead) -> str:
        """
        Generate a follow-up message for an inactive lead.

        Args:
            lead: The lead to follow up with

        Returns:
            Follow-up message string
        """
        if not self.client:
            return self._get_followup_fallback(lead)

        try:
            lead_context = self._build_lead_context(lead)
            intent_hint = "HOT leads are ready to buy - push for a call/demo. WARM leads need nurturing - offer value. COLD leads need gentle check-ins."

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": f"Lead Context:\n{lead_context}"},
                {"role": "system", "content": f"Guidance: {intent_hint}"},
                {"role": "system", "content": (
                    "The lead has been inactive for a while. "
                    "Generate a friendly, non-pushy follow-up message to re-engage them. "
                    "Reference their interest if known, ask about their timeline, and offer value. "
                    "Keep it brief, conversational, and end with a question. "
                    "Match the tone to their interest level."
                )},
            ]

            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=200,
                temperature=0.8,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating follow-up message: {e}", exc_info=True)
            return self._get_followup_fallback(lead)

    async def analyze_lead_intent(self, lead: Lead, message: str) -> dict:
        """
        Analyze lead intent and return structured data.

        Args:
            lead: The lead to analyze
            message: The message to analyze

        Returns:
            Dictionary with intent classification and suggestions
        """
        intent = self._detect_intent(message)

        return {
            "intent": intent,
            "suggestions": self._get_intent_suggestions(intent),
            "should_ask_name": not lead.name,
            "should_push_conversion": intent == "hot" and lead.status != LeadStatus.CLOSED,
        }

    def _detect_intent(self, message: str) -> str:
        """
        Detect lead intent from message content.

        Args:
            message: The user's message

        Returns:
            Intent classification: 'hot', 'warm', or 'cold'
        """
        message_lower = message.lower()

        # Count keyword matches for each category
        hot_count = sum(1 for kw in self.HOT_KEYWORDS if kw in message_lower)
        warm_count = sum(1 for kw in self.WARM_KEYWORDS if kw in message_lower)
        cold_count = sum(1 for kw in self.COLD_KEYWORDS if kw in message_lower)

        # Check for name sharing (engagement signal)
        if re.search(r"(my name is|i'm|i am|call me|this is)\s+\w+", message_lower):
            warm_count += 2

        # Check for pricing questions (hot signal)
        if re.search(r"(how much|what.*cost|pricing|price|budget)", message_lower):
            hot_count += 1

        # Determine intent based on keyword counts
        if cold_count > 0 and cold_count > hot_count and cold_count > warm_count:
            return "cold"
        elif hot_count > 0 and hot_count >= warm_count:
            return "hot"
        elif warm_count > 0:
            return "warm"
        else:
            # Default based on engagement indicators
            if "?" in message or len(message) > 50:
                return "warm"
            return "cold"

    def _build_lead_context(self, lead: Lead) -> str:
        """Build context string about the lead"""
        context_parts = [
            f"Phone: {lead.phone}",
            f"Current Status: {lead.status.value.upper()}",
        ]

        if lead.name:
            context_parts.append(f"Name: {lead.name} (KNOWN - use their name naturally)")
        else:
            context_parts.append("Name: UNKNOWN - ask for their name naturally in your response")

        if lead.interest:
            context_parts.append(f"Interest: {lead.interest}")

        if lead.last_message:
            context_parts.append(f"Recent Conversation: {lead.last_message[:300]}")

        # Add conversation count hint
        if lead.status == LeadStatus.NEW:
            context_parts.append("This is likely their FIRST message - start with a warm greeting")
        elif lead.status == LeadStatus.ENGAGED:
            context_parts.append("They've engaged before - continue the conversation naturally")

        return "\n".join(context_parts)

    def _get_intent_context(self, intent: str, lead: Lead) -> str:
        """Get context about the detected intent"""
        if intent == "hot":
            return (
                "INTENT: HOT - This lead is showing strong buying signals!\n"
                "ACTIONS: Move toward conversion. Ask about timeline, offer to schedule a call/demo, discuss next steps. "
                "Be direct about value and ROI. Create subtle urgency."
            )
        elif intent == "warm":
            return (
                "INTENT: WARM - This lead is interested but needs more information.\n"
                "ACTIONS: Nurture the relationship. Answer questions, share relevant benefits, ask qualifying questions. "
                "Build trust and identify their specific needs. Ask for their name if not known."
            )
        else:
            return (
                "INTENT: COLD - This lead is just browsing or unsure.\n"
                "ACTIONS: Be helpful but not pushy. Offer value without pressure. "
                "Ask what sparked their interest. Keep it brief and friendly."
            )

    def _get_intent_suggestions(self, intent: str) -> List[str]:
        """Get suggested actions based on intent"""
        if intent == "hot":
            return [
                "Ask about their timeline",
                "Offer a demo or call",
                "Discuss pricing/budget",
                "Create urgency gently"
            ]
        elif intent == "warm":
            return [
                "Ask qualifying questions",
                "Share relevant benefits",
                "Ask for their name if unknown",
                "Offer helpful resources"
            ]
        else:
            return [
                "Keep it brief and friendly",
                "Offer value without pressure",
                "Ask what sparked their interest",
                "Leave door open for future"
            ]

    def _get_fallback_response(self, lead: Lead, user_message: str) -> str:
        """Get a fallback response when AI is not available"""
        # Detect intent for better fallback
        intent = self._detect_intent(user_message)

        # Check if user shared their name
        name_match = re.search(r"(my name is|i'm|i am|call me|this is)\s+(\w+)", user_message, re.IGNORECASE)
        if name_match and not lead.name:
            name = name_match.group(2).capitalize()
            return f"Nice to meet you, {name}! 👋 I'm Alex from CloseZap. What brings you here today? I'd love to help you find the right solution."

        name = lead.name or "there"

        if lead.status == LeadStatus.NEW:
            # First contact - ask for name naturally
            return f"Hey! 👋 Thanks for reaching out. I'm Alex, and I'd love to help you find what you're looking for. By the way, what should I call you? And what sparked your interest today?"

        elif lead.status == LeadStatus.ENGAGED:
            if intent == "hot":
                return f"Great questions, {name}! It sounds like you're ready to move forward. Would you like me to schedule a quick call to discuss pricing and next steps? I can show you exactly how CloseZap can help you achieve your goals."
            elif intent == "warm":
                return f"Thanks for the questions, {name}! Let me help clarify that. What specific aspect would you like to explore more? I'm happy to share more details or set up a demo if that would help."
            else:
                return f"No worries, {name}! I'm here whenever you're ready. Is there anything specific about CloseZap you're curious about? I'd be happy to explain how we've helped others in similar situations."

        else:  # CLOSED
            return f"Welcome back, {name}! Great to hear from you again. How can I help you today?"

    def _get_followup_fallback(self, lead: Lead) -> str:
        """Get a fallback follow-up message"""
        name = lead.name or "there"

        if lead.status == LeadStatus.ENGAGED:
            return f"Hey {name}! 👋 Just checking in - any questions about CloseZap that I can help with? I'm here whenever you're ready to take the next step."
        elif lead.status == LeadStatus.NEW:
            return f"Hi {name}! 👋 I noticed we didn't get a chance to connect. I'd love to learn more about what you're looking for. What's the best time to chat?"
        else:
            return f"Hi {name}! Hope you're doing well. Just wanted to follow up and see if there's anything new I can help you with!"