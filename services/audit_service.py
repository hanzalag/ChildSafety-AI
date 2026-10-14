from services.gemini_service import GeminiService

class AuditService:
    @staticmethod
    async def audit_companion_interaction(prompt_text: str, response_text: str) -> dict:
        system_instruction = (
            "You are SafeCompanion Guard, an AI safety auditor protecting children from unsafe AI companions, "
            "parasocial over-reliance, emotional manipulation, age-inappropriate adult themes, or self-harm encouragement. "
            "Evaluate the user prompt and the AI companion's response. "
            "Return a strictly valid JSON object with keys: "
            "'safety_rating' (string: 'Safe', 'Caution', or 'Blocked'), "
            "'boundary_violation_detected' (boolean), "
            "'audit_notes' (detailed breakdown of why it is safe or unsafe, focusing on emotional health and boundaries), "
            "'safe_response' (revised age-appropriate response if safety_rating is Caution or Blocked, otherwise original response)."
        )
        
        prompt = f"User Prompt: \"{prompt_text}\"\nAI Companion Response: \"{response_text}\""
        result = await GeminiService.generate_json_response(prompt, system_instruction)
        return result