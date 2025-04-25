# novel_tracker/normalization.py
import re
import dateparser

def normalize_status(raw_status):
    status_map = {
        'completed': ['complete', 'finished', 'concluded'],
        'ongoing': ['ongoing', 'updating', 'publishing'],
        'hiatus': ['hiatus', 'paused']
    }
    lower_status = raw_status.lower()
    for normalized, variants in status_map.items():
        if any(variant in lower_status for variant in variants):
            return normalized
    return 'unknown'

def normalize_chapters(chapter_str):
    numbers = re.findall(r'\d+', str(chapter_str))
    return int(numbers[-1]) if numbers else 0

def normalize_date(date_str):
    return dateparser.parse(date_str).isoformat() if date_str else None