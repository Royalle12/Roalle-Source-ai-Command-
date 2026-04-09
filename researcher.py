from viral_frameworks import get_strategy_prompt, VIRAL_FRAMEWORKS
import google.generativeai as genai
import json
import os
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class ContentResearcher:
    """
    General Hendricks Universal Intelligence OS.
    Implements advanced Viral DNA across ANY niche.
    """
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_viral_script(self, niche="wellness", goal="engagement", strategy="hormozi_unit"):
        """
        Universal script generator.
        Args:
            niche: Any niche or product (e.g., 'hormone health', 'SaaS for builders')
            goal: 'sales', 'engagement', 'educational', 'ugc'
            strategy: 'hormozi_unit', 'mrbeast_momentum', 'executive_luxury'
        """
        strategy_prompt = get_strategy_prompt(strategy)
        
        prompt = f"""
        Act as a World-Class Viral Content Strategist for General Hendricks.
        Your goal is to create a script for a {goal} focused ad/content in the '{niche}' niche.
        
        {strategy_prompt}
        
        DNA REQUIREMENTS:
        1. Every script must have a 'Pattern Interrupt' visual cue.
        2. The language must be bold, executive, and zero-fluff.
        3. Prioritize 'Wisdom Sharing' over 'Education'.
        
        RETURN JSON ONLY:
        {{
            "title": "Universal Viral DNA",
            "hook": "...",
            "problem": "...",
            "insight": "...",
            "payoff": "...",
            "cta": "...",
            "mood_keywords": ["keyword1", "keyword2", "keyword3"],
            "strategy_used": "{strategy}"
        }}
        """

        response = self.model.generate_content(prompt)
        try:
            content_text = response.text
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            
            return json.loads(content_text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return None

    def generate_from_url(self, url_content, goal="sales", strategy="hormozi_unit"):
        """
        URL Intelligence: Distills a viral script from raw web content.
        """
        strategy_prompt = get_strategy_prompt(strategy)
        
        prompt = f"""
        Act as the General Hendricks Intelligence Engine.
        Scan the following raw web content and extract the most 'Viral' wisdom for a {goal} ad.
        
        CONTENT SOURCE:
        {url_content[:4000]}  # Limit content size
        
        {strategy_prompt}
        
        TRANSFORM this intelligence into a high-converting viral script.
        
        RETURN JSON ONLY:
        {{
            "title": "Intelligence Engine Output",
            "hook": "...",
            "problem": "...",
            "insight": "...",
            "payoff": "...",
            "cta": "...",
            "mood_keywords": ["keyword1", "keyword2"],
            "strategy_used": "{strategy}"
        }}
        """

        response = self.model.generate_content(prompt)
        try:
            content_text = response.text
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            return json.loads(content_text)
        except Exception as e:
            print(f"Error generating from URL: {e}")
            return None

if __name__ == "__main__":
    researcher = ContentResearcher()
    print("Testing Universal Niche (SaaS)...")
    print(researcher.generate_viral_script('SaaS for Architects', 'sales', 'mrbeast_momentum'))
