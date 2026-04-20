import re
from typing import Optional, List

from config import Config
from database import get_db_connection

# -------------------------
# Language Detection
# -------------------------

GUJARATI_RANGE = re.compile(r"[\u0A80-\u0AFF]")
HINDI_RANGE = re.compile(r"[\u0900-\u097F]")


def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "en"
    if GUJARATI_RANGE.search(text):
        return "gu"
    if HINDI_RANGE.search(text):
        return "hi"
    return "en"


def get_language_instruction(lang: str) -> str:
    if lang == "gu":
        return "Always respond in Gujarati. Use simple, respectful language."
    if lang == "hi":
        return "Always respond in Hindi. Use simple, respectful language."
    return "Respond in English. Use simple, clear language."


# -------------------------
# Chat History (DB)
# -------------------------

def get_last_messages(user_id: int, limit: int = 5) -> List[dict]:
    """
    Returns last N conversations as:
    [
        {"role": "user", "message": "..."},
        {"role": "assistant", "message": "..."}
    ]
    """
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT message, bot_response
            FROM chat_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (user_id, limit),
        )
        rows = cursor.fetchall()
        cursor.close()

        history = []
        for row in reversed(rows):
            history.append({"role": "user", "message": row["message"]})
            if row["bot_response"]:
                history.append(
                    {"role": "assistant", "message": row["bot_response"]}
                )

        return history

    except Exception as e:
        print("History fetch error:", e)
        return []
    finally:
        conn.close()


def save_user_message(user_id: int, message: str, language: str) -> int:
    """
    Inserts user message and returns inserted row ID
    """
    conn = get_db_connection()
    if not conn:
        return -1

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO chat_history (user_id, message, language)
            VALUES (%s, %s, %s)
            """,
            (user_id, message[:4000], language),
        )
        conn.commit()
        row_id = cursor.lastrowid
        cursor.close()
        return row_id

    except Exception as e:
        print("Save user message error:", e)
        return -1
    finally:
        conn.close()


def save_bot_response(row_id: int, response: str) -> None:
    """
    Updates bot response for the latest user message
    """
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE chat_history
            SET bot_response = %s
            WHERE id = %s
            """,
            (response[:4000], row_id),
        )
        conn.commit()
        cursor.close()

    except Exception as e:
        print("Save bot response error:", e)
    finally:
        conn.close()


# -------------------------
# Gemini Integration
# -------------------------

def get_gemini_response(
    user_message: str,
    history: List[dict],
    language: str,
    api_key: str,
) -> Optional[str]:
    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        system_prompt = f"""
You are Aarohi AI, a safe and respectful women’s health assistant.

{get_language_instruction(language)}

Rules:
- Be empathetic and supportive
- Provide educational health information only
- Encourage doctor consultation when needed
- Do NOT diagnose diseases
"""

        conversation = [system_prompt.strip()]

        for h in history:
            role = "User" if h["role"] == "user" else "Assistant"
            conversation.append(f"{role}: {h['message']}")

        conversation.append(f"User: {user_message}")
        conversation.append("Assistant:")

        final_prompt = "\n\n".join(conversation)

        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=final_prompt,
        )

        if response and response.text:
            return response.text.strip()

        return "I’m sorry, I couldn’t understand that. Please try again."

    except Exception as e:
        print("Gemini API error:", e)
        return "I’m having trouble responding right now. Please try again later."


# -------------------------
# Main Chat Flow
# -------------------------

def process_chat(user_id: int, message: str, api_key: str):
    if not message or not message.strip():
        return None, "Message is required"

    language = detect_language(message)
    history = get_last_messages(user_id)

    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cursor = conn.cursor()

        # 1️⃣ Insert user message FIRST
        cursor.execute(
            """
            INSERT INTO chat_history (user_id, message, language)
            VALUES (%s, %s, %s)
            """,
            (user_id, message[:4000], language),
        )
        row_id = cursor.lastrowid
        conn.commit()

        # 2️⃣ Get Gemini response
        response = get_gemini_response(
            user_message=message,
            history=history,
            language=language,
            api_key=api_key,
        )

        if not response:
            return None, "Failed to get AI response"

        # 3️⃣ UPDATE same row → bot_response
        cursor.execute(
            """
            UPDATE chat_history
            SET bot_response = %s
            WHERE id = %s
            """,
            (response[:4000], row_id),
        )
        conn.commit()

        return response, None

    except Exception as e:
        print("Chat processing error:", e)
        return None, "Internal server error"

    finally:
        cursor.close()
        conn.close()


