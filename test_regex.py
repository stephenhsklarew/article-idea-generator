#!/usr/bin/env python3
import re

# Test with straight quotes
subject1 = 'Notes: "Daily Pulseflow Experiment Sync" Oct 23, 2025'
# Test with curly quotes
subject2 = 'Notes: "Daily Pulseflow Experiment Sync" Oct 23, 2025'

pattern = r'^Notes:\s*["""]([^"""]+)[""]\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})'

for subject in [subject1, subject2]:
    print(f'\nSubject: {subject}')
    print(f'First quote char code: {ord(subject[7])}')
    match = re.match(pattern, subject)
    if match:
        print(f'✓ MATCHED - Topic: "{match.group(1)}", Date: "{match.group(2)}"')
    else:
        print('✗ NO MATCH')
