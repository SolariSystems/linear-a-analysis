#!/usr/bin/env python3
"""Linear A Iteration 2: Positional analysis + cross-tablet name tracking."""

import json
import re
from collections import defaultdict

with open('/tmp/lineara.xyz/items_analysis/inscriptions.json') as f:
    data = json.load(f)

IDEOGRAMS = {
    'OLE', 'OLE+U', 'OLE+A', 'OLE+E', 'OLE+KI', 'OLE+MI', 'OLE+DI',
    'OLE+NE', 'OLE+TA', 'OLE+RI', 'OLE+QIf', 'OLE+TU', 'OLE+RA',
    'GRA', 'VIN', 'FIC', 'NI', 'CYP', 'BOS', 'OVISm', 'OVISf',
    'CAPm', 'CAPf', 'SUS', 'TELA', 'LANA', 'AES', 'AUR', 'OLIV',
    'ARE', 'AROM',
}

KNOWN_VOCAB = {'KU-RO', 'KI-RO', 'SA-RA\u2082', 'JE-DI', 'RE-ZA', 'KA-PA', 'A-DU', 'SA-RO'}

def is_number(w):
    try:
        float(w)
        return True
    except:
        return False

def is_word(w):
    if not w or w == '\n':
        return False
    if ord(w[0]) > 0xFFFF:
        return False
    if w == '\u1001' or (len(w) == 1 and ord(w) > 127):
        return False
    if is_number(w):
        return False
    return True

def is_commodity(w):
    return w in IDEOGRAMS or w.startswith('OLE')

# ============================================================
# 1. POSITIONAL ANALYSIS — Where does each word appear on tablets?
# ============================================================
print("=" * 80)
print("POSITIONAL ANALYSIS — Word positions within tablet lines")
print("=" * 80)

# Track: for each word, what POSITION does it appear in?
# Position = (line_number, position_in_line)
word_positions = defaultdict(list)  # word -> [(tablet_id, line_num, pos_in_line, total_in_line)]
word_line_positions = defaultdict(lambda: defaultdict(int))  # word -> {first/middle/last -> count}

for entry in data:
    tablet_id = entry[0]
    info = entry[1]
    words = info.get('transliteratedWords', [])
    
    # Split into lines
    lines = [[]]
    for w in words:
        if w == '\n':
            lines.append([])
        elif is_word(w):
            lines[-1].append(w)
    
    for line_num, line_words in enumerate(lines):
        if not line_words:
            continue
        total = len(line_words)
        for pos, w in enumerate(line_words):
            word_positions[w].append((tablet_id, line_num, pos, total))
            if pos == 0:
                word_line_positions[w]['first'] += 1
            elif pos == total - 1:
                word_line_positions[w]['last'] += 1
            else:
                word_line_positions[w]['middle'] += 1

# Find words with strong positional preferences
print(f"\n{'Word':25s} {'Total':>6s} {'First%':>7s} {'Middle%':>8s} {'Last%':>7s}  Position Preference")
print("-" * 85)

position_findings = []
for w in sorted(word_line_positions.keys(), key=lambda x: -sum(word_line_positions[x].values())):
    counts = word_line_positions[w]
    total = sum(counts.values())
    if total < 5:
        continue
    first_pct = counts['first'] / total * 100
    middle_pct = counts['middle'] / total * 100
    last_pct = counts['last'] / total * 100
    
    preference = ''
    if first_pct > 60:
        preference = '→ LINE-INITIAL (header/subject)'
    elif last_pct > 60:
        preference = '→ LINE-FINAL (total/result)'
    elif middle_pct > 60:
        preference = '→ MEDIAL (modifier/connector)'
    
    if total >= 5:
        position_findings.append((w, total, first_pct, middle_pct, last_pct, preference))
        if preference or total >= 10:
            print(f"  {w:23s} {total:6d} {first_pct:6.1f}% {middle_pct:7.1f}% {last_pct:6.1f}%  {preference}")

# ============================================================
# 2. CROSS-TABLET NAME TRACKING
# ============================================================
print(f"\n\n{'='*80}")
print("CROSS-TABLET NAME TRACKING — Multi-sign words appearing on 3+ tablets")
print(f"{'='*80}")

# Find multi-sign words (potential names) that recur across tablets
name_candidates = defaultdict(set)  # word -> set of tablet_ids
for entry in data:
    tablet_id = entry[0]
    info = entry[1]
    words = info.get('transliteratedWords', [])
    for w in words:
        if not is_word(w):
            continue
        if '-' in w and not is_commodity(w) and w not in KNOWN_VOCAB and not w.startswith('*'):
            name_candidates[w].add(tablet_id)

# Filter to words on 3+ tablets
recurring_names = {w: tablets for w, tablets in name_candidates.items() if len(tablets) >= 3}

print(f"\nMulti-sign words on 3+ tablets: {len(recurring_names)}")
print(f"\n{'Word':30s} {'Tablets':>8s}  Tablet IDs")
print("-" * 80)
for w in sorted(recurring_names.keys(), key=lambda x: -len(recurring_names[x])):
    tablets = recurring_names[w]
    tablet_list = ', '.join(sorted(tablets)[:6])
    if len(tablets) > 6:
        tablet_list += f' (+{len(tablets)-6} more)'
    print(f"  {w:28s} {len(tablets):8d}  {tablet_list}")

# ============================================================
# 3. CO-OCCURRENCE NETWORK — Which names appear TOGETHER?
# ============================================================
print(f"\n\n{'='*80}")
print("CO-OCCURRENCE NETWORK — Names appearing together on same tablets")
print(f"{'='*80}")

# Build co-occurrence matrix for recurring multi-sign words
recurring_list = sorted(recurring_names.keys(), key=lambda x: -len(recurring_names[x]))[:30]
cooccurrences = defaultdict(lambda: defaultdict(int))

for entry in data:
    tablet_id = entry[0]
    info = entry[1]
    words = info.get('transliteratedWords', [])
    present = [w for w in words if w in recurring_names]
    for i, w1 in enumerate(present):
        for w2 in present[i+1:]:
            cooccurrences[w1][w2] += 1
            cooccurrences[w2][w1] += 1

print(f"\n{'Word A':25s} {'Word B':25s} {'Co-occur':>9s}")
print("-" * 65)
shown = set()
for w1 in recurring_list:
    for w2 in sorted(cooccurrences[w1].keys(), key=lambda x: -cooccurrences[w1][x]):
        if cooccurrences[w1][w2] >= 2 and (w2, w1) not in shown:
            print(f"  {w1:23s} {w2:23s} {cooccurrences[w1][w2]:9d}")
            shown.add((w1, w2))

# ============================================================
# 4. SITE DISTRIBUTION — Do words cluster by site?
# ============================================================
print(f"\n\n{'='*80}")
print("SITE DISTRIBUTION — Where do recurring words appear?")
print(f"{'='*80}")

word_sites = defaultdict(lambda: defaultdict(int))
for entry in data:
    tablet_id = entry[0]
    info = entry[1]
    site = info.get('site', 'unknown')
    words = info.get('transliteratedWords', [])
    for w in words:
        if w in recurring_names or w in KNOWN_VOCAB:
            word_sites[w][site] += 1

# Find words that are site-specific
print(f"\n{'Word':25s} {'Sites':>6s}  Distribution")
print("-" * 80)
for w in sorted(word_sites.keys(), key=lambda x: -sum(word_sites[x].values()))[:40]:
    sites = word_sites[w]
    total = sum(sites.values())
    if total < 3:
        continue
    site_str = ', '.join(f'{s}:{n}' for s, n in sorted(sites.items(), key=lambda x: -x[1])[:4])
    num_sites = len(sites)
    marker = ''
    if num_sites == 1:
        marker = ' ← SITE-SPECIFIC'
    elif max(sites.values()) / total > 0.8:
        marker = f' ← CONCENTRATED ({max(sites, key=sites.get)})'
    print(f"  {w:23s} {num_sites:6d}  {site_str}{marker}")

# ============================================================
# 5. LIBATION FORMULA TABLETS — Full structural parse
# ============================================================
print(f"\n\n{'='*80}")
print("LIBATION FORMULA TABLETS — Structural analysis")
print(f"{'='*80}")

libation_tablets = []
for entry in data:
    tablet_id = entry[0]
    info = entry[1]
    words = info.get('transliteratedWords', [])
    word_strs = [w for w in words if is_word(w)]
    
    # Check for libation formula elements
    has_formula = any('WA-JA' in w for w in word_strs) or any('A-TA-I' in w for w in word_strs)
    has_asasarame = any('SA-SA-RA' in w for w in word_strs)
    
    if has_formula or has_asasarame:
        libation_tablets.append({
            'id': tablet_id,
            'site': info.get('site', '?'),
            'support': info.get('support', '?'),
            'words': word_strs,
        })

print(f"\nLibation-related tablets found: {len(libation_tablets)}")
for tab in sorted(libation_tablets, key=lambda t: t['id']):
    word_str = ' | '.join(tab['words'][:15])
    print(f"\n  {tab['id']} ({tab['site']}, {tab['support']})")
    print(f"    {word_str}")

# ============================================================
# 6. NEW VOCABULARY CANDIDATES — Words constrained by position + commodity
# ============================================================
print(f"\n\n{'='*80}")
print("NEW VOCABULARY CANDIDATES — Position + commodity constrained")
print(f"{'='*80}")

# Words that are LINE-INITIAL (headers/subjects) AND have commodity associations
print(f"\n  LINE-INITIAL words with commodity associations (likely PLACE NAMES or CATEGORIES):")
for w, total, first_pct, mid_pct, last_pct, pref in position_findings:
    if first_pct > 55 and total >= 5:
        # Check commodity associations
        tablets_with_word = set()
        for entry in data:
            tablet_id = entry[0]
            words = entry[1].get('transliteratedWords', [])
            if w in words:
                tablets_with_word.add(tablet_id)
                commodities = [x for x in words if is_commodity(x)]
                if commodities:
                    pass
        if '-' in w:
            print(f"    {w:25s} first:{first_pct:.0f}% ({total}x) — likely header/category")

# Words that are LINE-FINAL (results/totals)
print(f"\n  LINE-FINAL words (likely TOTALS, RESULTS, or VERBS):")
for w, total, first_pct, mid_pct, last_pct, pref in position_findings:
    if last_pct > 55 and total >= 5:
        if '-' in w or w in KNOWN_VOCAB:
            print(f"    {w:25s} last:{last_pct:.0f}% ({total}x)")

