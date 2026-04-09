import google.generativeai as genai
import json
import os
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class ContentResearcher:
    """
    Advanced Viral Content DNA Engine.
    Implements: Hook -> Problem -> Insight -> Payoff structure.
    """
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_viral_script(self, niche):
        """
        Generates a high-performance viral script based on the 'Evolution System' DNA.
        Niches: 'beauty' (Transformation) or 'hormones' (Women's Health)
        """
        if niche == 'beauty':
            prompt = """
            Act as a Viral Beauty Growth Strategist. 
            Goal: Create a 'Transformation' Reel script that STOPS THE SCROLL.
            
            DNA STRUCTURE (CRITICAL):
            1. HOOK (1-2s): Must be bold, contrarian, or high-stakes. 
               Examples: "Your expensive serum is doing nothing," "Stop washing your face like this."
            2. PROBLEM: Relatable pain point about skin/beauty transformation.
            3. INSIGHT: The 'Royalle Source' authority secret (Expert-level beauty hack).
            4. PAYOFF: The 'Before vs After' vision or the final solution.
            
            Tone: Bold, engaging, concise, and executive. 
            NEVER be neutral or overly educational.
            
            RETURN JSON ONLY:
            {
                "title": "Beauty Transformation DNA",
                "hook": "...",
                "problem": "...",
                "insight": "...",
                "payoff": "...",
                "mood_keywords": ["Luxury Skin", "Macro Glow", "Transformation Cut"]
            }
            """
        elif niche == 'hormones':
            prompt = """
            Act as an Authority in Women's Hormone Health.
            Goal: Create a 'Pattern Interrupt' script for Women's Health.
            
            DNA STRUCTURE (CRITICAL):
            1. HOOK (1-2s): "If you're over 30, read this," "Why you're still tired..."
            2. PROBLEM: The hidden hormone struggle no one talks about.
            3. INSIGHT: The contrarian health fact (The pattern interrupt).
            4. PAYOFF: The solution for radical health transformation.
            
            Tone: Supportive but BOLD. Authoritative. Exciting.
            
            RETURN JSON ONLY:
            {
                "title": "Hormones Evolution DNA",
                "hook": "...",
                "problem": "...",
                "insight": "...",
                "payoff": "...",
                "mood_keywords": ["Wellness Aura", "Scientific Insight", "Morning Light"]
            }
            """
        else:
            return None

        response = self.model.generate_content(prompt)
        try:
            content_text = response.text
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            
            return json.loads(content_text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return None

if __name__ == "__main__":
    researcher = ContentResearcher()
    print("Testing Beauty DNA...")
    print(researcher.generate_viral_script('beauty'))
    print("\nTesting Hormone DNA...")
    print(researcher.generate_viral_script('hormones'))
