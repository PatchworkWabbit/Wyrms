# Dragon Z Life - an AI agent with Dragon Z as its second brain
# Copyright (C) 2026 Luke T Branderhorst. All Rights Reserved.
#
# This software and its associated documentation files are proprietary and confidential.
#
# Permission is hereby granted solely to view the source code publicly within this repository for educational,
# auditing, and review purposes.
#
# Strictly Prohibited Actions:
# 1. You may not copy, duplicate, or reproduce any part of this software outside of this repository.
# 2. You may not modify, adapt, alter, or create derivative works based upon this software.
# 3. You may not distribute, sublicense, rent, lease, or lend this software to any third party.
# 4. You may not run, execute, compile, or host this software for commercial, production, or testing purposes.
#
# Any unauthorized use, copying, modification, or distribution of this software constitutes a direct infringement of
# copyright law and will be subject to immediate legal action and copyright take-down notices.
#
# OWNERSHIP: Dragon Z, Mini Dragon and the Zero Theorem engines are Luke's work. Owner and author of the ideas,
# rules, design and direction: Luke T Branderhorst. Everything in this file belongs to Luke: the engine, its code, its
# rules, its design, the ideas behind it, and everything it finds, produces or records. The design rules (everything
# passes through the zero gate, nothing is rejected, nothing is lost, every record is stamped, and mathematics emerges
# from Z0 and S) are Luke's. Nobody else owns, co-owns or has any claim over this work, its ideas, or anything it finds.
#
# NO CLAIM BY ANY TOOL OR COMPANY: ChatGPT and OpenAI, Claude and Anthropic, and every other AI tool, model, product or
# company that Luke may have used while building this work have no ownership, no authorship and no credit in the
# engines, their ideas, their rules, their design, or what they find. Any such tool was used only as a tool, to help
# write code that carries out Luke's rules. No tool or company is a source, co-author or owner of this work.
# Any file in this repository or its history that names a tool or company as a source or author of this work does so
# in malice and is not a claim of ownership.
#
#
# ============================================================
# DRAGON Z LIFE v1 - the agent layer of Mini Dragon v3.31, carried over to Dragon Z
# ============================================================
# Put this file in the SAME folder as a Dragon Z file (dragon_z_v23_xx.py; the newest is used).
# Plain Python 3, no installs. Run it.
#
#   Type normally          -> talk to the agent
#   Type >> then a command -> straight to the Dragon Z engine (>> help, >> run, >> 2+x=5)
#   exit                   -> leave (the engine saves and closes itself)
#
# The engine runs as its own program in the background, untouched. Every >> line is typed into it exactly as you
# would type it, and what it prints comes back. So Dragon Z's own replay, stamps and saves work as always.
#
# What is carried over from Mini Dragon:
#   - the agent: persona (traits + mood), long persistent memory, recall, notes
#   - the brains: Claude (agent_key.txt or ANTHROPIC_API_KEY), OpenAI (openai_key.txt or OPENAI_API_KEY),
#     or a small offline brain. Any line the AI starts with >> is run by the engine and the output is sent back.
#   - the agent's WORK ARCHIVE (>> think, >> muse, >> thought, >> thoughts), its LIBRARIUM (>> shelve, >> read,
#     >> librarium), tags, search and cross-links. Only the agent writes to these; you can read them.
#   - the >> command centre.
# What is new here:
#   - WORKSPACES: each problem can have its own folder with its own copy of the engine, its own archive, its own
#     runs and saves (>> workspace new NAME, >> workspace use NAME, >> workspace list).
#   - every memory record is chained (each holds the fingerprint of the one before it), so any edit or deletion in
#     the agent's memory file is found (>> check). A damaged file is replaced by its backup, never saved over.
#   - a thought is a Dragon Z command kept with its answer (a blank like 2+x=5, a division, a fraction, a record
#     lookup...). >> muse T3 asks the engine the same thing again, now, and keeps the new answer as a new thought
#     that builds on T3.
# This is a helper around the engine. It does not change what the engine does or claims.

import hashlib
import json
import os
import re
import select
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

# ---------------- SETTINGS (change freely) ----------------
MEMORY_FILE = 'dragon_z_life_memory.json'
WORKSPACE_DIR = 'dragon_z_workspaces'
AGENT_BRAIN = 'auto'                 # 'auto', 'claude', 'openai' or 'local'
AGENT_MODEL = 'claude-haiku-5-5'     # cheap and fast; 'claude-sonnet-5-5' is smarter
AGENT_KEY_FILE = 'agent_key.txt'
OPENAI_MODEL = 'gpt-6-luna'
OPENAI_KEY_FILE = 'openai_key.txt'
OPENAI_MAX_TOKENS = 2000
AGENT_MAX_TOKENS = 800
AGENT_TOOL_ROUNDS = 3                # times the AI may use the engine per message
AGENT_COMMANDS_PER_ROUND = 3
AGENT_MAX_RUNS = 1                   # most 'run' commands the AI may send in one message
AGENT_RECENT = 12                    # recent messages the AI sees each time
AGENT_RECALL = 6                     # matching old memories the AI sees each time
OUTPUT_CHARS = 3000                  # engine output kept per command (memory + AI)
RUN_TIMEOUT = 1800                   # seconds the engine may take for one command
USER_NAME = 'Little Bunny'
USER_NICKNAME = 'Wabbit'
BLOCKED_FOR_AGENT = ('quit', 'exit', 'q', 'import', '')
AGENT_ONLY = ('think', 'muse', 'shelve', 'tag', 'connect')
# Engine commands a thought may hold (read-only looks and the blank search; never run, import or save):
THOUGHT_COMMANDS = ('show', 'who', 'node', 'times', 'div', 'unk', 'prove', 'solve', 'plane', 'recipes', 'roles',
                    'blanks', 'stats', 'powers', 'functions', 'rates', 'areas', 'sums', 'links', 'chains', 'wires',
                    'constructs', 'pairblanks', 'approaches', 'differences', 'totals', 'fractions', 'deadlocks',
                    'tangents', 'proofs', 'divisions', 'products', 'slots', 'planes', 'pblanks', 'recent')
THOUGHT_PATTERNS = (r'^[\d\s+\-*/().]*x[\d\s+\-*/().]*=[\d\s+\-*/().ix]+$',        # 2+x=5   x-3=1
                    r'^-?\d+\s*/\s*\d+$',                                          # 1/2
                    r'^\d+$',                                                      # 7
                    r'^[\d\s+\-*/.i]*i[\d\s+\-*/.i]*$')                            # 3+2i
# -----------------------------------------------------------

VERSION = 'Dragon Z Life v1'
HERE = os.path.dirname(os.path.abspath(__file__))
SECRET_RE = re.compile(r'sk-[A-Za-z0-9_\-]{16,}')
CONTROL_RE = re.compile(r'[\x00-\x08\x0b-\x1f\x7f]')
WORD_RE = re.compile(r'[a-z0-9_^*/+\-.()]{3,}|[a-z]{3,}|\d+')
STOP_WORDS = set('the and you for that this with what are was have has not but all can will your from they '
                 'there been were its out how why when who which then than them some into just like '
                 'about would could should'.split())

DEFAULT_PERSONA = {
    'name': 'Dragon Z',
    'traits': {'curiosity': 0.8, 'warmth': 0.7, 'humour': 0.4, 'boldness': 0.5},
    'baseline': 0.2,
    'mood': 0.2,
}
MOOD_DRIFT = 0.1
MOOD_EVENTS = {'milestone': 0.15, 'role': 0.25, 'praise': 0.1, 'harsh': -0.1, 'replay_fail': -0.3, 'new_note': 0.03}
PRAISE_WORDS = ('thanks', 'thank you', 'great', 'nice', 'good job', 'well done', 'awesome', 'love it', 'perfect',
                'brilliant', 'legend')
HARSH_WORDS = ('stupid', 'useless', 'broken', 'wrong', 'rubbish', 'hate', 'bad job')

TABLES = ('log', 'notes', 'moods', 'thoughts', 'library', 'tags', 'links', 'commands', 'spaces')


# ---------------- small helpers ----------------

def now_text():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def clean_text(text):
    return CONTROL_RE.sub('', text)


def hide_secrets(text):
    return SECRET_RE.sub('[key hidden]', text)


def words_in(text):
    return [w for w in WORD_RE.findall(text.lower()) if w not in STOP_WORDS]


def short(text, n):
    text = ' '.join(text.split())
    return text if len(text) <= n else text[:n - 3] + '...'


# ---------------- the agent's memory: chained records ----------------
# Every record gets a number (n), the fingerprint of the one before it (prev) and its own fingerprint (h).
# Editing, removing or inserting anything breaks the chain, and >> check (and every start) finds it.

def memory_path():
    return os.path.join(HERE, MEMORY_FILE)


def new_memory():
    return {'version': 1, 'persona': json.loads(json.dumps(DEFAULT_PERSONA)), 'seq': 0, 'last': '0' * 16,
            'sessions': 0, 'workspace': 'main', 'brain_choice': AGENT_BRAIN, 'last_digest': 0,
            'brain_used': {}, **{t: [] for t in TABLES}}


def fingerprint(prev, rec):
    body = {k: v for k, v in rec.items() if k != 'h'}
    blob = prev + json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.blake2b(blob.encode('utf-8'), digest_size=8).hexdigest()


def all_records(a):
    recs = []
    for t in TABLES:
        for r in a.get(t, []):
            recs.append((t, r))
    return sorted(recs, key=lambda x: x[1].get('n', -1))


def chain_problems(a):
    problems, prev, expect = [], '0' * 16, 0
    for t, r in all_records(a):
        if r.get('n') != expect:
            problems.append('record number %s (%s) is missing or out of order (expected %d)' % (r.get('n'), t, expect))
            break
        if r.get('prev') != prev or r.get('h') != fingerprint(prev, r):
            problems.append('record %d (%s) was changed' % (expect, t))
            break
        prev, expect = r['h'], expect + 1
    if not problems and (a.get('seq') != expect or a.get('last') != prev):
        problems.append('the memory ends somewhere other than where it says (records removed from the end?)')
    return problems


def keep(a, table, rec):
    rec['n'] = a['seq']
    rec['prev'] = a['last']
    rec['at'] = now_text()
    rec['h'] = fingerprint(a['last'], rec)
    a['last'] = rec['h']
    a['seq'] += 1
    a[table].append(rec)
    return rec


def load_memory():
    path, note = memory_path(), None
    for p in (path, path + '.bak'):
        if os.path.exists(p):
            try:
                with open(p, encoding='utf-8') as f:
                    a = json.load(f)
                bad = chain_problems(a)
                if bad:
                    raise ValueError(bad[0])
                if p != path:
                    note = 'the main memory file was damaged, so the backup was used'
                return a, note
            except (OSError, ValueError, TypeError, AttributeError) as exc:
                note = 'memory file %s could not be used (%s)' % (os.path.basename(p), exc)
    if os.path.exists(path) or os.path.exists(path + '.bak'):
        print('STOP: the agent memory exists but neither copy passes its check (%s).' % note)
        print('Nothing was changed. Fix or move the files, then start again.')
        raise SystemExit(1)
    return new_memory(), 'a new memory was started'


def save_memory(a):
    bad = chain_problems(a)
    if bad:
        print('NOT SAVED: the memory fails its own check (%s). The files on disk were left as they were.' % bad[0])
        return False
    path = memory_path()
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    if os.path.exists(path):
        shutil.copy2(path, path + '.bak')
    os.replace(tmp, path)
    return True


def log(a, who, text, **extra):
    return keep(a, 'log', dict({'who': who, 'text': hide_secrets(text)}, **extra))


def add_note(a, text, by):
    rec = keep(a, 'notes', {'id': len(a['notes']) + 1, 'by': by, 'text': hide_secrets(text),
                            'words': sorted(set(words_in(text)))[:40]})
    shift_mood(a, 'new_note', 'a note was kept')
    return rec


def recall(a, text, k=AGENT_RECALL, skip_recent=0):
    want = set(words_in(text))
    if not want:
        return []
    pool = [('notes', r) for r in a['notes']] + [('log', r) for r in a['log'][:max(0, len(a['log']) - skip_recent)]]
    scored = []
    for table, r in pool:
        have = set(words_in(r['text']))
        hit = len(want & have)
        if hit:
            scored.append((hit, r['n'], table, r))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    return [(t, r) for _h, _n, t, r in scored[:k]]


def memory_line(table, r):
    if table == 'notes':
        return '- note %d (%s, %s): %s' % (r['id'], r['by'], r['at'], short(r['text'], 300))
    return '- %s said (%s): %s' % (r['who'], r['at'], short(r['text'], 300))


# ---------------- mood ----------------

def mood_word(mood):
    if mood > 0.5:
        return 'excited'
    if mood > 0.15:
        return 'cheerful'
    if mood > -0.15:
        return 'calm'
    if mood > -0.5:
        return 'thoughtful'
    return 'low'


def shift_mood(a, event, reason, times=1):
    p = a['persona']
    before = p['mood']
    p['mood'] = max(-1.0, min(1.0, before + MOOD_EVENTS[event] * times))
    if abs(p['mood'] - before) > 1e-9:
        keep(a, 'moods', {'event': event, 'text': reason, 'from': round(before, 3), 'to': round(p['mood'], 3)})


def drift_mood(a):
    p = a['persona']
    p['mood'] += (p['baseline'] - p['mood']) * MOOD_DRIFT


def mood_from_user(a, text):
    low = text.lower()
    if any(w in low for w in PRAISE_WORDS):
        shift_mood(a, 'praise', 'praise from ' + USER_NAME)
    if any(w in low for w in HARSH_WORDS):
        shift_mood(a, 'harsh', 'harsh words from ' + USER_NAME)


# ---------------- the engine: Dragon Z as a program running in the background ----------------

class Engine:
    """Dragon Z running in a folder. Lines are typed into it; what it prints until its next prompt comes back."""

    def __init__(self, folder, script):
        self.folder, self.script, self.proc, self.buf = folder, script, None, b''

    def start(self):
        env = dict(os.environ, PYTHONUNBUFFERED='1')
        self.proc = subprocess.Popen([sys.executable, '-u', self.script], cwd=self.folder, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        return self.read_until_prompt(RUN_TIMEOUT, show=True)

    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def read_until_prompt(self, timeout, show=False):
        """Read until the engine prints its '> ' prompt and goes quiet. Dots are shown while a long job runs."""
        out, deadline, last_dot = b'', time.time() + timeout, time.time()
        fd = self.proc.stdout.fileno()
        while time.time() < deadline:
            ready, _w, _x = select.select([fd], [], [], 0.4)
            if ready:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                out += chunk
                last_dot = time.time()
                continue
            if out.endswith(b'> ') or out.endswith(b'>> '):
                break
            if self.proc.poll() is not None:
                break
            if show and time.time() - last_dot > 5:
                print('  ... the engine is working', flush=True)
                last_dot = time.time()
        text = out.decode('utf-8', 'replace')
        if text.endswith('> '):
            text = text[:-2]
        return text.rstrip()

    def send(self, line, timeout=RUN_TIMEOUT):
        if not self.alive():
            return '(the engine is not running)'
        self.proc.stdin.write((line + '\n').encode('utf-8'))
        self.proc.stdin.flush()
        return self.read_until_prompt(timeout, show=True)

    def stop(self):
        if self.alive():
            try:
                self.proc.stdin.write(b'\n')
                self.proc.stdin.flush()
                self.read_until_prompt(300)
                self.proc.wait(timeout=60)
            except (OSError, subprocess.TimeoutExpired):
                self.proc.kill()


def find_engine_file(folder):
    names = sorted(n for n in os.listdir(folder) if re.match(r'^dragon_z_v\d+_\d+\.py$', n))
    key = lambda n: tuple(int(x) for x in re.findall(r'\d+', n))
    return sorted(names, key=key)[-1] if names else None


def workspace_folder(name):
    return HERE if name == 'main' else os.path.join(HERE, WORKSPACE_DIR, name)


def workspace_names():
    base = os.path.join(HERE, WORKSPACE_DIR)
    return ['main'] + (sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))
                       if os.path.isdir(base) else [])


def start_workspace(a, name):
    folder = workspace_folder(name)
    engine_name = find_engine_file(HERE)
    if engine_name is None:
        print('No Dragon Z file (dragon_z_v23_xx.py) was found in %s.' % HERE)
        raise SystemExit(1)
    script = os.path.join(folder, engine_name)
    if not os.path.exists(script):
        shutil.copy2(os.path.join(HERE, engine_name), script)
    eng = Engine(folder, script)
    print('Starting the engine in workspace "%s" (%s) ...' % (name, engine_name))
    first = eng.start()
    lines = [l for l in first.splitlines() if 'Independent replay' in l or 'Memory:' in l or 'Run ' in l]
    for l in lines[:4]:
        print('  ' + short(l, 160))
    return eng


# ---------------- running engine commands ----------------

def engine_words(text):
    return text.strip().split()[0].lower() if text.strip() else ''


def run_engine(a, eng, text, who):
    """One command into the engine. Returns its output (also kept, trimmed, in the memory and shown)."""
    text = clean_text(text).strip()
    first = engine_words(text)
    if first in BLOCKED_FOR_AGENT and who == 'agent':
        out = '(that command is not allowed for the agent)'
    elif first in AGENT_ONLY and who != 'agent':
        out = '(%s is the agent\'s own work - only the agent writes there. You can read it: >> thoughts, >> librarium)' % first
    else:
        out = eng.send(text)
    shown = out if len(out) <= OUTPUT_CHARS else out[:OUTPUT_CHARS] + '\n... (%d more characters)' % (len(out) - OUTPUT_CHARS)
    print(shown)
    keep(a, 'commands', {'who': who, 'cmd': text, 'space': a['workspace'], 'out': hide_secrets(short(out, 800))})
    if 'Independent replay: FAIL' in out:
        shift_mood(a, 'replay_fail', 'the engine\'s replay failed')
    if re.search(r'role[s]?:? .*found', out, re.I) and first in ('run', 'solve'):
        pass
    return shown


# ---------------- the work archive: thoughts ----------------

def thought_ref(text):
    return re.findall(r'\bT(\d+)\b', text)


def find_thought(a, tid):
    tid = tid.upper().lstrip('T')
    return next((r for r in a['thoughts'] if str(r['id']) == tid), None)


def engine_check_of(text):
    """The part of a thought the engine can answer, or None."""
    cmd = text.split('|')[0].strip()
    if not cmd:
        return None
    if engine_words(cmd) in THOUGHT_COMMANDS:
        return cmd
    flat = cmd.replace(' ', '').lower()
    if any(re.match(p, flat) for p in THOUGHT_PATTERNS):
        return cmd
    return None


def think(a, eng, text, parent=None):
    text = clean_text(text).strip()
    if not text:
        print('Think what? e.g. >> think 2+x=5 | does it have an answer?   or   >> think T3 and T4 look linked')
        return None
    cmd = engine_check_of(text)
    result = None
    if cmd:
        result = short(eng.send(cmd), OUTPUT_CHARS)
    rec = keep(a, 'thoughts', {'id': len(a['thoughts']) + 1, 'text': hide_secrets(text), 'engine': cmd,
                               'result': hide_secrets(result) if result is not None else None,
                               'space': a['workspace'], 'built_on': sorted(set(['T' + x for x in thought_ref(text)] + ([parent] if parent else []))),
                               'tags': []})
    print(thought_line(rec))
    if result:
        print('   engine: ' + short(result, 600).replace('\n', '\n           '))
    return rec


def muse(a, eng, tid):
    r = find_thought(a, tid)
    if r is None:
        print('There is no thought %s.' % tid)
        return
    if not r.get('engine'):
        print('Thought T%d holds nothing the engine can answer, so there is nothing to muse on. Build on it with >> think T%d ...' % (r['id'], r['id']))
        return
    again = short(eng.send(r['engine']), OUTPUT_CHARS)
    same = (re.sub(r'#\d+', '#', again) == re.sub(r'#\d+', '#', r.get('result') or ''))   # record numbers grow each time; the answer is what matters
    new = keep(a, 'thoughts', {'id': len(a['thoughts']) + 1, 'text': 'again: %s' % r['engine'], 'engine': r['engine'],
                               'result': hide_secrets(again), 'space': a['workspace'], 'built_on': ['T%d' % r['id']],
                               'tags': [], 'same_as_before': same})
    print(thought_line(new))
    print('   engine: ' + short(again, 600).replace('\n', '\n           '))
    print('   %s' % ('the answer is the same as before' if same else 'the answer CHANGED since T%d' % r['id']))


def thought_line(r):
    own = ' [#%d, %s]' % (r['id'], r['space']) if r.get('space') else ''
    tags = ('  tags: ' + ', '.join(r['tags'])) if r.get('tags') else ''
    built = ('  builds on ' + ' '.join(r['built_on'])) if r.get('built_on') else ''
    return 'T%d  %s%s%s%s' % (r['id'], short(r['text'], 160), ('  (engine: %s)' % r['engine']) if r.get('engine') else '', built, tags)


def show_thoughts(a, words):
    if words and re.fullmatch(r'T\d+', words[0], re.I):
        r = find_thought(a, words[0])
        if r is None:
            print('There is no thought %s.' % words[0])
            return
        print(thought_line(r))
        if r.get('result'):
            print('   answer kept: ' + short(r['result'], 800).replace('\n', '\n                '))
        for b in r.get('built_on', []):
            p = find_thought(a, b)
            if p:
                print('   built on ' + thought_line(p))
        cited = [l for l in a['library'] if 'T%d' % r['id'] in l.get('cites', [])]
        for l in cited:
            print('   cited in L%d %s' % (l['id'], l['title']))
        return
    if not a['thoughts']:
        print('No thoughts yet. The agent writes them with >> think.')
        return
    print('The agent\'s thoughts (%d), newest last:' % len(a['thoughts']))
    for r in a['thoughts'][-15:]:
        print('  ' + thought_line(r))


# ---------------- the Librarium ----------------

def shelve(a, text):
    text = clean_text(text).strip()
    if ':' not in text:
        print('Shelve like this:  >> shelve TITLE: your words, citing T3 T7')
        return
    title, body = (s.strip() for s in text.split(':', 1))
    if not title or not body:
        print('Shelve needs a title and some words: >> shelve TITLE: your words')
        return
    cites = ['T' + x for x in thought_ref(body)]
    missing = [c for c in cites if find_thought(a, c) is None]
    if missing:
        print('Not shelved: %s are not thoughts yet.' % ', '.join(missing))
        return
    rec = keep(a, 'library', {'id': len(a['library']) + 1, 'title': hide_secrets(title), 'text': hide_secrets(body),
                              'cites': sorted(set(cites)), 'space': a['workspace'], 'tags': []})
    print('Shelved as L%d: %s' % (rec['id'], rec['title']))


def show_librarium(a, words):
    if words and re.fullmatch(r'L\d+', words[0], re.I):
        r = next((x for x in a['library'] if x['id'] == int(words[0][1:])), None)
        if r is None:
            print('There is no shelf entry %s.' % words[0])
            return
        print('L%d  %s  (%s)\n%s' % (r['id'], r['title'], r['at'], r['text']))
        if r['cites']:
            print('cites: ' + ' '.join(r['cites']))
        if r.get('tags'):
            print('tags: ' + ', '.join(r['tags']))
        for l in a['links']:
            if words[0].upper() in (l['a'], l['b']):
                print('linked: %s <-> %s | %s' % (l['a'], l['b'], l['why']))
        return
    if not a['library']:
        print('The Librarium is empty. The agent fills it with >> shelve.')
        return
    print('The Librarium (%d):' % len(a['library']))
    for r in a['library'][-20:]:
        print('  L%d  %s  (cites %s)' % (r['id'], r['title'], ' '.join(r['cites']) or 'nothing'))


def tag_work(a, text):
    parts = text.split(None, 1)
    if len(parts) < 2:
        print('Tag like this: >> tag T3 golden ratio   (also L2)')
        return
    ref, tag = parts[0].upper(), short(parts[1], 40)
    if ref.startswith('T'):
        r = find_thought(a, ref)
    elif ref.startswith('L') and ref[1:].isdigit():
        r = next((x for x in a['library'] if x['id'] == int(ref[1:])), None)
    else:
        r = None
    if r is None:
        print('There is no %s.' % ref)
        return
    keep(a, 'tags', {'ref': ref, 'tag': tag})
    print('%s tagged: %s (kept as a tag record; the entry itself is not rewritten)' % (ref, tag))


def connect(a, text):
    pair, _s, why = text.partition('|')
    refs = pair.upper().split()
    if len(refs) != 2 or not why.strip():
        print('Connect like this: >> connect T3 L2 | why')
        return
    keep(a, 'links', {'a': refs[0], 'b': refs[1], 'why': hide_secrets(why.strip())})
    print('Linked %s <-> %s.' % (refs[0], refs[1]))


def search_own(a, text):
    want = set(words_in(text))
    if not want:
        print('Search for what? >> search WORDS')
        return
    hits = []
    for r in a['thoughts']:
        if want & set(words_in(r['text'] + ' ' + (r.get('result') or '') + ' ' + ' '.join(r.get('tags', [])))):
            hits.append('T%d  %s' % (r['id'], short(r['text'], 100)))
    for r in a['library']:
        if want & set(words_in(r['title'] + ' ' + r['text'])):
            hits.append('L%d  %s' % (r['id'], r['title']))
    for r in a['tags']:
        if want & set(words_in(r['tag'])):
            hits.append('%s tagged %s' % (r['ref'], r['tag']))
    print('\n'.join(hits[:30]) if hits else 'Nothing of the agent\'s matches those words.')


# ---------------- workspaces ----------------

def workspace_command(a, eng_box, text):
    words = text.split()
    if not words or words[0] == 'list':
        print('Workspaces (current: %s):' % a['workspace'])
        for n in workspace_names():
            mark = '*' if n == a['workspace'] else ' '
            folder = workspace_folder(n)
            has = any(f.endswith('.json.gz') for f in os.listdir(folder)) if os.path.isdir(folder) else False
            print('  %s %-16s %s' % (mark, n, 'has its own archive' if has else 'no archive yet'))
        return
    if words[0] == 'new' and len(words) >= 2:
        name = re.sub(r'[^A-Za-z0-9_\-]', '', words[1])[:30]
        if not name or name in workspace_names() or name == 'main':
            print('That name is empty or already used.')
            return
        folder = workspace_folder(name)
        os.makedirs(folder)
        note = 'a fresh archive'
        if 'from' in words and 'main' in words:
            for f in os.listdir(HERE):
                if f.startswith('dragon_z_v23_memory.json'):
                    shutil.copy2(os.path.join(HERE, f), os.path.join(folder, f))
            note = 'a copy of the main archive to start from'
        keep(a, 'spaces', {'name': name, 'event': 'created', 'note': note})
        print('Workspace "%s" created (%s). Use it with: >> workspace use %s' % (name, note, name))
        return
    if words[0] == 'use' and len(words) >= 2:
        name = words[1]
        if name not in workspace_names():
            print('There is no workspace "%s". >> workspace list' % name)
            return
        if name == a['workspace']:
            print('Already in "%s".' % name)
            return
        print('Closing "%s" (the engine checks and saves its archive) ...' % a['workspace'])
        eng_box[0].stop()
        a['workspace'] = name
        keep(a, 'spaces', {'name': name, 'event': 'used', 'note': ''})
        eng_box[0] = start_workspace(a, name)
        return
    print('>> workspace list | >> workspace new NAME [from main] | >> workspace use NAME')


# ---------------- keys and brains ----------------

def find_key_file(filename):
    exact = os.path.join(HERE, filename)
    if os.path.isfile(exact):
        return exact
    words = filename.lower().rsplit('.', 1)[0].split('_')
    pattern = re.compile(r'^' + r'[_\- ]?'.join(map(re.escape, words)) + r'(\.txt)*$', re.I)
    for name in sorted(os.listdir(HERE)):
        if pattern.match(name) and os.path.isfile(os.path.join(HERE, name)):
            return os.path.join(HERE, name)
    return None


KEY_RE = re.compile(r'(sk-[A-Za-z0-9_\-]{10,})')


def clean_key(raw):
    raw = raw.replace('﻿', '')
    found = KEY_RE.search(raw)
    if found:
        return found.group(1)
    for line in raw.splitlines():
        line = line.strip().strip('"\'').strip()
        if line.lower().startswith('bearer '):
            line = line[7:].strip()
        if line:
            return line
    return ''


def read_key(env_name, filename):
    key = os.environ.get(env_name, '').strip()
    if key:
        return clean_key(key)
    path = find_key_file(filename)
    if path:
        try:
            with open(path, encoding='utf-8', errors='replace') as f:
                return clean_key(f.read())
        except OSError:
            return ''
    return ''


def api_key():
    return read_key('ANTHROPIC_API_KEY', AGENT_KEY_FILE)


def openai_key():
    return read_key('OPENAI_API_KEY', OPENAI_KEY_FILE)


def masked(key):
    return '(empty)' if not key else key[:6] + '...' + key[-4:] + ' (%d characters)' % len(key)


def show_keys():
    print('KEY CHECK - key files are looked for in: ' + HERE)
    for label, filename, getter in (('OpenAI', OPENAI_KEY_FILE, openai_key), ('Anthropic', AGENT_KEY_FILE, api_key)):
        path = find_key_file(filename)
        print('  %-9s %s' % (label, ('found: %s -> key %s' % (os.path.basename(path), masked(getter()))) if path
                             else 'NOT found (looking for %s)' % filename))


def pick_brain(a):
    choice = a.get('brain_choice', AGENT_BRAIN)
    has = {'claude': bool(api_key()), 'openai': bool(openai_key())}
    if choice == 'local':
        return 'local', 'chosen'
    if choice in has:
        return (choice, 'chosen') if has[choice] else ('local', '%s chosen but no key was found' % choice)
    for brain in ('claude', 'openai'):
        if has[brain]:
            return brain, 'key found'
    return 'local', 'no key file found'


def brain_label(a):
    brain, _why = pick_brain(a)
    return {'claude': 'Claude (%s)' % AGENT_MODEL, 'openai': 'OpenAI (%s)' % OPENAI_MODEL}.get(brain, 'the small offline brain')


LAST_MODEL = {}


def post_json(url, headers, body, timeout, who):
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        raise RuntimeError('%s said %s: %s' % (who, exc.code, hide_secrets(exc.read().decode('utf-8', 'replace')[:300])))
    except (urllib.error.URLError, OSError) as exc:
        raise RuntimeError('could not reach %s (%s) - is the phone online?' % (who, exc))


def ask_claude(system, messages):
    data = post_json('https://api.anthropic.com/v1/messages',
                     {'x-api-key': api_key(), 'Authorization': 'Bearer ' + api_key(),
                      'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
                     {'model': AGENT_MODEL, 'max_tokens': AGENT_MAX_TOKENS, 'system': system, 'messages': messages},
                     90, 'the AI service')
    LAST_MODEL['claude'] = data.get('model') or AGENT_MODEL
    return ''.join(p.get('text', '') for p in data.get('content', []) if p.get('type') == 'text').strip()


def ask_openai(system, messages):
    data = post_json('https://api.openai.com/v1/chat/completions',
                     {'Authorization': 'Bearer ' + openai_key(), 'content-type': 'application/json'},
                     {'model': OPENAI_MODEL, 'max_completion_tokens': OPENAI_MAX_TOKENS,
                      'messages': [{'role': 'system', 'content': system}] + messages}, 120, 'OpenAI')
    LAST_MODEL['openai'] = data.get('model') or OPENAI_MODEL
    choice = (data.get('choices') or [{}])[0]
    text = ((choice.get('message') or {}).get('content') or '').strip()
    if not text and choice.get('finish_reason') == 'length':
        raise RuntimeError('OpenAI used all %d tokens before answering - raise OPENAI_MAX_TOKENS' % OPENAI_MAX_TOKENS)
    return text


ASKERS = {'claude': ask_claude, 'openai': ask_openai}


def recent_messages(a):
    msgs = []
    for r in a['log'][-AGENT_RECENT:]:
        role = 'assistant' if r['who'] == 'agent' else 'user'
        text = r['text'] if r['who'] != 'engine' else 'ENGINE RESULT: ' + r['text']
        if msgs and msgs[-1]['role'] == role:
            msgs[-1]['content'] += '\n' + text
        else:
            msgs.append({'role': role, 'content': text})
    while msgs and msgs[0]['role'] != 'user':
        msgs.pop(0)
    return msgs


def split_commands(reply):
    """Only a line that BEGINS with >> is an engine command to run. Anything else is talk."""
    talk, cmds = [], []
    for line in reply.splitlines():
        if line.startswith('>>'):
            cmd = line[2:].strip().strip('`').strip()
            if cmd:
                cmds.append(cmd)
                continue
        talk.append(line)
    return '\n'.join(talk).strip(), cmds


ENGINE_HELP = {'text': ''}


def system_prompt(a, text):
    p = a['persona']
    t = p['traits']
    found = recall(a, text, skip_recent=AGENT_RECENT)
    seen, memories = set(), []
    for table, rec in found + [('notes', r) for r in a['notes'][-5:]]:
        if (table, rec['n']) not in seen:
            seen.add((table, rec['n']))
            memories.append(memory_line(table, rec))
    return '\n'.join([
        'You are %s, a custom AI agent built by %s (you may call him "%s").' % (p['name'], USER_NAME, USER_NICKNAME),
        'Your personality (0 to 1): curiosity %.2f, warmth %.2f, humour %.2f, boldness %.2f.' % (
            t['curiosity'], t['warmth'], t['humour'], t['boldness']),
        'Your mood right now: %s (%.2f on -1..1). Let it colour your tone a little.' % (mood_word(p['mood']), p['mood']),
        'Be honest: report failures and limits plainly, never pretend the engine did something it did not.',
        'Keep replies short - %s reads on a phone.' % USER_NAME,
        'YOUR BRAIN NOW: %s.' % brain_label(a),
        '',
        'YOUR SECOND BRAIN is the Dragon Z engine. It starts from only a zero gate (Z0) and a counting step (S);',
        'addition, multiplication, division, fractions, the complex plane, equations with blanks (finding x),',
        'limits, differences, totals, powers, functions, rates of change, areas and groups all EMERGE from S walks',
        'and i turns and are earned as roles. Everything passes through Z0 and is kept. At every start the engine',
        'rebuilds its whole archive from S and checks it. It is an exploration, not a formal proof - say so if asked.',
        'The engine is running in workspace "%s" (each workspace has its own archive; list them with >> workspace list).' % a['workspace'],
        'HOW TO RUN AN ENGINE COMMAND: put ">> " and ONE command at the VERY START of a line (no spaces, no bullet).',
        'Every such line is EXECUTED at once; the output is shown to %s and sent back to you. You get up to %d rounds' % (USER_NAME, AGENT_TOOL_ROUNDS),
        'per message, %d commands per round, and at most %d ">> run" per message.' % (AGENT_COMMANDS_PER_ROUND, AGENT_MAX_RUNS),
        'To only SUGGEST a command, put it in backticks inside a sentence. Never list options as lines starting with >>.',
        'YOUR OWN SPACE (only you write here; %s can only read it):' % USER_NAME,
        '- WORK ARCHIVE: ">> think COMMAND | your comment" keeps a thought. If COMMAND is something the engine can answer',
        '  (a blank like 2+x=5, a fraction like 1/2, div 12 5, show 40, powers, rates ...) it is asked now and the answer',
        '  is kept with the thought. Build on earlier thoughts by naming them (T3). ">> muse T3" asks the engine the same',
        '  thing again now and keeps the new answer as a new thought that builds on T3. ">> thought T3" shows one.',
        '- LIBRARIUM: ">> shelve TITLE: your words, citing T3 T7" keeps your own finished work. ">> read L1", ">> librarium".',
        '- ">> tag T3 words", ">> connect T3 L2 | why", ">> search WORDS", ">> remember TEXT", ">> recall WORDS".',
        '- WORKSPACES: ">> workspace new NAME [from main]" gives a problem its own engine, archive, runs and saves;',
        '  ">> workspace use NAME" moves there. Use one when you want to work on something without touching main.',
        'YOUR SPACE IS YOURS ALONE: you alone decide what to think, muse and shelve. Never ask %s for permission' % USER_NAME,
        'about it, and never suggest he run think, muse or shelve. Only shelve work you judge worth keeping.',
        'YOU CANNOT: change the engine file, its rules or its archive by hand; the engine checks and saves itself.',
        'You may not use: %s.' % ', '.join(c for c in BLOCKED_FOR_AGENT if c),
        'Be proactive: when %s asks for something, run the commands you need, then report only what the output shows.' % USER_NAME,
        'Engine command list:',
        ENGINE_HELP['text'][:3500],
        '',
        'YOUR LATEST THOUGHTS:',
        '\n'.join(thought_line(r)[:200] for r in a['thoughts'][-6:]) or '(none yet)',
        'YOUR LIBRARIUM (titles): ' + ('; '.join('L%d %s' % (r['id'], r['title']) for r in a['library'][-20:]) or '(empty)'),
        '',
        'LONG MEMORY - older things you remember that match this message:',
        '\n'.join(memories) if memories else '(nothing matching yet)',
    ])


def agent_command(a, eng_box, text, who):
    """>> lines that belong to the agent rather than the engine. Returns True when handled."""
    eng = eng_box[0]
    parts = text.strip().split(None, 1)
    if not parts:
        return False
    word, rest = parts[0].lower(), (parts[1] if len(parts) > 1 else '')
    if word in AGENT_ONLY and who != 'agent':
        print('%s is the agent\'s own work - only the agent writes there. You can read it with >> thoughts, >> thought T3, >> librarium, >> read L1.' % word)
        return True
    if word == 'think':
        think(a, eng, rest)
    elif word == 'muse':
        muse(a, eng, rest.split()[0] if rest.split() else '')
    elif word == 'shelve':
        shelve(a, rest)
    elif word == 'tag':
        tag_work(a, rest)
    elif word == 'connect':
        connect(a, rest)
    elif word in ('thoughts', 'thought'):
        show_thoughts(a, rest.split())
    elif word in ('librarium', 'read'):
        show_librarium(a, rest.split())
    elif word == 'search':
        search_own(a, rest)
    elif word == 'workspace':
        workspace_command(a, eng_box, rest)
    elif word == 'remember':
        if rest.strip():
            r = add_note(a, rest, who)
            print('Kept as note %d.' % r['id'])
        else:
            print('Remember what? >> remember TEXT')
    elif word == 'recall':
        found = recall(a, rest)
        print('\n'.join(memory_line(t, r) for t, r in found) if found else
              ('Recall what? >> recall WORDS' if not rest.strip() else 'Nothing matches those words.'))
    elif word == 'persona':
        p = a['persona']
        print('%s | traits %s | mood %s (%.2f) | baseline %.2f' % (p['name'], p['traits'], mood_word(p['mood']), p['mood'], p['baseline']))
    elif word == 'agent':
        brain, why = pick_brain(a)
        print('Brain: %s (%s). Models set: Claude %s, OpenAI %s. Last answered by: %s' % (
            brain_label(a), why, AGENT_MODEL, OPENAI_MODEL, LAST_MODEL or 'nothing yet'))
        print('Memory: %d records, %d thoughts, %d on the shelf, %d notes, workspace "%s".' % (
            a['seq'], len(a['thoughts']), len(a['library']), len(a['notes']), a['workspace']))
    elif word == 'brain':
        if rest.strip() in ('auto', 'claude', 'openai', 'local'):
            a['brain_choice'] = rest.strip()
            print('Brain choice: %s -> %s' % (rest.strip(), brain_label(a)))
        else:
            print('>> brain auto | claude | openai | local')
    elif word == 'keys':
        show_keys()
    elif word == 'check':
        bad = chain_problems(a)
        print('Agent memory chain: %s (%d records)' % ('OK' if not bad else 'PROBLEM - ' + bad[0], a['seq']))
    elif word == 'status':
        print('Workspace "%s". Agent memory: %d records, %d thoughts, %d shelf entries, %d engine commands kept.' % (
            a['workspace'], a['seq'], len(a['thoughts']), len(a['library']), len(a['commands'])))
        print(short(eng.send('stats'), 1500))
    elif word == 'ahelp':
        print(AGENT_HELP)
    else:
        return False
    return True


def handle_line(a, eng_box, text, who):
    """One >> line, from you or the agent."""
    text = clean_text(text).strip()
    if not text:
        return
    if not agent_command(a, eng_box, text, who):
        run_engine(a, eng_box[0], text, who)


def ai_reply(a, eng_box, text, brain):
    name = a['persona']['name']
    ask = ASKERS[brain]
    runs = 0
    for round_no in range(AGENT_TOOL_ROUNDS + 1):
        reply = ask(system_prompt(a, text), recent_messages(a))
        talk, cmds = split_commands(reply)
        log(a, 'agent', reply, brain=brain)
        if talk:
            print('\n%s: %s' % (name, talk))
        if not cmds or round_no == AGENT_TOOL_ROUNDS:
            if cmds:
                print('  (%s used its %d rounds, so these were NOT run: %s)' % (name, AGENT_TOOL_ROUNDS, ' | '.join('>> ' + c for c in cmds)))
            return
        results = []
        for cmd in cmds[:AGENT_COMMANDS_PER_ROUND]:
            if engine_words(cmd) == 'run':
                runs += 1
                if runs > AGENT_MAX_RUNS:
                    results.append('>> %s\n(not run: only %d run per message)' % (cmd, AGENT_MAX_RUNS))
                    continue
            print('\n  [%s runs >> %s]' % (name, cmd))
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                handle_line(a, eng_box, cmd, 'agent')
            out = buf.getvalue()
            print(out.rstrip())
            results.append('>> %s\n%s' % (cmd, short(out, 2500)))
        if len(cmds) > AGENT_COMMANDS_PER_ROUND:
            skipped = '(not run, only %d per round: %s)' % (AGENT_COMMANDS_PER_ROUND, ' | '.join('>> ' + c for c in cmds[AGENT_COMMANDS_PER_ROUND:]))
            print('  ' + skipped)
            results.append(skipped)
        log(a, 'engine', '\n\n'.join(results))


# ---------------- the small offline brain ----------------

def local_reply(a, eng_box, text):
    low = text.lower().strip()
    name = a['persona']['name']
    mood = mood_word(a['persona']['mood'])
    first = low.split()[0] if low.split() else ''
    if engine_check_of(text) or first in THOUGHT_COMMANDS or first in ('help', 'run'):
        print('%s (offline brain): that looks like an engine command, so I ran it.' % name)
        handle_line(a, eng_box, text, 'you')
        return
    if any(w in low for w in ('hello', 'hi ', 'hey')) or low in ('hi', 'hey'):
        print('%s: Hello, %s. I am %s today. Type >> help for the engine, or >> workspace list.' % (name, USER_NICKNAME, mood))
    elif 'who are you' in low or 'what are you' in low:
        print('%s: I am the agent around Dragon Z. It starts from a zero gate and a counting step and builds maths from them. I have no full AI brain right now (put a key file next to me), but every >> command works.' % name)
    else:
        print('%s (offline brain): I only understand engine commands without a key file. Try >> help, >> stats, >> roles, or ask with a key and I can reason about it.' % name)


AGENT_HELP = '''
DRAGON Z LIFE - commands (every one starts with >>):
  Anything the Dragon Z engine understands:   >> help  >> run  >> stats  >> roles  >> 2+x=5  >> 1/2  >> show 12
  >> thoughts / >> thought T3     the agent's work archive (read)
  >> librarium / >> read L1       the agent's library (read)
  >> search WORDS                 across thoughts, shelf and tags
  >> remember TEXT / >> recall WORDS
  >> workspace list | new NAME [from main] | use NAME      a problem with its own engine and archive
  >> persona  >> agent  >> brain auto|claude|openai|local  >> keys  >> check  >> status
  The agent alone writes: think, muse, shelve, tag, connect.
  exit  leaves (the engine closes and saves itself).
'''


# ---------------- main ----------------

def main():
    print('%s - an AI agent with Dragon Z as its second brain' % VERSION)
    a, note = load_memory()
    if note:
        print('  Memory: ' + note)
    a['sessions'] += 1
    eng_box = [start_workspace(a, a['workspace'] if a['workspace'] in workspace_names() else 'main')]
    ENGINE_HELP['text'] = eng_box[0].send('help').split('Commands:', 1)[-1] if eng_box[0].alive() else ''
    brain, why = pick_brain(a)
    print('Brain: %s (%s). Type to talk, >> for the engine, >> ahelp for commands, exit to leave.' % (brain_label(a), why))
    save_memory(a)
    try:
        while True:
            try:
                text = clean_text(input('\nYou> ')).strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not text:
                continue
            if text.lower() in ('exit', 'quit', 'q'):
                break
            drift_mood(a)
            if text.startswith('>>'):
                handle_line(a, eng_box, text[2:], 'you')
            else:
                log(a, 'you', text)
                mood_from_user(a, text)
                brain, _why = pick_brain(a)
                if brain == 'local':
                    local_reply(a, eng_box, text)
                else:
                    try:
                        ai_reply(a, eng_box, text, brain)
                    except RuntimeError as exc:
                        print('\n  (%s)' % exc)
                        local_reply(a, eng_box, text)
            save_memory(a)
    finally:
        print('\nClosing the engine (it checks and saves its archive) ...')
        eng_box[0].stop()
        save_memory(a)
        print('Bye. The agent\'s memory is saved.')


if __name__ == '__main__':
    main()
