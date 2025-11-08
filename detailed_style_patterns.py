#!/usr/bin/env python3
"""
Create comprehensive style pattern analysis with specific examples
"""

import json
import re

def extract_detailed_patterns(articles):
    """Extract detailed writing patterns with specific examples"""

    patterns = {
        'opening_strategies': [],
        'structural_elements': [],
        'tone_indicators': [],
        'vocabulary_analysis': [],
        'rhetorical_devices': [],
        'example_integration': [],
        'transition_techniques': [],
        'closing_strategies': []
    }

    for article in articles:
        content = article['content']
        title = article['title']
        edition = article['edition']

        # Get paragraphs
        paragraphs = [p.strip() for p in content.split('\n') if p.strip() and len(p.strip()) > 10]

        # OPENING STRATEGIES
        if len(paragraphs) > 0:
            first_substantive = paragraphs[1] if len(paragraphs) > 1 else paragraphs[0]
            patterns['opening_strategies'].append({
                'article': title,
                'edition': edition,
                'hook': first_substantive[:300],
                'technique': analyze_opening_technique(first_substantive)
            })

        # STRUCTURAL ELEMENTS
        section_headers = find_section_headers(paragraphs)
        if section_headers:
            patterns['structural_elements'].append({
                'article': title,
                'edition': edition,
                'sections': section_headers[:8],
                'total_sections': len(section_headers)
            })

        # TONE INDICATORS
        tone_words = extract_tone_words(content)
        if tone_words:
            patterns['tone_indicators'].append({
                'article': title,
                'edition': edition,
                'authority_words': tone_words['authority'][:5],
                'empathy_words': tone_words['empathy'][:5],
                'urgency_words': tone_words['urgency'][:5]
            })

        # RHETORICAL DEVICES
        devices = find_rhetorical_devices(paragraphs)
        if devices:
            patterns['rhetorical_devices'].append({
                'article': title,
                'edition': edition,
                'devices': devices
            })

        # EXAMPLE INTEGRATION
        examples = find_examples(paragraphs)
        if examples:
            patterns['example_integration'].append({
                'article': title,
                'edition': edition,
                'examples': examples[:3]
            })

        # TRANSITION TECHNIQUES
        transitions = find_transition_patterns(paragraphs)
        if transitions:
            patterns['transition_techniques'].append({
                'article': title,
                'edition': edition,
                'transitions': transitions[:5]
            })

        # CLOSING STRATEGIES
        if len(paragraphs) >= 2:
            # Get last substantive paragraph (before SEO/URL info)
            closing_paras = [p for p in paragraphs[-5:] if not p.startswith('SEO') and not p.startswith('Article URL') and not p.startswith('#')]
            if closing_paras:
                patterns['closing_strategies'].append({
                    'article': title,
                    'edition': edition,
                    'closing': closing_paras[-1][:300],
                    'technique': analyze_closing_technique(closing_paras[-1])
                })

    return patterns

def analyze_opening_technique(text):
    """Identify the opening technique used"""
    techniques = []
    text_lower = text.lower()

    if any(word in text_lower for word in ['story', 'years ago', 'when i', 'experience', 'remember']):
        techniques.append('Personal anecdote/story')
    if '?' in text:
        techniques.append('Provocative question')
    if any(word in text_lower for word in ['imagine', 'picture', 'consider']):
        techniques.append('Invitation to imagine')
    if any(word in text_lower for word in ['problem', 'challenge', 'struggle', 'difficulty']):
        techniques.append('Problem statement')
    if any(word in text_lower for word in ['every day', 'many', 'most', 'all']):
        techniques.append('Universal observation')

    return techniques if techniques else ['Direct statement']

def analyze_closing_technique(text):
    """Identify the closing technique used"""
    techniques = []
    text_lower = text.lower()

    if '?' in text:
        techniques.append('Question to reader')
    if any(word in text_lower for word in ['share', 'comment', 'react', 'thoughts']):
        techniques.append('Call to engagement')
    if any(word in text_lower for word in ['transform', 'future', 'begin', 'start', 'take action']):
        techniques.append('Call to action')
    if any(word in text_lower for word in ['remember', 'key', 'important', 'ultimately']):
        techniques.append('Key takeaway summary')

    return techniques if techniques else ['Simple conclusion']

def find_section_headers(paragraphs):
    """Find potential section headers"""
    headers = []
    for p in paragraphs:
        # Headers are typically short, don't end with period, and may have title case
        if len(p.split()) <= 12 and not p.endswith('.') and len(p) < 120:
            # Check if it looks like a header (title case or short)
            if p[0].isupper() and ':' not in p[20:]:  # Not a sentence fragment
                headers.append(p)
    return headers

def extract_tone_words(content):
    """Extract words that establish tone"""
    content_lower = content.lower()

    authority_words = [
        'framework', 'strategy', 'methodology', 'approach', 'essential',
        'critical', 'fundamental', 'proven', 'research', 'data', 'evidence',
        'analyze', 'evaluate', 'assess'
    ]

    empathy_words = [
        'understand', 'challenge', 'struggle', 'frustration', 'common',
        'natural', 'reasonable', 'realize', 'recognize', 'acknowledge'
    ]

    urgency_words = [
        'now', 'immediately', 'urgent', 'critical', 'must', 'imperative',
        'cannot wait', 'quickly', 'rapid', 'accelerate', 'competitive advantage'
    ]

    found_authority = [w for w in authority_words if w in content_lower]
    found_empathy = [w for w in empathy_words if w in content_lower]
    found_urgency = [w for w in urgency_words if w in content_lower]

    return {
        'authority': found_authority,
        'empathy': found_empathy,
        'urgency': found_urgency
    }

def find_rhetorical_devices(paragraphs):
    """Find rhetorical devices used"""
    devices = []

    for p in paragraphs:
        # Metaphors and analogies
        if any(phrase in p.lower() for phrase in ['like ', 'similar to', 'analogous', 'just as', 'imagine']):
            devices.append({
                'type': 'Metaphor/Analogy',
                'example': p[:150]
            })

        # Repetition/Parallelism
        if p.count('•') >= 3 or p.count('-') >= 3:
            devices.append({
                'type': 'List/Enumeration',
                'example': p[:150]
            })

        # Rhetorical questions
        if '?' in p and len(p.split()) < 30:
            devices.append({
                'type': 'Rhetorical question',
                'example': p[:150]
            })

    # Limit to avoid duplication
    return devices[:5]

def find_examples(paragraphs):
    """Find how examples and case studies are introduced"""
    examples = []

    for i, p in enumerate(paragraphs):
        p_lower = p.lower()

        # Look for example introductions
        if any(phrase in p_lower for phrase in [
            'for example', 'for instance', 'case in point', 'consider',
            'imagine', 'years ago', 'recently', 'in my experience'
        ]):
            # Get this paragraph and maybe the next
            context = p
            if i + 1 < len(paragraphs):
                context += " " + paragraphs[i + 1]

            examples.append({
                'introduction': p[:200],
                'type': 'real-world example' if any(x in p_lower for x in ['years ago', 'client', 'company']) else 'hypothetical example'
            })

    return examples

def find_transition_patterns(paragraphs):
    """Find how transitions between ideas work"""
    transitions = []

    transition_phrases = [
        'however', 'but', 'yet', 'on the other hand',
        'first', 'second', 'third', 'finally',
        'moreover', 'furthermore', 'additionally',
        'as a result', 'therefore', 'consequently',
        'for example', 'for instance',
        'in contrast', 'similarly',
        'this means', 'in other words'
    ]

    for p in paragraphs:
        p_lower = p.lower()
        # Check if paragraph starts with a transition
        for phrase in transition_phrases:
            if p_lower.startswith(phrase) or f'. {phrase}' in p_lower or f', {phrase}' in p_lower:
                transitions.append({
                    'phrase': phrase,
                    'context': p[:150]
                })
                break

    return transitions

def main():
    # Load articles
    with open('/Users/stephensklarew/Development/Scripts/Blog idea generator/articles_for_analysis.json', 'r') as f:
        articles = json.load(f)

    print("="*80)
    print("COMPREHENSIVE WRITING STYLE PATTERN ANALYSIS")
    print("="*80)

    patterns = extract_detailed_patterns(articles)

    # OPENING STRATEGIES
    print("\n" + "="*80)
    print("1. OPENING HOOK STRATEGIES")
    print("="*80)
    for item in patterns['opening_strategies']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        print(f"\nTechniques: {', '.join(item['technique'])}")
        print(f"\nExample:")
        print(f'"{item["hook"]}"')
        print("-" * 80)

    # STRUCTURAL PATTERNS
    print("\n" + "="*80)
    print("2. STRUCTURAL ORGANIZATION")
    print("="*80)
    for item in patterns['structural_elements']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        print(f"Total sections: {item['total_sections']}")
        print(f"\nSection headers:")
        for section in item['sections']:
            print(f"  • {section}")
        print("-" * 80)

    # TONE INDICATORS
    print("\n" + "="*80)
    print("3. TONE ESTABLISHMENT")
    print("="*80)
    for item in patterns['tone_indicators']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        if item['authority_words']:
            print(f"\n  Authority words: {', '.join(item['authority_words'])}")
        if item['empathy_words']:
            print(f"  Empathy words: {', '.join(item['empathy_words'])}")
        if item['urgency_words']:
            print(f"  Urgency words: {', '.join(item['urgency_words'])}")
        print("-" * 80)

    # RHETORICAL DEVICES
    print("\n" + "="*80)
    print("4. RHETORICAL DEVICES")
    print("="*80)
    for item in patterns['rhetorical_devices']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        for device in item['devices']:
            print(f"\n  {device['type']}:")
            print(f'  "{device["example"]}..."')
        print("-" * 80)

    # EXAMPLE INTEGRATION
    print("\n" + "="*80)
    print("5. EXAMPLE AND CASE STUDY INTEGRATION")
    print("="*80)
    for item in patterns['example_integration']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        for ex in item['examples']:
            print(f"\n  Type: {ex['type']}")
            print(f'  Introduction: "{ex["introduction"]}..."')
        print("-" * 80)

    # TRANSITIONS
    print("\n" + "="*80)
    print("6. TRANSITION TECHNIQUES")
    print("="*80)
    for item in patterns['transition_techniques']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        for trans in item['transitions']:
            print(f"\n  Phrase: '{trans['phrase']}'")
            print(f'  Context: "{trans["context"]}..."')
        print("-" * 80)

    # CLOSING STRATEGIES
    print("\n" + "="*80)
    print("7. CLOSING STRATEGIES")
    print("="*80)
    for item in patterns['closing_strategies']:
        print(f"\n📰 {item['article']} ({item['edition']})")
        print(f"\nTechniques: {', '.join(item['technique'])}")
        print(f"\nExample:")
        print(f'"{item["closing"]}"')
        print("-" * 80)

    # Save comprehensive report
    output_file = '/Users/stephensklarew/Development/Scripts/Blog idea generator/comprehensive_style_patterns.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"Comprehensive patterns saved to: {output_file}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
