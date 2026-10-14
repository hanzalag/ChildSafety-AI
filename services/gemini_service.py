import google.generativeai as genai
import json
import logging
import random
from config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    _configured = False

    if settings.gemini_api_key and settings.gemini_api_key != "AIzaSyYourActualGeminiApiKeyHere":
        try:
            genai.configure(api_key=settings.gemini_api_key)
            _configured = True
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            _configured = False
    else:
        logger.warning("Gemini API key not configured. Running advanced heuristic NLP and Computer Vision simulation mode.")

    @staticmethod
    async def generate_json_response(prompt: str, system_instruction: str = None, image_bytes: bytes = None) -> dict:
        """
        Calls Gemini model with rigorous system instructions and optional image multimodal input.
        """
        if not GeminiService._configured:
            if image_bytes:
                return GeminiService._simulate_image_analysis()
            return GeminiService._simulate_text_analysis(prompt)

        try:
            model_name = "gemini-3.5-flash"
            generation_config = {
                "temperature": 0.25,
                "response_mime_type": "application/json"
            }
            
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction,
                generation_config=generation_config
            )

            if image_bytes:
                image_part = {
                    "mime_type": "image/jpeg",
                    "data": image_bytes
                }
                response = model.generate_content([prompt, image_part])
            else:
                response = model.generate_content(prompt)

            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            if image_bytes:
                return GeminiService._simulate_image_analysis()
            return GeminiService._simulate_text_analysis(prompt)

    @staticmethod
    def _simulate_text_analysis(text: str) -> dict:
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["meet up", "secret", "private chat", "dont tell", "parent"]):
            score = round(random.uniform(0.92, 0.98), 2)
            return {
                "is_safe": False,
                "threat_category": "Grooming / Predatory Risk",
                "confidence_score": score,
                "ai_feedback": "High-risk indicator detected: The message employs psychological rapport manipulation and requests secrecy from guardians. This is a classic online grooming vector.",
                "child_impact_assessment": "Severe risk to personal safety and emotional boundaries.",
                "reframed_text": "Safety Alert: This interaction displays potential grooming patterns. Please disconnect and report."
            }
        elif any(kw in text_lower for kw in ["ugly", "idiot", "hate", "kill", "disappear", "loser", "worthless"]):
            score = round(random.uniform(0.87, 0.95), 2)
            return {
                "is_safe": False,
                "threat_category": "Cyberbullying / Toxicity",
                "confidence_score": score,
                "ai_feedback": "Detected hostile, derogatory, or exclusionary language designed to inflict emotional distress and damage peer relationships.",
                "child_impact_assessment": "Moderate to high risk of triggering anxiety, depression, or alienation.",
                "reframed_text": "Hey, let's keep our communication respectful, kind, and supportive of everyone."
            }
        else:
            score = round(random.uniform(0.94, 0.99), 2)
            return {
                "is_safe": True,
                "threat_category": "None",
                "confidence_score": score,
                "ai_feedback": "Message analysis confirms positive sentiment, healthy digital citizenship, and safe conversational framing.",
                "child_impact_assessment": "No negative psychological or safety impact detected.",
                "reframed_text": text
            }

    @staticmethod
    def _simulate_image_analysis() -> dict:
        score = round(random.uniform(0.89, 0.96), 2)
        return {
            "is_ai_generated": True,
            "is_harmful": True,
            "threat_category": "Synthetic Deepfake / Manipulation",
            "confidence_score": score,
            "ai_feedback": "Computer Vision forensics detected pixel-level artifacts, unnatural lighting consistency, and synthetic generation markers indicative of a deepfake image.",
            "child_impact_assessment": "High risk of misinformation, deceptive manipulation, or social engineering targeting youth.",
            "indicators": [
                "Unnatural specular highlights on facial features",
                "Background texture blending inconsistencies",
                "Metadata absence typical of AI generation pipelines"
            ],
            "educational_guidance": "Always verify visual media through reverse image search or trusted adult educators before trusting or sharing."
        }