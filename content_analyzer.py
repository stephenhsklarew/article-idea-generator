import os
import sys
from typing import Dict
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Add UnifiedLLMClient to path
unified_llm_path = Path.home() / 'Development' / 'Scripts' / 'UnifiedLLMClient'
sys.path.insert(0, str(unified_llm_path))

from llm_client import get_client

class ContentAnalyzer:
    def __init__(self, content_focus=None, mode='test', model_override=None, provider_override=None):
        """
        Initialize ContentAnalyzer with specified mode.

        Args:
            content_focus: Custom content focus string
            mode: 'test' (uses Qwen 2.5 32B) or 'production' (uses Qwen 2.5 32B). Default: 'test'
            model_override: Specific model name to override mode defaults
            provider_override: Specific provider to use with model_override ('qwen', 'anthropic', 'openai', or 'google')
        """
        # If model override is specified, use it with the provider
        if model_override:
            self.model = model_override

            # If provider is explicitly specified, use it
            if provider_override:
                self.provider = provider_override.lower()
            else:
                # Auto-detect provider from model name
                if 'qwen' in model_override.lower():
                    self.provider = 'qwen'
                elif 'claude' in model_override.lower():
                    self.provider = 'claude'
                elif 'gpt' in model_override.lower() or 'o1' in model_override.lower():
                    self.provider = 'openai'
                elif 'gemini' in model_override.lower():
                    self.provider = 'google'
                else:
                    # Default to Qwen (local, free)
                    self.provider = 'qwen'

        # Mode-based configuration (only if no model override)
        elif mode == 'production':
            self.provider = 'qwen'
            self.model = 'qwen2.5:32b'
        elif mode == 'test':
            self.provider = 'qwen'
            self.model = 'qwen2.5:32b'
        else:
            # Fallback to Qwen
            self.provider = 'qwen'
            self.model = 'qwen2.5:32b'

        # Initialize the unified LLM client
        self._init_client()

        # Load filter settings
        self.excluded_people = self._parse_csv_env('EXCLUDE_PEOPLE')
        self.excluded_subjects = self._parse_csv_env('EXCLUDE_SUBJECTS')

        # Set content focus (default: AI strategy for business leaders)
        if content_focus:
            self.content_focus = content_focus
        else:
            self.content_focus = os.getenv('CONTENT_FOCUS', '').strip() or \
                               'AI strategy and innovation for business leaders'

    def _init_client(self):
        """Initialize the unified LLM client"""
        try:
            # Use UnifiedLLMClient with explicit provider
            self.client = get_client(provider=self.provider)
        except Exception as e:
            raise ValueError(f"Failed to initialize {self.provider} client: {str(e)}")

    def _parse_csv_env(self, env_var: str) -> list:
        """Parse comma-separated environment variable into list"""
        value = os.getenv(env_var, '').strip()
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]

    def should_exclude_transcript(self, transcript: Dict) -> bool:
        """Check if transcript should be excluded based on filters"""
        # Check subject line filters
        subject = transcript.get('subject', '').lower()
        for keyword in self.excluded_subjects:
            if keyword.lower() in subject:
                return True

        # Check people filters (in transcript body)
        body = transcript.get('body', '').lower()
        for person in self.excluded_people:
            if person.lower() in body:
                return True

        return False

    def _create_prompt(self, transcript: Dict) -> str:
        """Create the analysis prompt"""
        return f"""You are analyzing a conversation transcript for content focused on {self.content_focus}.

Conversation Topic: {transcript['topic']}
Date: {transcript['date']}

Transcript:
{transcript['body']}

Please analyze this transcript and provide 2-5 recommended topics. For EACH topic, include:
- A compelling topic title geared towards the audience
- 1-3 sentence description of why this would make a good article
- 2-5 KEY INSIGHTS specifically related to this topic
- 1-3 NOTABLE QUOTES that support this topic (with speaker name if identifiable)
- OPTIONAL: Evidence or supporting data that provides credible facts
- OPTIONAL: Real-world stories or perspectives mentioned in the conversation

IMPORTANT INSTRUCTIONS:
- Extract ACTUAL verbatim quotes from the transcript text
- Include the speaker's name next to each quote in the format: **[Name]:**
- Make insights actionable and specific
- Focus on content relevant to {self.content_focus}
- Include evidence/data and real-world stories when they appear in the transcript

Format your response EXACTLY as follows:

## TOPIC 1: [Topic Title]

**Description:** [1-3 sentence description of why this would make a good article for the target audience]

**Key Insights:**
• [Insight 1 related to this topic]
• [Insight 2 related to this topic]
• [Insight 3 related to this topic]
• [Insight 4 related to this topic]
• [Insight 5 related to this topic]

**Notable Quotes:**
> **[Speaker Name]:** "[Exact quote extracted verbatim from the transcript]"

> **[Speaker Name]:** "[Exact quote extracted verbatim from the transcript]"

> **[Speaker Name]:** "[Exact quote extracted verbatim from the transcript]"

**Evidence/Data:** (Optional - include if relevant data or statistics are mentioned, max 5 items)
• [Specific data point, statistic, or research finding mentioned in the conversation - 3-5 sentences max]
• [Another piece of supporting evidence - 3-5 sentences max]

**Real-World Examples:** (Optional - include if stories or examples are shared, max 5 items)
• [Real-world story, case study, or example from the conversation - 3-5 sentences max]
• [Another relevant example or perspective - 3-5 sentences max]

---

## TOPIC 2: [Topic Title]

**Description:** [1-3 sentence description]

**Key Insights:**
• [Insight 1 related to this topic]
• [Insight 2 related to this topic]
• [Insight 3 related to this topic]

**Notable Quotes:**
> **[Speaker Name]:** "[Exact quote extracted verbatim from the transcript]"

**Evidence/Data:** (Optional, max 5 items)
• [Relevant data if mentioned - 3-5 sentences max]

**Real-World Examples:** (Optional, max 5 items)
• [Relevant example if mentioned - 3-5 sentences max]

---

Continue this format for all topics (2-5 total).

NOTES:
- Only include Evidence/Data and Real-World Examples sections when relevant information exists in the transcript
- Include 2-5 insights per topic (use as many as are substantive and relevant)
- Include 1-3 quotes per topic (more quotes when they strongly support the topic)
- Limit Evidence/Data items to max 5 per topic, each 3-5 sentences
- Limit Real-World Examples to max 5 per topic, each 3-5 sentences"""

    def _call_llm(self, prompt: str) -> str:
        """Call LLM API via UnifiedLLMClient"""
        return self.client.generate(
            prompt=prompt,
            max_tokens=4000,
            temperature=0.7
        )

    def analyze_transcript(self, transcript: Dict) -> Dict:
        """
        Analyze a transcript and generate newsletter content suggestions

        Returns:
            Dict with keys: recommended_topics, key_insights, quotes
        """
        prompt = self._create_prompt(transcript)

        try:
            # Call the unified LLM client
            analysis = self._call_llm(prompt)

            # Add source information to the analysis
            analysis_with_source = f"**Source:** {transcript['subject']}\n\n{analysis}"

            return {
                'topic': transcript['topic'],
                'date': transcript['date'],
                'subject': transcript['subject'],
                'analysis': analysis_with_source
            }

        except Exception as e:
            return {
                'topic': transcript['topic'],
                'date': transcript['date'],
                'error': f"Error analyzing transcript with {self.provider}/{self.model}: {str(e)}"
            }

    def batch_analyze(self, transcripts: list) -> list:
        """Analyze multiple transcripts"""
        results = []
        for transcript in transcripts:
            result = self.analyze_transcript(transcript)
            results.append(result)
        return results
