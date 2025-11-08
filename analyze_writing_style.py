#!/usr/bin/env python3
"""
Analyze writing style patterns from the fetched articles
"""

import json
import re
from collections import Counter

def analyze_article(article):
    """Analyze a single article for style patterns"""
    content = article['content']
    title = article['title']

    # Split into paragraphs (double newlines or single newlines for short paragraphs)
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

    # Get opening (first 3 paragraphs)
    opening = paragraphs[:3] if len(paragraphs) >= 3 else paragraphs

    # Get closing (last 2 paragraphs)
    closing = paragraphs[-2:] if len(paragraphs) >= 2 else paragraphs[-1:]

    # Sentence analysis
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Paragraph lengths
    para_word_counts = [len(p.split()) for p in paragraphs]

    # Sentence lengths
    sentence_word_counts = [len(s.split()) for s in sentences]

    # Look for questions
    questions = [s for s in sentences if '?' in s]

    # Look for lists/bullets
    bullet_points = [p for p in paragraphs if p.startswith('•') or p.startswith('-') or p.startswith('*')]

    # Look for emphasis patterns (bold, italics markers, quotes)
    bold_pattern = re.findall(r'\*\*([^*]+)\*\*', content)

    # Look for transition words
    transition_words = [
        'however', 'therefore', 'moreover', 'furthermore', 'consequently',
        'meanwhile', 'nevertheless', 'in contrast', 'on the other hand',
        'first', 'second', 'third', 'finally', 'ultimately', 'essentially',
        'for example', 'for instance', 'specifically', 'in particular',
        'as a result', 'in fact', 'indeed', 'notably', 'importantly'
    ]

    found_transitions = []
    for word in transition_words:
        if word in content.lower():
            found_transitions.append(word)

    # Look for section headers (lines that are short and may be headers)
    potential_headers = [p for p in paragraphs if len(p.split()) <= 8 and len(p) < 80 and not p.endswith('.')]

    return {
        'title': title,
        'opening_paragraphs': opening,
        'closing_paragraphs': closing,
        'total_paragraphs': len(paragraphs),
        'total_sentences': len(sentences),
        'avg_paragraph_length': sum(para_word_counts) / len(para_word_counts) if para_word_counts else 0,
        'min_paragraph_length': min(para_word_counts) if para_word_counts else 0,
        'max_paragraph_length': max(para_word_counts) if para_word_counts else 0,
        'avg_sentence_length': sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0,
        'questions_count': len(questions),
        'sample_questions': questions[:3],
        'bullet_points_count': len(bullet_points),
        'sample_bullets': bullet_points[:5],
        'bold_elements': bold_pattern[:10],
        'transition_words_used': found_transitions,
        'potential_section_headers': potential_headers[:10],
        'word_count': len(content.split())
    }

def main():
    # Load articles
    with open('/Users/stephensklarew/Development/Scripts/Blog idea generator/articles_for_analysis.json', 'r') as f:
        articles = json.load(f)

    print("="*80)
    print("WRITING STYLE ANALYSIS")
    print("="*80)

    all_analyses = []

    for article in articles:
        print(f"\n{'='*80}")
        print(f"ARTICLE: {article['title']}")
        print(f"Edition: {article['edition']}")
        print(f"{'='*80}")

        analysis = analyze_article(article)
        all_analyses.append(analysis)

        print(f"\n📊 METRICS:")
        print(f"  Total paragraphs: {analysis['total_paragraphs']}")
        print(f"  Total sentences: {analysis['total_sentences']}")
        print(f"  Word count: {analysis['word_count']}")
        print(f"  Avg paragraph length: {analysis['avg_paragraph_length']:.1f} words")
        print(f"  Avg sentence length: {analysis['avg_sentence_length']:.1f} words")
        print(f"  Paragraph range: {analysis['min_paragraph_length']}-{analysis['max_paragraph_length']} words")

        print(f"\n🎯 OPENING HOOK:")
        for i, para in enumerate(analysis['opening_paragraphs'], 1):
            print(f"\n  Paragraph {i}:")
            print(f"  \"{para[:200]}{'...' if len(para) > 200 else ''}\"")

        print(f"\n🏁 CLOSING:")
        for i, para in enumerate(analysis['closing_paragraphs'], 1):
            print(f"\n  Final paragraph {i}:")
            print(f"  \"{para[:200]}{'...' if len(para) > 200 else ''}\"")

        if analysis['questions_count'] > 0:
            print(f"\n❓ QUESTIONS ({analysis['questions_count']} total):")
            for q in analysis['sample_questions']:
                print(f"  - \"{q.strip()}?\"")

        if analysis['bullet_points_count'] > 0:
            print(f"\n• BULLET POINTS ({analysis['bullet_points_count']} total):")
            for b in analysis['sample_bullets']:
                print(f"  {b[:100]}{'...' if len(b) > 100 else ''}")

        if analysis['bold_elements']:
            print(f"\n**EMPHASIS ELEMENTS:**")
            for b in analysis['bold_elements']:
                print(f"  - {b}")

        if analysis['transition_words_used']:
            print(f"\n🔄 TRANSITION WORDS:")
            print(f"  {', '.join(analysis['transition_words_used'][:15])}")

        if analysis['potential_section_headers']:
            print(f"\n📑 SECTION HEADERS:")
            for h in analysis['potential_section_headers']:
                print(f"  - {h}")

    # Overall patterns
    print(f"\n\n{'='*80}")
    print("OVERALL PATTERNS ACROSS ALL ARTICLES")
    print(f"{'='*80}")

    avg_para_length = sum(a['avg_paragraph_length'] for a in all_analyses) / len(all_analyses)
    avg_sent_length = sum(a['avg_sentence_length'] for a in all_analyses) / len(all_analyses)

    print(f"\n📊 AVERAGE METRICS:")
    print(f"  Average paragraph length: {avg_para_length:.1f} words")
    print(f"  Average sentence length: {avg_sent_length:.1f} words")
    print(f"  Average article length: {sum(a['word_count'] for a in all_analyses) / len(all_analyses):.0f} words")

    print(f"\n🎨 COMMON STYLE ELEMENTS:")
    print(f"  - Questions per article (avg): {sum(a['questions_count'] for a in all_analyses) / len(all_analyses):.1f}")
    print(f"  - Bullet points per article (avg): {sum(a['bullet_points_count'] for a in all_analyses) / len(all_analyses):.1f}")

    # Most common transitions across all articles
    all_transitions = []
    for a in all_analyses:
        all_transitions.extend(a['transition_words_used'])

    transition_counts = Counter(all_transitions)
    print(f"\n🔄 MOST COMMON TRANSITIONS:")
    for transition, count in transition_counts.most_common(10):
        print(f"  - {transition}: {count} times")

    # Save detailed analysis
    output_file = '/Users/stephensklarew/Development/Scripts/Blog idea generator/style_analysis_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analyses, f, indent=2, ensure_ascii=False)

    print(f"\n\n{'='*80}")
    print(f"Detailed analysis saved to: {output_file}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
