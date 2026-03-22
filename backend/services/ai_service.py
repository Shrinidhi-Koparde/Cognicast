"""
AI content generation service — uses Groq (primary) or Gemini (fallback).
"""

import json
import re
import asyncio
from config import settings

# ─── Provider Setup ────────────────────────────────────────────────
_provider = None  # "groq" or "gemini"
_groq_client = None

if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "your-groq-api-key-here":
    try:
        from groq import Groq
        _groq_client = Groq(api_key=settings.GROQ_API_KEY)
        _provider = "groq"
        print(f"[AI] Using Groq ({settings.GROQ_MODEL})")
    except Exception as e:
        print(f"[AI] Groq init failed: {e}")

if not _provider and settings.GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _provider = "gemini"
        print("[AI] Using Gemini (fallback)")
    except Exception as e:
        print(f"[AI] Gemini init failed: {e}")

if not _provider:
    print("[AI] WARNING: No AI provider configured! Set GROQ_API_KEY or GEMINI_API_KEY in .env")


# ─── Core Call Helper ──────────────────────────────────────────────
async def _call_model(prompt: str, max_retries: int = 3) -> str:
    """Call the AI model with retry logic for rate limits."""
    for attempt in range(max_retries):
        try:
            if _provider == "groq":
                # Groq uses OpenAI-compatible chat completions
                response = _groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=4096,
                )
                return response.choices[0].message.content

            elif _provider == "gemini":
                import google.generativeai as genai
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
                return response.text

            else:
                raise RuntimeError(
                    "No AI provider configured. Add GROQ_API_KEY or GEMINI_API_KEY to your .env file."
                )

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate" in error_str.lower() or "ResourceExhausted" in error_str:
                wait_time = (attempt + 1) * 10
                print(f"[RATE LIMIT] Attempt {attempt+1}/{max_retries}. Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                if attempt < max_retries - 1:
                    print(f"[AI ERROR] Attempt {attempt+1}: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    raise

    raise RuntimeError("AI API failed after all retries. Please try again later.")


def _parse_json_response(text: str) -> any:
    """Extract JSON from an AI response that may contain markdown fences."""
    # Try to find JSON in code blocks first
    match = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?```", text)
    if match:
        text = match.group(1)
    # Clean up and parse
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


# ─── Prompts ───────────────────────────────────────────────────────
MODE_PROMPTS = {
    "kids": "Explain like you're telling a fun story to a 10-year-old. Use simple words, analogies, and make it exciting and engaging.",
    "student": "Explain at a college-student level. Be clear, thorough, and use examples. Balance depth with accessibility.",
    "exam": "Be concise and exam-focused. Highlight key concepts, formulas, definitions, and important points. Prioritize what's most likely to be tested.",
}


# ─── Generation Functions ──────────────────────────────────────────
async def generate_conversation(chunks: list[str], mode: str = "student") -> list[dict]:
    """
    Generate a two-person conversational podcast script.
    Returns: [{"speaker": "student"|"mentor", "text": "..."}]
    """
    mode_instruction = MODE_PROMPTS.get(mode, MODE_PROMPTS["student"])
    content_text = "\n\n".join(chunks[:5])

    prompt = f"""You are creating a conversational podcast script between a Student and a Mentor.
The Student asks curious questions, and the Mentor explains concepts clearly.

Style instruction: {mode_instruction}

Based on the following academic content, create an engaging conversation with 10-16 turns.
Each turn should feel natural, like a real podcast discussion.
The Student should ask follow-up questions and sometimes share their understanding (which the Mentor can correct or build upon).

Content:
{content_text}

Return ONLY a JSON array in this exact format (no other text):
[
  {{"speaker": "student", "text": "..."}},
  {{"speaker": "mentor", "text": "..."}},
  ...
]"""

    response_text = await _call_model(prompt)
    result = _parse_json_response(response_text)

    if result and isinstance(result, list):
        return result

    # Fallback
    return [
        {"speaker": "student", "text": "Can you explain the main concepts from this material?"},
        {"speaker": "mentor", "text": f"Of course! Let me walk you through the key ideas. {chunks[0][:500]}..."},
    ]


async def generate_summary(chunks: list[str]) -> str:
    """Generate a concise summary of the content."""
    content_text = "\n\n".join(chunks[:5])

    prompt = f"""Summarize the following academic content in a clear, well-structured format.
Use bullet points and headers where appropriate. Keep it concise but comprehensive.

Content:
{content_text}

Return ONLY the summary text in markdown format."""

    response_text = await _call_model(prompt)
    return response_text.strip()


async def generate_cheat_sheet(chunks: list[str]) -> str:
    """Generate a cheat sheet with key formulas, definitions, and concepts."""
    content_text = "\n\n".join(chunks[:5])

    prompt = f"""Create a cheat sheet from the following academic content.
Include: key definitions, important formulas, critical concepts, and quick-reference points.
Format it as a compact, scannable reference sheet using markdown.

Content:
{content_text}

Return ONLY the cheat sheet in markdown format."""

    response_text = await _call_model(prompt)
    return response_text.strip()


async def generate_flashcards(chunks: list[str]) -> list[dict]:
    """Generate flashcards from content."""
    content_text = "\n\n".join(chunks[:5])

    prompt = f"""Create 8-12 flashcards from the following academic content.
Each flashcard should have a question/concept on the front and the answer/explanation on the back.

Content:
{content_text}

Return ONLY a JSON array in this exact format (no other text):
[
  {{"front": "What is...?", "back": "It is..."}},
  ...
]"""

    response_text = await _call_model(prompt)
    result = _parse_json_response(response_text)

    if result and isinstance(result, list):
        return result

    return [{"front": "Error generating flashcards", "back": "Please try again"}]


async def generate_quiz(chunks: list[str]) -> list[dict]:
    """Generate MCQ quiz questions."""
    content_text = "\n\n".join(chunks[:5])

    prompt = f"""Create 5-10 multiple choice questions from the following academic content.
Each question should have 4 options with exactly one correct answer.
Include a brief explanation for the correct answer.

Content:
{content_text}

Return ONLY a JSON array in this exact format (no other text):
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_index": 0,
    "explanation": "..."
  }},
  ...
]"""

    response_text = await _call_model(prompt)
    result = _parse_json_response(response_text)

    if result and isinstance(result, list):
        return result

    return []


async def answer_question(question: str, context: str) -> str:
    """Answer a user's doubt based on session context."""
    prompt = f"""You are a knowledgeable academic mentor. A student has a question about the material they've been studying.

Context from the study material:
{context[:3000]}

Student's question: {question}

Provide a clear, helpful, and accurate answer. If the question is not related to the context, still try to help but mention that it may be outside the scope of the current material."""

    response_text = await _call_model(prompt)
    return response_text.strip()
