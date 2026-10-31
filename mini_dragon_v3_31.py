# Mini Dragon - Zero Theorem engine with an AI agent
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
# MINI DRAGON v3.31 - basic Zero Theorem engine + algebra + calculus + AGENT
# ============================================================
# NEW in v3.31: the agent's next requests - automatic tags on every engine record
#   and thought (>> filter blocked limit), a STATUS dashboard (>> status), a DIGEST
#   of what is new (>> digest), the maintenance routine in one command
#   (>> maintain), dated SNAPSHOT copies of both memory files (>> snapshot), and
#   the agent may tag engine records in its own space (>> tag #123 ...).
# From v3.30: invisible control characters (like the ^@ Pydroid adds when
#   pasting) are removed from what you type, so >> commands are always seen
#   and messages are kept whole; old messages holding them now display whole
#   too (nothing in memory is changed). >> recall with no words shows how to
#   use it. The agent is told how many batches it may run per command.
# From v3.29: Mini Dragon's own requests - TAGS (>> tag T3 golden ratio),
#   SEARCH across its thoughts and Librarium (>> search WORDS, anyone may look)
#   and CROSS-LINKS between thoughts and shelf entries (>> connect T3 L2 | why).
#   tag and connect are the agent's alone; nothing is ever removed; every tag
#   and link passes through Z0. Thoughts show which shelf entries cite them.
# From v3.28: at start, a NOTICE when the chosen AI brain runs a small model
#   (it may skip some instructions - a known gap, left as it is on purpose).
# From v3.27: >> agent shows the model set for each brain, and the model the
#   AI service says actually answered the last message (proof, not a label).
#   OpenAI model set to gpt-6-luna.
# From v3.26: the agent's own WATCH LIST (>> watch PATTERN, agent only;
#   >> watches to look) - it sees a pattern and its parts appear. The agent
#   now knows which brain it runs on, old offline-brain replies are labelled,
#   and a short reminder before every message keeps its work its own.
# From v3.25: the agent is told its work archive and Librarium decisions
#   are its own - it never asks a human for permission or choices about them.
# From v3.24: the Claude brain sends its key both ways Anthropic accepts.
# From v3.23: licence notice; key files must have their real name;
#   anything that looks like an API key is hidden before it is saved in the
#   agent's memory or sent to the AI. Keep secrets off GitHub with .gitignore.
# From v3.22: the agent's personal WORK ARCHIVE (thoughts build on thoughts
#   with T3 / #12, and  >> muse T3  sends a thought through the zero engine)
#   and its LIBRARIUM (>> shelve). Only the agent writes to them - no human
#   interference; you can read them.
# From v3.21: THOUGHTS - a blank workspace in the engine where the agent
#   tries its own maths (>> think limit(log(x), x, 0, '+')), e.g. to work on
#   blocked records. Computed inside Z0, kept forever, kept apart from the
#   engine's own discoveries.
# From v3.20: the agent only runs a >> line when it means to (suggestions
#   in `backticks` are shown, not run); it acts instead of asking.
# From v3.19: key files are found even as openai_key.txt.txt or OpenAI_Key.txt;
#   >> keys shows what the agent can see; you are called Little Bunny / Wabbit;
#   plain engine words (help, stats, zero ...) work without >>; exit leaves;
#   cleaner recall; >> all symbolic / all complex / all constants.
# From v3.18: the agent can also use OpenAI (put your key in openai_key.txt).
# From v3.17: a custom AI agent with the engine as its second brain.
#   Type normally          -> talk to the agent
#   Type >> then a command -> straight to the engine  (>> help, >> run, >> 5)
#   Small personality engine (traits + mood) and long persistent memory in
#   mini_dragon_agent_memory.json (nothing deleted, everything through Z0).
#   Full AI brain: an OpenAI key in openai_key.txt, or an Anthropic key in
#   agent_key.txt, next to this file. Without a key: a small offline brain. See AGENT START below.
# ============================================================
# Needs SymPy (the maths library). In Pydroid3:
#     menu -> Pip -> type  sympy  -> Install.   Then run this file.
#
# How it works, in plain words:
#   1. GIVEN operands: digits 0-9, i, and the variable x.
#      NOT given: -i, e, pi. They have to come out of the work.
#   2. GIVEN operations:
#        two-input:  + - * / **  and  compose  (put one expression into x)
#        one-input:  sqrt, d/dx, integral, limit x->0, sin cos tan,
#                    asin acos atan, exp, log, expand, factor, solve(=0)
#   3. Every expression gets every one-input operation, and is combined
#      with every earlier expression (and itself), both orders, every
#      two-input operation.
#   4. Every result is kept (zero and repeats included), saved, and fed
#      back in. Each run does a batch, saves, and the next run carries on.
#
# Things that cannot give a value (divide by 0, log(0), infinities,
# integrals with no formula...) are COUNTED with the reason, not hidden.
# Jobs that are too slow or too big for a phone are PARKED, not deleted,
# and can be retried later.
#
# Its memory file is separate, so older engines' files are never touched.
# This is a computational exploration, not a mathematical proof.

import cmath
import hashlib
import heapq
import json
import os
import re
import shutil
import signal
import time

try:
    import mpmath
    import sympy as sp
    from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                            implicit_multiplication, convert_xor)
except ImportError:
    print('This engine needs SymPy.')
    print('In Pydroid3: menu -> Pip -> type sympy -> Install. Then run again.')
    raise SystemExit

# ---------------- SETTINGS (change freely) ----------------
OPERANDS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'i', 'x']
BINARY = ['+', '-', '*', '/', '**', 'compose']
UNARY = ['sqrt', 'd/dx', 'integral', 'limit x->0', 'sin', 'cos', 'tan',
         'asin', 'acos', 'atan', 'exp', 'log', 'expand', 'factor', 'solve']
WORK_PER_RUN = 1000   # jobs tried each run
OP_SECONDS = 2.0      # a single job slower than this is PARKED (None = no limit)
MAX_SIZE = 40         # results with more operations than this are PARKED
MAX_DIGITS = 300      # results with numbers longer than this are PARKED
MAX_POWER = 12        # ** with a plain-number exponent bigger than this is PARKED
                      # Change any guard (or set to None) and parked jobs
                      # are retried automatically on the next run.
CLOCKS_ON = True      # stamp every record with the four clocks
# 00404 slot machine: each reference is broken into units (0 stays 0, every
# other digit d becomes d ones: 00404 -> 00111101111). Every gap between two
# symbols is a slot: left unused (digits join into a longer number - no cap at
# 9) or filled with an operation. An operation is only offered to the slots
# once the engine has produced a new value with it (emerged).
SLOT_REFERENCES = ['00404']
SLOT_OPS = ['join', '+', '-', '*', '/', '**']
SLOT_WORK_PER_RUN = 200   # slot fillings tried each run (the rest wait, saved)
OLD_MEMORIES = {'v1': 'mini_dragon_memory.json', 'v2': 'mini_dragon_v2_memory.json'}
PLANE_SECONDS = 0.5   # time allowed to place one value in the plane
EQUAL_SECONDS = 0.5   # time allowed to fingerprint / prove one link when first made
PROOF_SECONDS = 2.0   # time allowed per retry in the proof queue
PROOF_WORK_PER_RUN = 20     # numeric links / unchecked values retried each run
SWAP_WORK_PER_RUN = 200     # records checked each run for exact-link swaps
EQUAL_BACKFILL_PER_RUN = 2000  # older values fingerprinted per run (upgrades)
MAX_COMPARE = 3             # group members a new value is compared with, at most
EQUAL_WORK_SECONDS = 10.0   # most time per run for link upkeep (rest waits, saved)
# Priority selectors: the observer scores each new value; the highest score
# waiting gets its full turn next (every one-input op + pairing with every
# given operand). Nothing is skipped - important values just go first.
PRIORITY_SCORES = {'watched': 100, 'milestone': 80, 'plane_first': 60,
                   'simple_constant': 40, 'simple_x': 20}
SIMPLE_LENGTH = 10          # a value written in at most this many characters is 'simple'
BACKUP_ON_SAVE = True # keep the previous good save as <memory>.bak
MEMORY_FILE = 'mini_dragon_v3_memory.json'
# Values the observer reports by name when they first appear (add your own):
WATCH = ['-i', 'e', 'pi', '-1', '1/2', '-1/2', '10', '-10', '100', 'sqrt(2)',
         '2*pi', 'pi/2', 'I*pi', '1+i', '(1+sqrt(5))/2', 'x^2', 'x^3/3',
         'exp(x)', 'log(x)', 'sin(x)', 'cos(x)', '-sin(x)', '1/x', 'sqrt(x)']
# -----------------------------------------------------------

X = sp.Symbol('x')
USER_NAMES = {'x': X, 'i': sp.I, 'I': sp.I, 'e': sp.E, 'E': sp.E, 'pi': sp.pi}
STORED_NAMES = {'x': X, 'I': sp.I, 'E': sp.E, 'pi': sp.pi}
USER_RULES = standard_transformations + (implicit_multiplication, convert_xor)


def memory_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), MEMORY_FILE)


def read_user(text):
    """What you type: 2x, x^2, 3-2i, sqrt(2), e, pi ..."""
    value = parse_expr(text, local_dict=USER_NAMES, transformations=USER_RULES)
    if not isinstance(value, sp.Basic):
        value = sp.sympify(value)
    extra = value.free_symbols - {X}
    if extra:
        raise ValueError('only x is a variable here (not %s)' % ', '.join(map(str, extra)))
    return value


def read_stored(text):
    return parse_expr(text, local_dict=STORED_NAMES)


# ---------------- outcomes ----------------

class Blocked(Exception):
    """No value exists for this job (e.g. divide by zero)."""


class Skip(Exception):
    """The operation does not apply (e.g. solve with no x in it)."""


class ParkIt(Exception):
    """Too big for the phone right now; saved to retry later."""


class TooSlow(BaseException):
    """BaseException so SymPy's own error handling can't swallow it."""


CAN_TIME = hasattr(signal, 'SIGALRM') and hasattr(signal, 'setitimer')


def _alarm(signum, frame):
    raise TooSlow()


def run_timed(func, seconds=None):
    seconds = OP_SECONDS if seconds is None else seconds
    if not CAN_TIME or seconds is None:
        return func()
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return func()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


# ---------------- the maths ----------------

def unary(op, a):
    if op == 'sqrt':
        return [sp.sqrt(a)]
    if op == 'd/dx':
        return [sp.diff(a, X)]
    if op == 'integral':
        r = sp.integrate(a, X)
        if r.has(sp.Integral):
            raise Blocked('no_integral_formula')
        return [r]  # constant of integration C = 0 shown; full answer is this + C
    if op == 'limit x->0':
        r = sp.limit(a, X, 0)
        if r.has(sp.Limit):
            raise Blocked('limit_not_found')
        return [r]
    if op in ('sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'exp', 'log'):
        return [getattr(sp, op)(a)]
    if op == 'expand':
        return [sp.expand(a)]
    if op == 'factor':
        return [sp.factor(a)]
    if op == 'solve':
        if not a.has(X):
            raise Skip('solve_needs_x')
        return list(sp.solve(sp.Eq(a, 0), X))
    raise ValueError('unknown operation ' + op)


def binary(op, a, b):
    if op == '+':
        return [a + b]
    if op == '-':
        return [a - b]
    if op == '*':
        return [a * b]
    if op == '/':
        if b.is_zero:
            raise Blocked('division_by_zero')
        return [a / b]
    if op == '**':
        if (MAX_POWER is not None and b.is_Rational and a not in (0, 1, -1)
                and (abs(b.p) > MAX_POWER or b.q > MAX_POWER)):
            raise ParkIt('power_guard')
        return [a ** b]
    if op == 'compose':
        if not a.has(X):
            raise Skip('compose_needs_x')
        if not b.has(X):  # putting a number into x: check the size first
            try:
                safe_estimate(a, safe_estimate(b))
            except TooBig:
                raise ParkIt('too_big_to_evaluate')
        return [a.subs(X, b)]
    raise ValueError('unknown operation ' + op)


UNDEFINED = (sp.nan, sp.zoo, sp.oo, -sp.oo)


def problem_with(value):
    if value.has(*UNDEFINED) or value.has(sp.AccumBounds):
        return 'blocked', 'undefined_or_infinite'
    if MAX_SIZE is not None and sp.count_ops(value) > MAX_SIZE:
        return 'parked', 'too_big'
    if MAX_DIGITS is not None:
        for n in value.atoms(sp.Rational):
            if max(abs(int(n.p)).bit_length(), int(n.q).bit_length()) * 0.302 > MAX_DIGITS:
                return 'parked', 'too_many_digits'
    return None, None


def kind_of(value):
    if value.has(X):
        return 'symbolic'
    if value.is_Rational:
        return 'rational'
    if value.has(sp.I):
        return 'complex'
    return 'constant'


# ---------------- THE FOUR CLOCKS ----------------
# 1. Zero clock    - starts at T0 = 0, ticks once per passage through Z0.
# 2. Wall clock    - the phone's real date and time (the phone can change it).
# 3. Elapsed clock - time since this session started; never goes backwards.
# 4. CPU clock     - processor time the engine has used this session.
# Elapsed and CPU restart every session (each time you start the program),
# so every stamp also records its session number. Times are never invented
# for records made before the clocks existed.

SESSION = {'id': None, 'mono0': time.monotonic_ns(), 'cpu0': time.process_time_ns()}


def clock_state(m):
    return m.setdefault('clock', {'sessions': 0, 'runs': [], 'op_time_ns': {},
                                  'started_at_record': len(m['expressions'])})


def start_session(m):
    c = clock_state(m)
    c['sessions'] += 1
    SESSION.update(id=c['sessions'], mono0=time.monotonic_ns(),
                   cpu0=time.process_time_ns())


def read_clocks(m):
    """[zero tick, session, wall ms, elapsed microseconds, CPU microseconds]"""
    return [zero_state(m)['passages'], SESSION['id'], time.time_ns() // 1000000,
            (time.monotonic_ns() - SESSION['mono0']) // 1000,
            (time.process_time_ns() - SESSION['cpu0']) // 1000]


def wall_text(ms):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ms / 1000))


def clock_line(t):
    return ('zero tick %d | %s | %.3f s elapsed, %.3f s CPU into session %d'
            % (t[0], wall_text(t[2]), t[3] / 1e6, t[4] / 1e6, t[1]))


# ---------------- ZERO GATE (Z0) ----------------
# Everything that comes from 0 goes back through 0.
# Every operation runs through zero_gate, and every archive record - values,
# given operands, blocked and parked records alike - passes through it and is
# stamped with its passage number. Passing through 0 never changes a value
# or a path; it records that the path went through Z0.

ZERO_RULE = 'everything_through_zero_mini_v1'
# Under these rules these reasons can never give a value, so Z0 keeps them as
# records but does not resend them. Every other blocked reason (SymPy could not,
# no integral formula, limit not found) is resent to Z0 when the rules change.
FINAL_REASONS = ('division_by_zero', 'undefined_or_infinite', 'no_solution')


def zero_state(m):
    return m.setdefault('zero', {'rule': ZERO_RULE, 'nexus': 'Z0',
                                 'passages': 0, 'record_passages': 0,
                                 'historical_backfill': 0, 'updates': 0,
                                 'operations': {}, 'returned_to_zero': 0,
                                 'rules_seen': None})


def zero_gate(m, what, **kw):
    """The single gate. what = 'operation', 'record' or 'update'."""
    z = zero_state(m)
    z['passages'] += 1
    if what == 'operation':
        job, args = kw['job'], kw['args']
        z['operations'][job[1]] = z['operations'].get(job[1], 0) + 1
        start = time.monotonic_ns()
        try:
            if job[0] == 'u':
                return unary(job[1], args[0])
            if job[0] == 's':  # exact-link swap: replace one spelling by an equal one
                return [args[0].subs(args[1], args[2])]
            return binary(job[1], args[0], args[1])
        finally:  # elapsed time per operation, even if it was too slow
            spent = clock_state(m)['op_time_ns']
            spent[job[1]] = spent.get(job[1], 0) + time.monotonic_ns() - start
    if what == 'record':
        rec = kw['record']
        if 'z0' in rec:
            return rec  # already passed through 0
        z['record_passages'] += 1
        rec['z0'] = z['record_passages']
        if kw.get('historical'):
            rec['z0_backfill'] = True  # existed before the gate; passed now
            z['historical_backfill'] += 1
        elif CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    if what == 'update':  # a parked/blocked record changed status
        rec = kw['record']
        z['updates'] += 1
        entry = [z['passages'], rec.get('status')]
        if CLOCKS_ON and SESSION['id'] is not None:
            entry.append(read_clocks(m))
        rec.setdefault('z0_updates', []).append(entry)
        return rec
    if what == 'thought':  # the agent's own maths, computed inside Z0
        z['operations']['thought'] = z['operations'].get('thought', 0) + 1
        start = time.monotonic_ns()
        try:
            return kw['func']()
        finally:
            spent = clock_state(m)['op_time_ns']
            spent['thought'] = spent.get('thought', 0) + time.monotonic_ns() - start
    if what == 'thought_record':  # a thought kept in the agent's workspace
        rec = kw['record']
        z['thought_passages'] = z.get('thought_passages', 0) + 1
        rec['z0t'] = z['thought_passages']
        rec['tick'] = z['passages']
        if CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    if what == 'watch_record':  # a watch the agent starts, or a sighting of one
        rec = kw['record']
        z['watch_passages'] = z.get('watch_passages', 0) + 1
        rec['z0w'] = z['watch_passages']
        rec['tick'] = z['passages']
        if CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    if what in ('tag_record', 'connect_record', 'digest_record'):  # the agent tags or cross-links its own work
        rec = kw['record']
        z[what + '_passages'] = z.get(what + '_passages', 0) + 1
        rec[{'tag_record': 'z0tag', 'connect_record': 'z0con'}.get(what, 'z0dig')] = z[what + '_passages']
        rec['tick'] = z['passages']
        if CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    if what == 'shelf_record':  # an entry the agent shelves in its Librarium
        rec = kw['record']
        z['shelf_passages'] = z.get('shelf_passages', 0) + 1
        rec['z0s'] = z['shelf_passages']
        rec['tick'] = z['passages']
        if CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    if what == 'agent':  # a chat message, note or mood change of the agent
        rec = kw['record']
        z['agent_passages'] = z.get('agent_passages', 0) + 1
        rec['z0a'] = z['agent_passages']
        rec['tick'] = z['passages']
        if CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    raise ValueError('unknown zero gate passage: ' + what)


def zero_report(m):
    z = zero_state(m)
    missing = [r['id'] for r in m['expressions'] if 'z0' not in r]
    stamps = [r['z0'] for r in m['expressions'] if 'z0' in r]
    ok = not missing and len(set(stamps)) == len(stamps)
    return {'complete': ok, 'records': len(m['expressions']),
            'passed': len(stamps), 'missing': missing[:20],
            'counter_matches': z['record_passages'] == len(m['expressions'])}


def zero_repair(m):
    """Before saving: anything that missed the gate passes through 0 NOW.
    Nothing is refused or dropped; late passages are marked and logged."""
    z = zero_state(m)
    missing = [r for r in m['expressions'] if 'z0' not in r]
    if not missing:
        return 0
    # Continue numbering after the highest stamp so no two records share one.
    z['record_passages'] = max([r['z0'] for r in m['expressions'] if 'z0' in r] or [0])
    for rec in missing:
        zero_gate(m, 'record', record=rec)
        rec['z0_late'] = True
    z['late_passages'] = z.get('late_passages', 0) + len(missing)
    z.setdefault('repairs', []).append({'run': m['runs'], 'count': len(missing),
                                        'ids': [r['id'] for r in missing[:50]]})
    return len(missing)


def rules_signature():
    return json.dumps([OPERANDS, BINARY, UNARY, guards(), sp.__version__])


# ---------------- THE OBSERVER (emergent information net) ----------------
# Watches every value the moment it first appears. It never changes a value,
# a path or a job - it only notes what emerged, when, and which milestone
# (first negative, first fraction, first x^3 ...) it was.

def observer_state(m):
    return m.setdefault('observer', {'milestones': {}, 'first_by_op': {},
                                     'first_by_depth': {}, 'runs': {},
                                     'backfilled': []})


def milestone_names(value):
    """Plain-language labels for what kind of new thing this value is."""
    names = []
    if value.has(X):
        names.append('first with x')
        try:
            poly = sp.Poly(value, X)
            names.append('first polynomial of degree %d' % poly.degree())
        except sp.PolynomialError:
            pass
        for f, label in ((sp.sin, 'sin'), (sp.cos, 'cos'), (sp.tan, 'tan'),
                         (sp.exp, 'exp'), (sp.log, 'log'), (sp.asin, 'asin'),
                         (sp.acos, 'acos'), (sp.atan, 'atan')):
            if value.has(f):
                names.append('first %s with x' % label)
        if value.has(sp.I):
            names.append('first x mixed with i')
    elif value.is_Rational:
        if value.is_Integer:
            n = int(value)
            if n < 0:
                names.append('first negative whole number')
            for size in (10, 100, 1000, 10 ** 6):
                if n >= size:
                    names.append('first whole number >= %d' % size)
                if n <= -size:
                    names.append('first whole number <= -%d' % size)
        else:
            names.append('first fraction')
            if value < 0:
                names.append('first negative fraction')
    else:
        re_part, im_part = value.as_real_imag()
        if im_part != 0:
            names.append('first complex number')
            if re_part == 0:
                if value != sp.I:
                    names.append('first pure imaginary (not i)')
            elif re_part.is_Rational and im_part.is_Rational:
                names.append('first a+bi with whole/fraction parts')
        else:
            names.append('first irrational number')
            if value.has(sp.pi):
                names.append('first number with pi')
            if value.has(sp.E) or value.has(sp.exp):
                names.append('first number with e')
            if any(a.is_Pow and a.exp == sp.Rational(1, 2) for a in sp.preorder_traversal(value)):
                names.append('first square root')
    return names


def timed_milestones(m, idx, value):
    """The observer gets the same time limit as every operation. Some SymPy
    checks (e.g. splitting asin(3)/sqrt(1 + asin(3)**2) into real and
    imaginary parts) can take minutes. If it runs out of time the value is
    still kept - it just isn't classified, and that is logged."""
    try:
        return run_timed(lambda: milestone_names(value))
    except TooSlow:
        slow = observer_state(m).setdefault('too_slow_to_classify', [])
        slow.append(idx)
        return []
    except Exception:
        return []


# ---------------- SAFETY CHECK BEFORE EVALUATING ----------------
# Some values are towers of powers. Evaluating them exactly makes Python build
# a gigantic whole number, which the timer cannot interrupt and which can use
# gigabytes of memory. So before any numeric evaluation, the value is first
# estimated with ordinary phone-sized numbers (bounded work, no giant numbers).
# If that overflows, the value is "too big to evaluate safely": still kept,
# only that check is skipped and logged.

class TooBig(Exception):
    pass


SAFE_FUNCS = {sp.sin: cmath.sin, sp.cos: cmath.cos, sp.tan: cmath.tan,
              sp.asin: cmath.asin, sp.acos: cmath.acos, sp.atan: cmath.atan,
              sp.sinh: cmath.sinh, sp.cosh: cmath.cosh, sp.tanh: cmath.tanh,
              sp.asinh: cmath.asinh, sp.acosh: cmath.acosh, sp.atanh: cmath.atanh,
              sp.exp: cmath.exp, sp.log: cmath.log,
              sp.cot: lambda z: 1 / cmath.tan(z), sp.sec: lambda z: 1 / cmath.cos(z),
              sp.csc: lambda z: 1 / cmath.sin(z), sp.coth: lambda z: 1 / cmath.tanh(z),
              sp.sech: lambda z: 1 / cmath.cosh(z), sp.csch: lambda z: 1 / cmath.sinh(z),
              sp.acot: lambda z: cmath.atan(1 / z), sp.acoth: lambda z: cmath.atanh(1 / z),
              sp.Abs: lambda z: complex(abs(z)), sp.re: lambda z: complex(z.real),
              sp.im: lambda z: complex(z.imag), sp.arg: lambda z: complex(cmath.phase(z)),
              sp.conjugate: lambda z: z.conjugate()}
SAFE_LIMIT = 1e300


def safe_estimate(expr, x_value=None, depth=0):
    """Estimate a value with plain complex numbers. Raises TooBig on overflow."""
    if depth > 200:
        raise TooBig('too deeply nested')
    try:
        if expr.is_Integer or expr.is_Rational:
            if max(abs(int(expr.p)).bit_length(), int(expr.q).bit_length()) > 990:
                raise TooBig('number too long')
            out = complex(int(expr.p) / int(expr.q))
        elif expr is sp.I:
            out = 1j
        elif expr is sp.pi:
            out = complex(cmath.pi)
        elif expr is sp.E:
            out = complex(cmath.e)
        elif expr == X:
            if x_value is None:
                raise TooBig('x has no value here')
            out = complex(x_value)
        elif expr.is_Float:
            out = complex(float(expr))
        elif expr.is_Add:
            out = sum(safe_estimate(a, x_value, depth + 1) for a in expr.args)
        elif expr.is_Mul:
            out = 1
            for a in expr.args:
                out *= safe_estimate(a, x_value, depth + 1)
        elif expr.is_Pow:
            base = safe_estimate(expr.base, x_value, depth + 1)
            power = safe_estimate(expr.exp, x_value, depth + 1)
            if base == 0:
                out = 0j if power.real > 0 else complex('inf')
            else:
                # |base^power| = exp(Re(power*log(base))): check size BEFORE computing
                if (power * cmath.log(base)).real > 690:
                    raise TooBig('power too large')
                out = base ** power
        elif expr.func in SAFE_FUNCS:
            arg = safe_estimate(expr.args[0], x_value, depth + 1)
            if expr.func is sp.exp and arg.real > 690:
                raise TooBig('exp too large')
            out = SAFE_FUNCS[expr.func](arg)
        else:
            raise TooBig('unknown function ' + type(expr).__name__)
    except (OverflowError, ZeroDivisionError, ValueError) as exc:
        raise TooBig(str(exc)[:40])
    if not (abs(out) < SAFE_LIMIT):
        raise TooBig('too large')
    return out


def safe_to_evaluate(value, x_value=None):
    safe_estimate(value, x_value)  # raises TooBig if it isn't
    return True


# ---------------- THE PLANE: positive, negative, i, -i ----------------
# Every new number is placed in the plane: on one of the four directions,
# in a quarter between two of them, or at 0. Values with x are not single
# points, so they stay off the plane. Placing never changes a value.

REGIONS = {(0, 0): '0', (1, 0): '+', (-1, 0): '-', (0, 1): '+i', (0, -1): '-i',
           (1, 1): 'Q1 (+ and +i)', (-1, 1): 'Q2 (- and +i)',
           (-1, -1): 'Q3 (- and -i)', (1, -1): 'Q4 (+ and -i)'}
REGION_ALIASES = {'0': '0', '+': '+', '-': '-', 'i': '+i', '+i': '+i', '-i': '-i',
                  'q1': 'Q1 (+ and +i)', 'q2': 'Q2 (- and +i)',
                  'q3': 'Q3 (- and -i)', 'q4': 'Q4 (+ and -i)'}


def plane_state(m):
    return m.setdefault('plane', {'region': {}, 'count': {}, 'first': {},
                                  'reach': {}, 'numeric_signs': 0,
                                  'unplaced': [], 'off_plane': 0})


def sign_of(v):
    """Exact sign where SymPy can prove it; otherwise a 30-digit numeric
    check (counted separately, since that is evidence, not proof)."""
    if v == 0:
        return 0, False
    if v.is_positive:
        return 1, False
    if v.is_negative:
        return -1, False
    n = v.evalf(30)
    if not n.is_number or not n.is_real:
        raise ValueError('sign unknown')
    if abs(n) < sp.Float('1e-25'):
        raise ValueError('too close to 0 to tell')
    return (1 if n > 0 else -1), True


def place_value(value):
    if not value.is_Rational:
        safe_to_evaluate(value)  # TooBig -> counted as 'could not be placed'
    if value.is_Rational:
        re_part, im_part = value, sp.Integer(0)
    else:
        re_part, im_part = value.as_real_imag()
    (sr, nr), (si, ni) = sign_of(re_part), sign_of(im_part)
    def size(part):  # bigger than a phone's decimal numbers can hold -> 1e308
        try:
            f = float(part.evalf())
        except (OverflowError, TypeError, ValueError):
            f = float('inf') if part.is_positive else float('-inf') if part.is_negative else 0.0
        return max(-1e308, min(1e308, f))
    return REGIONS[(sr, si)], size(re_part), size(im_part), nr or ni


def place(m, idx, value):
    """Put a new value in the plane and update the observer's map."""
    pl = plane_state(m)
    key = m['expressions'][idx]['value']
    if value.has(X):
        pl['off_plane'] += 1
        return None
    try:
        region, re_f, im_f, numeric = run_timed(lambda: place_value(value), PLANE_SECONDS)
    except TooSlow:
        pl['unplaced'].append([idx, 'too_slow'])
        return None
    except Exception as exc:
        pl['unplaced'].append([idx, str(exc)[:40]])
        return None
    pl['region'][key] = region
    pl['count'][region] = pl['count'].get(region, 0) + 1
    pl['numeric_signs'] += numeric
    new_region = region not in pl['first']
    pl['first'].setdefault(region, idx)
    # how far the engine has reached in each of the four directions
    for direction, amount in (('+', re_f), ('-', -re_f), ('+i', im_f), ('-i', -im_f)):
        best = pl['reach'].get(direction)
        if amount > 0 and (best is None or amount > best[0]):
            pl['reach'][direction] = [amount, idx]
    return region if new_region else None


def plane_label(m, key):
    return plane_state(m)['region'].get(key)


# ---------------- EQUAL-VALUE LINKS ----------------
# The same thing can be written different ways (i**i and exp(-pi/2), or
# (x+1)**2 and x**2+2*x+1). Both pathways are always kept separately -
# nothing is ever merged. Every equality check becomes an ARCHIVE RECORD that
# passes through Z0 with clock stamps; its parents are the two values compared:
#   exact     - SymPy proved them equal (the proof method is saved)
#   numeric   - 30-digit check agrees, not proved yet (queued for retries)
#   different - same leading digits, but proved NOT equal
#   unchecked - the value couldn't be fingerprinted in time (queued for retry)
# Numbers are compared directly; expressions with x are compared at two test
# points (one real, one complex) - a weaker check, labelled as such.
# Exact links feed back: 0 swaps one spelling for the other inside other
# expressions, making new pathways.

# Third point lies outside the usual safe ranges (|Im| > pi, Re > pi), so
# look-alikes such as log(exp(x)) and x, or sqrt(x**2) and acos(cos(x)), split.
X_POINTS = (sp.Rational(7, 3), sp.Rational(-11, 5) + sp.I / 7, 5 + 4 * sp.I)


def equal_state(m):
    eq = m.setdefault('equal', {})
    if 'pairs' not in eq:  # new layout (v3.15); older link lists converted below
        old = dict(eq)
        eq.clear()
        eq.update({'keys': {}, 'buckets': {}, 'links': {}, 'pairs': {},
                   'proof_queue': [], 'fp_queue': [], 'swap_links': [],
                   'swap': {'link': 0, 'scan': 0, 'dir': 0}, 'backfill': 0,
                   'old_layout': old})
    return eq


def to_mp(part):
    """A SymPy number as a plain 30-digit decimal (fast, no exact maths)."""
    return mpmath.mpf(sp.Float(part, 30)._mpf_)


def part_keys(part, size):
    """Two keys per number part: rounded and cut at 15 digits. Two equal numbers
    can only miss each other if they straddle BOTH grids - far rarer.
    Plain decimal arithmetic only: exact SymPy log/floor here took minutes."""
    if abs(part) < mpmath.mpf('1e-25') * size:
        return ('0', '0')
    sign = '-' if part < 0 else ''
    mag = abs(part)
    e = int(mpmath.floor(mpmath.log10(mag)))
    scaled = mag / mpmath.mpf(10) ** e * mpmath.mpf(10) ** 14
    return ('%s%de%d' % (sign, int(mpmath.floor(scaled + mpmath.mpf('0.5'))), e),
            '%s%de%d' % (sign, int(mpmath.floor(scaled)), e))


def real_imag(n):
    """Fully worked-out real and imaginary parts (no leftover re(...)/im(...))."""
    parts = (sp.re(n).evalf(30), sp.im(n).evalf(30))
    if not all(p.is_Number for p in parts):
        raise ValueError('could not work out the number fully')
    return parts


def number_keys(n):
    with mpmath.workdps(30):  # 30-digit working precision, local to this step
        re_part, im_part = (to_mp(p) for p in real_imag(n))
        size = max(abs(re_part), abs(im_part), mpmath.mpf(1))
        r, i = part_keys(re_part, size), part_keys(im_part, size)
    return [r[0] + '|' + i[0], r[1] + '|' + i[1]]


def sample(value):
    """30-digit sample(s): the number itself, or the expression at 2 points."""
    if value.has(X):
        for pt in X_POINTS:
            safe_to_evaluate(value, complex(pt))
        out = [sp.N(value.subs(X, pt), 30) for pt in X_POINTS]
    else:
        safe_to_evaluate(value)
        out = [sp.N(value, 30)]
    for n in out:
        if n.has(sp.nan, sp.zoo, sp.oo, -sp.oo) or not n.is_number:
            raise ValueError('no finite sample')
    return out


def keys_for(samples):
    per = [number_keys(n) for n in samples]
    return ['#'.join(k[j] for k in per) + ('@x' if len(samples) > 1 else '')
            for j in (0, 1)]


def close(sa, sb):
    with mpmath.workdps(30):
        return _close(sa, sb)


def _close(sa, sb):
    if len(sa) != len(sb):
        return False
    for a, b in zip(sa, sb):
        ar, ai = (to_mp(p) for p in real_imag(a))
        br, bi = (to_mp(p) for p in real_imag(b))
        if abs(mpmath.mpc(ar, ai) - mpmath.mpc(br, bi)) > mpmath.mpf('1e-24') * max(1, abs(mpmath.mpc(ar, ai))):
            return False
    return True


PROOF_METHODS = (
    ('simplify', lambda a, b: sp.simplify(a - b)),
    ('rewrite_exp', lambda a, b: sp.simplify(a.rewrite(sp.exp) - b.rewrite(sp.exp))),
    ('rewrite_log', lambda a, b: sp.simplify(a.rewrite(sp.log) - b.rewrite(sp.log))),
    ('expand_complex', lambda a, b: sp.expand_complex(a - b)),
    ('trigsimp', lambda a, b: sp.trigsimp(a - b)),
)


def prove_equal(a, b):
    """(True, method) proved equal | (False, method) proved different |
    (None, None) could not tell in the time allowed."""
    for name, method in PROOF_METHODS:
        diff = method(a, b)
        if diff == 0:
            return True, name
        if diff.is_number and diff.is_zero is False:
            return False, name
    return None, None


def first_id(m, key):
    return m['results'][key][0]


def add_link_record(m, kind, parents, extra):
    idx = len(m['expressions'])
    depth = 1 + max(m['expressions'][p]['depth'] for p in parents)
    rec = {'id': idx, 'value': None, 'status': 'link', 'kind': kind,
           'op': 'equal?', 'parents': list(parents), 'depth': depth}
    rec.update(extra)
    zero_gate(m, 'record', record=rec)
    m['expressions'].append(rec)
    return idx


def set_link_kind(m, rid, kind, method=None):
    """Upgrade a link (numeric -> exact/different); passes back through 0."""
    rec = m['expressions'][rid]
    rec['kind'] = kind
    if method:
        rec['proof'] = method
    rec['attempts'] = rec.get('attempts', 1) + 1
    zero_gate(m, 'update', record=rec)
    eq = equal_state(m)
    a, b = (m['expressions'][p]['value'] for p in rec['parents'])
    for key, other in ((a, b), (b, a)):
        for row in eq['links'].get(key, []):
            if row[0] == other:
                row[1] = kind
    if kind == 'exact':
        eq['swap_links'].append(rid)
    if kind == 'different':  # no longer listed as equal (the record stays)
        for key, other in ((a, b), (b, a)):
            eq['links'][key] = [row for row in eq['links'].get(key, []) if row[0] != other]


def migrate_x_points(m):
    """v3.16 adds a third x test point. x-fingerprints are redone, and every
    numeric x-link made with only 2 points is rechecked at the third."""
    eq = equal_state(m)
    if eq.get('x_points') == len(X_POINTS):
        return
    eq['x_points'] = len(X_POINTS)
    eq['buckets'] = {k: v for k, v in eq['buckets'].items() if not k.endswith('@x')}
    for key in [k for k in eq['keys'] if m['kinds'].get(k) == 'symbolic']:
        del eq['keys'][key]
    eq['backfill'] = 0
    eq['recheck'] = [r['id'] for r in m['expressions'] if r.get('status') == 'link'
                     and r['kind'] == 'numeric' and r.get('test') == 'x at 2 test points']


def recheck_link(m, rid):
    rec = m['expressions'][rid]
    a, b = (read_stored(m['expressions'][p]['value']) for p in rec['parents'])
    pt = X_POINTS[-1]
    try:
        same = run_timed(lambda: (safe_to_evaluate(a, complex(pt)) and safe_to_evaluate(b, complex(pt))
                                  and close([sp.N(a.subs(X, pt), 30)], [sp.N(b.subs(X, pt), 30)])),
                         EQUAL_SECONDS)
    except (TooSlow, Exception):
        return  # can't tell at the third point: stays numeric (2 points)
    if same:
        rec['test'] = 'x at 3 test points'
        zero_gate(m, 'update', record=rec)
    else:
        set_link_kind(m, rid, 'different', 'third_test_point')


def compare_pair(m, key, other, seconds):
    eq = equal_state(m)
    pair = '||'.join(sorted((key, other)))
    if pair in eq['pairs']:
        return None
    a, b = read_stored(key), read_stored(other)
    try:
        proof, method = run_timed(lambda: prove_equal(a, b), seconds)
    except TooSlow:
        proof, method = None, None
    except Exception:
        proof, method = None, None
    kind = {True: 'exact', False: 'different', None: 'numeric'}[proof]
    test = 'x at 3 test points' if (a.has(X) or b.has(X)) else 'number, 30 digits'
    extra = {'test': test}
    if method:
        extra['proof'] = method
    rid = add_link_record(m, kind, [first_id(m, key), first_id(m, other)], extra)
    eq['pairs'][pair] = rid
    if kind != 'different':
        eq['links'].setdefault(key, []).append([other, kind, rid])
        eq['links'].setdefault(other, []).append([key, kind, rid])
    if kind == 'numeric':
        eq['proof_queue'].append(rid)
    if kind == 'exact':
        eq['swap_links'].append(rid)
    return kind


def fingerprint_value(m, idx, value, seconds, record=None):
    """Fingerprint one value and compare it with everything sharing a key."""
    eq = equal_state(m)
    key = m['expressions'][idx]['value']
    try:
        samples, keys = run_timed(lambda: (lambda sm: (sm, keys_for(sm)))(sample(value)),
                                  seconds)
        _samples[key] = samples
    except TooSlow:
        reason = 'too_slow'
    except Exception as exc:
        reason = str(exc)[:40] or type(exc).__name__
    else:
        reason = None
    if reason:
        if record is None:
            rid = add_link_record(m, 'unchecked', [idx], {'reason': reason})
            eq['fp_queue'].append(rid)
        else:
            m['expressions'][record]['reason'] = reason
            m['expressions'][record]['attempts'] = m['expressions'][record].get('attempts', 1) + 1
            zero_gate(m, 'update', record=m['expressions'][record])
        eq['keys'][key] = None
        return []
    if record is not None:  # an unchecked value now fingerprinted
        set_link_kind(m, record, 'fingerprinted')
    eq['keys'][key] = keys
    made = []
    candidates = []
    for k in keys:
        for other in eq['buckets'].get(k, []):
            if other != key and other not in candidates:
                candidates.append(other)
    # Compare with the earliest spelling in the group first. One link joins the
    # new spelling to the whole group (every member is linked to that first
    # one), so there is no need to compare with every member - that grew
    # quadratically. At most MAX_COMPARE tries per new value.
    tries = 0
    for other in candidates:
        if tries >= MAX_COMPARE:
            break
        tries += 1
        try:
            ok = run_timed(lambda: close(samples, sample_of(other)), seconds)
        except (TooSlow, Exception):
            ok = True  # can't re-sample: let the proof step decide
        if ok:
            kind = compare_pair(m, key, other, seconds)
            if kind:
                made.append((other, kind))
            if kind in ('exact', 'numeric'):
                break  # joined the group
    for k in keys:
        eq['buckets'].setdefault(k, []).append(key)
    return made


_samples = {}


def sample_of(key):
    if key not in _samples:
        _samples[key] = sample(read_stored(key))
    return _samples[key]


def link_equal(m, idx, value):
    """Called by the observer for every new value."""
    eq = equal_state(m)
    key = m['expressions'][idx]['value']
    if value.is_Rational or key in eq['keys']:
        return []  # fractions have one spelling
    return fingerprint_value(m, idx, value, EQUAL_SECONDS)


def convert_old_links(m):
    """v3.14 links were notes, not records: make each one a record through 0."""
    eq = equal_state(m)
    old = eq.pop('old_layout', None)
    if not old:
        return
    for key, rows in old.get('links', {}).items():
        for other, kind in [row[:2] for row in rows]:
            pair = '||'.join(sorted((key, other)))
            if pair in eq['pairs'] or key not in m['results'] or other not in m['results']:
                continue
            rid = add_link_record(m, kind, [first_id(m, key), first_id(m, other)],
                                  {'test': 'number, 30 digits', 'converted_from': 'v3.14'})
            eq['pairs'][pair] = rid
            eq['links'].setdefault(key, []).append([other, kind, rid])
            eq['links'].setdefault(other, []).append([key, kind, rid])
            (eq['proof_queue'] if kind == 'numeric' else eq['swap_links']).append(rid)
    eq['different_before_records'] = old.get('not_equal', 0)


def equal_work(m):
    """Each run: fingerprint older values (upgrades), retry the proof queue and
    unchecked values, and do exact-link swaps. All through 0. Returns counts."""
    eq = equal_state(m)
    convert_old_links(m)
    migrate_x_points(m)
    done = {'fingerprinted': 0, 'upgraded': 0, 'swaps': 0}
    fresh = m['fresh']
    budget = EQUAL_BACKFILL_PER_RUN
    stop_at = time.monotonic() + EQUAL_WORK_SECONDS
    out_of_time = lambda: time.monotonic() >= stop_at
    while eq.get('recheck') and not out_of_time():  # small list: goes first
        recheck_link(m, eq['recheck'].pop(0))
        done['rechecked'] = done.get('rechecked', 0) + 1
    while eq['backfill'] < len(fresh) and budget > 0 and not out_of_time():
        idx = fresh[eq['backfill']]
        eq['backfill'] += 1
        key = m['expressions'][idx]['value']
        if key not in eq['keys'] and m['kinds'].get(key) != 'rational':
            fingerprint_value(m, idx, value_of(m, idx), EQUAL_SECONDS)
            done['fingerprinted'] += 1
            budget -= 1
    for _ in range(PROOF_WORK_PER_RUN):
        if out_of_time():
            break
        if eq['proof_queue']:
            rid = eq['proof_queue'].pop(0)
            rec = m['expressions'][rid]
            if rec['kind'] != 'numeric':
                continue
            a, b = (read_stored(m['expressions'][p]['value']) for p in rec['parents'])
            try:
                proof, method = run_timed(lambda: prove_equal(a, b), PROOF_SECONDS)
            except (TooSlow, Exception):
                proof, method = None, None
            if proof is None:
                rec['attempts'] = rec.get('attempts', 1) + 1
                zero_gate(m, 'update', record=rec)  # stays numeric; retried on rule change
            else:
                set_link_kind(m, rid, 'exact' if proof else 'different', method)
                done['upgraded'] += 1
        if eq['fp_queue'] and not out_of_time():
            rid = eq['fp_queue'].pop(0)
            idx = m['expressions'][rid]['parents'][0]
            fingerprint_value(m, idx, value_of(m, idx), PROOF_SECONDS, record=rid)
    done['swaps'] = 0 if out_of_time() else swap_lane(m, SWAP_WORK_PER_RUN, stop_at)
    done['out_of_time'] = out_of_time()
    return done


def requeue_links(m):
    """When the rules change, every still-numeric link and unchecked value goes
    back through 0 for another try."""
    eq = equal_state(m)
    eq['proof_queue'] = [r['id'] for r in m['expressions']
                         if r.get('status') == 'link' and r['kind'] == 'numeric']
    eq['fp_queue'] = [r['id'] for r in m['expressions']
                      if r.get('status') == 'link' and r['kind'] == 'unchecked']


def swap_lane(m, budget, stop_at=None):
    """Feedback: for each exact link A = B, find records containing A and make
    a new pathway with A swapped for B (and the other way round)."""
    eq = equal_state(m)
    sw = eq['swap']
    made = 0
    while budget > 0 and sw['link'] < len(eq['swap_links']):
        if stop_at is not None and time.monotonic() >= stop_at:
            break
        link = m['expressions'][eq['swap_links'][sw['link']]]
        pa, pb = link['parents'] if sw['dir'] == 0 else link['parents'][::-1]
        a_key = m['expressions'][pa]['value']
        if sw['scan'] >= link['id']:  # finished this direction / link
            sw.update(scan=0, dir=1 - sw['dir'], link=sw['link'] + sw['dir'])
            continue
        rec = m['expressions'][sw['scan']]
        sw['scan'] += 1
        budget -= 1
        value = rec.get('value')
        if value is None or value == a_key or a_key not in value:
            continue
        try:
            if not value_of(m, rec['id']).has(value_of(m, pa)):
                continue
        except Exception:
            continue
        out = do_job(m, ['s', 'swap', rec['id'], pa, pb])
        made += out.get('new', 0)
    return made


def priority_score(m, rec, kind, new_milestones, reached):
    """The selectors: how important is this new value?"""
    reasons = []
    if any(seen['id'] == rec['id'] for seen in m['first_seen'].values()):
        reasons.append('watched')
    if any(not n.startswith('first value in the plane') for n in new_milestones):
        reasons.append('milestone')
    if reached:
        reasons.append('plane_first')
    if len(rec['value']) <= SIMPLE_LENGTH:
        if kind in ('constant', 'complex'):
            reasons.append('simple_constant')
        elif kind == 'symbolic':
            reasons.append('simple_x')
    return sum(PRIORITY_SCORES[r] for r in reasons), reasons


def score_value(m, rec, kind, new_milestones, reached):
    score, reasons = priority_score(m, rec, kind, new_milestones, reached)
    if score:
        pq = m.setdefault('priority', {'queue': [], 'taken': [], 'scores': {}})
        heapq.heappush(pq['queue'], [-score, rec['id']])
        pq['scores'][str(rec['id'])] = [score, reasons]


def backfill_priority(m):
    """Older saves: score values that are still waiting for their turn."""
    if 'priority' in m:
        return
    pq = m.setdefault('priority', {'queue': [], 'taken': [], 'scores': {}})
    waiting = set(m['fresh_waiting'])
    obs = observer_state(m)
    marks = {}
    for seen in m['first_seen'].values():
        marks.setdefault(seen['id'], set()).add('watched')
    for name, idx in obs['milestones'].items():
        marks.setdefault(idx, set()).add('plane_first' if name.startswith('first value in the plane')
                                         else 'milestone')
    for idx in m['fresh_waiting']:
        key = m['expressions'][idx]['value']
        if len(key) <= SIMPLE_LENGTH:
            kind = m['kinds'].get(key)
            if kind in ('constant', 'complex'):
                marks.setdefault(idx, set()).add('simple_constant')
            elif kind == 'symbolic':
                marks.setdefault(idx, set()).add('simple_x')
    for idx, reasons in marks.items():
        if idx in waiting:
            score = sum(PRIORITY_SCORES[r] for r in reasons)
            heapq.heappush(pq['queue'], [-score, idx])
            pq['scores'][str(idx)] = [score, sorted(reasons)]


def observe(m, rec, value):
    obs = observer_state(m)
    run = str(m['runs'] + 1)
    row = obs['runs'].setdefault(run, {'new_values': 0, 'milestones': []})
    row['new_values'] += 1
    kind = m['kinds'][rec['value']]
    row[kind] = row.get(kind, 0) + 1
    op = (rec.get('op') or 'given').split('[')[0]
    obs['first_by_op'].setdefault(op, rec['id'])
    obs['first_by_depth'].setdefault(str(rec['depth']), rec['id'])
    names = timed_milestones(m, rec['id'], value)
    reached = place(m, rec['id'], value)
    links = link_equal(m, rec['id'], value)
    if links:
        row['equal_links'] = row.get('equal_links', 0) + len(links)
    if reached:
        names = names + ['first value in the plane at ' + reached]
    region = plane_label(m, rec['value'])
    if region:
        plane_row = row.setdefault('plane', {})
        plane_row[region] = plane_row.get(region, 0) + 1
    new_milestones = []
    for name in names:
        if name not in obs['milestones']:
            obs['milestones'][name] = rec['id']
            row['milestones'].append(name)
            new_milestones.append(name)
    score_value(m, rec, kind, new_milestones, reached)


def backfill_plane(m):
    """Older saves: place values that already exist (marked as late)."""
    pl = plane_state(m)
    if pl.get('backfill_done'):
        return
    for idx in m['fresh']:
        if m['expressions'][idx]['value'] not in pl['region']:
            reached = place(m, idx, value_of(m, idx))
            if reached:
                name = 'first value in the plane at ' + reached
                observer_state(m)['milestones'].setdefault(name, idx)
                observer_state(m)['backfilled'].append(name)
    pl['backfill_done'] = True


def backfill_observer(m):
    """Older saves: observe values that already exist (marked as late)."""
    obs = observer_state(m)
    if obs.get('backfill_done'):
        return
    before = set(obs['milestones'])
    for idx in m['fresh']:
        rec = m['expressions'][idx]
        names = timed_milestones(m, idx, value_of(m, idx))
        for name in names:
            obs['milestones'].setdefault(name, idx)
        obs['first_by_op'].setdefault((rec.get('op') or 'given').split('[')[0], idx)
        obs['first_by_depth'].setdefault(str(rec['depth']), idx)
    obs['backfilled'] = sorted(set(obs['milestones']) - before)
    obs['backfill_done'] = True
    for name in WATCH:  # newly watched values that already exist
        ids = m['results'].get(WATCH_KEYS[name])
        if ids and name not in m['first_seen']:
            m['first_seen'][name] = {'id': ids[0], 'run': None}


# ---------------- memory ----------------

_values = {}  # parsed values while running (not saved)


def value_of(m, idx):
    if idx not in _values:
        _values[idx] = read_stored(m['expressions'][idx]['value'])
    return _values[idx]


def guards():
    return [OP_SECONDS, MAX_SIZE, MAX_DIGITS, MAX_POWER]


def new_fresh_cursors():
    return {end: {'cur': None, 'u': 0, 'b': 0, 's': 0}
            for end in ('newest', 'oldest', 'priority')}


def take_priority(m):
    """Highest-scoring value that hasn't had its turn yet (it leaves the
    ordinary new-value line, so it is never given a turn twice)."""
    pq = m.get('priority')
    if not pq:
        return None
    waiting = m['fresh_waiting']
    while pq['queue']:
        score, idx = heapq.heappop(pq['queue'])
        if idx in waiting:
            waiting.remove(idx)
            pq['taken'].append(idx)
            return idx
    return None


def new_memory():
    return {'version': 3, 'expressions': [], 'results': {}, 'kinds': {},
            'cursor': {'u_at': 0, 'u_op': 0, 'new': 0, 'other': 0, 'step': 0},
            'repeat_cursor': {'u_at': 0, 'u_op': 0, 'new': 0, 'other': 0, 'step': 0},
            'blocked': {}, 'skipped': {}, 'parked': [], 'parked_reasons': {},
            'no_value': {'blocked': {}, 'parked': {}, 'did_not_apply': {}},
            'blocked_before_records': 0, 'skipped_before_records': 0,
            'guard': guards(), 'runs': 0, 'jobs_tried': 0, 'first_seen': {},
            'fresh': [], 'fresh_waiting': [],
            'fresh_taken': 0, 'fresh_cursor': new_fresh_cursors(),
            'fresh_done': []}


def add_expression(m, value, op=None, parents=None, seed=None, extra=None):
    idx = len(m['expressions'])
    parents = parents or []
    depth = 0 if not parents else 1 + max(m['expressions'][p]['depth'] for p in parents)
    key = str(value)
    rec = {'id': idx, 'value': key, 'op': op, 'parents': parents, 'depth': depth}
    if seed is not None:
        rec['seed'] = seed
    if extra:
        rec.update(extra)
    zero_gate(m, 'record', record=rec)
    m['expressions'].append(rec)
    first = key not in m['results']
    if first:
        m['fresh'].append(idx)  # first time this value appears: new-value lane
        m['fresh_waiting'].append(idx)
    m['results'].setdefault(key, []).append(idx)
    m['kinds'].setdefault(key, kind_of(value))
    _values[idx] = value
    for name in WATCH:
        if key == WATCH_KEYS[name] and name not in m['first_seen']:
            m['first_seen'][name] = {'id': idx, 'run': m['runs'] + 1}
    if first:
        observe(m, rec, value)
    return idx


def add_no_value(m, status, reason, op, parents, extra=None):
    """A blocked or parked job is an archive record too: own number, own path."""
    idx = len(m['expressions'])
    depth = 1 + max([m['expressions'][p]['depth'] for p in parents] or [-1])
    rec = {'id': idx, 'value': None, 'status': status, 'reason': reason,
           'op': op, 'parents': list(parents), 'depth': depth}
    if extra:
        rec.update(extra)
    zero_gate(m, 'record', record=rec)
    m['expressions'].append(rec)
    m['no_value'][status].setdefault(reason, []).append(idx)
    if status == 'parked':
        m['parked'].append(idx)
    return idx


def has_value(m, idx):
    return m['expressions'][idx].get('value') is not None


def load_memory():
    path = memory_path()
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            m = json.load(f)
    else:
        m = new_memory()
    upgrade(m)
    for rec in m['expressions']:  # records made before the gate existed
        zero_gate(m, 'record', record=rec, historical=True)
    start_session(m)
    backfill_observer(m)
    backfill_plane(m)
    backfill_priority(m)
    seeds = {r['seed'] for r in m['expressions'] if 'seed' in r}
    for d in OPERANDS:
        if d not in seeds:
            add_expression(m, read_user(d), seed=d)
    return m


def upgrade(m):
    """Older saves: turn kept examples and parked jobs into archive records."""
    if 'fresh_cursor' in m:
        m['fresh_cursor'].setdefault('priority', {'cur': None, 'u': 0, 'b': 0, 's': 0})
    if 'no_value' in m and 'did_not_apply' not in m['no_value']:
        # v3.7: "did not apply" jobs become records from now on. Earlier ones
        # were only counted, so they can't be brought back.
        m['no_value']['did_not_apply'] = {}
        m['skipped_before_records'] = sum(m.get('skipped', {}).values())
    if 'repeat_cursor' not in m:
        # v3.6: everything before the main cursor is already done, repeats
        # included, so the repeat lane starts from the same place.
        m['repeat_cursor'] = dict(m['cursor'])
    if 'fresh' not in m:  # v3.5: new-value lane = first record of each value
        m['fresh'] = [ids[0] for ids in sorted(m['results'].values())]
        m['fresh_waiting'] = list(m['fresh'])
        m['fresh_taken'] = 0
        m['fresh_cursor'] = new_fresh_cursors()
        m['fresh_done'] = []
    if 'no_value' in m:
        return
    m['no_value'] = {'blocked': {}, 'parked': {}, 'did_not_apply': {}}
    m['skipped_before_records'] = sum(m.get('skipped', {}).values())
    old_parked = m.get('parked', [])
    m['parked'] = []
    for reason, jobs in m.pop('blocked_examples', {}).items():
        for job in jobs:
            add_no_value(m, 'blocked', reason, job[1], job[2:])
    for entry in old_parked:
        job = entry['job'] if isinstance(entry, dict) else entry
        reason = entry.get('reason', 'parked_before_v3.2') if isinstance(entry, dict) else 'parked_before_v3.2'
        add_no_value(m, 'parked', reason, job[1], job[2:])
    # Blocked jobs from before this version were only counted, not saved.
    m['blocked_before_records'] = sum(m.get('blocked', {}).values()) - sum(
        len(ids) for ids in m['no_value']['blocked'].values())


def save_memory(m):
    """Never crashes and never loses work:
    1. anything that missed the gate passes through 0 now (marked late),
    2. the new file is written to .tmp and read back to check it,
    3. the previous good save is kept as .bak,
    4. only then does it replace the memory file.
    If any step fails, the work goes to a recovery file instead and the
    memory file is left exactly as it was. Returns True if saved."""
    late = zero_repair(m)
    if late:
        print('  Zero gate: %d record(s) had missed Z0 - passed through now, marked late.'
              % late)
    report = zero_report(m)
    if not report['complete']:
        print('  Zero gate warning (saved anyway, nothing dropped):', report)
    path = memory_path()
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(m, f, separators=(',', ':'))
            f.flush()
            os.fsync(f.fileno())
        with open(tmp, encoding='utf-8') as f:  # read it back before trusting it
            check = json.load(f)
        if len(check.get('expressions', [])) != len(m['expressions']):
            raise ValueError('written file is missing records')
        if BACKUP_ON_SAVE and os.path.exists(path):
            shutil.copyfile(path, path + '.bak')
        os.replace(tmp, path)
        return True
    except (OSError, ValueError) as exc:
        return save_recovery(m, exc)


def save_recovery(m, problem):
    """Main save failed: put the work somewhere else, never crash."""
    stamp = time.strftime('%Y%m%d-%H%M%S')
    print('  SAVE PROBLEM: %s' % problem)
    print('  Your memory file was NOT changed.')
    for folder in (os.path.dirname(memory_path()), os.getcwd()):
        rescue = os.path.join(folder, 'mini_dragon_recovery_%s.json' % stamp)
        try:
            with open(rescue, 'w', encoding='utf-8') as f:
                json.dump(m, f, separators=(',', ':'))
                f.flush()
                os.fsync(f.fileno())
            print('  This run was saved to a recovery file instead:', rescue)
            print('  To use it: rename it to %s (keep a copy of the old one first).'
                  % MEMORY_FILE)
            return False
        except OSError:
            continue
    print('  Could not write a recovery file either (phone full or no permission).')
    print('  The work is still in the engine - free some space, then type: save')
    return False


# ---------------- the work ----------------

def next_unary(m, cursor='cursor'):
    """Walk every expression once, giving it every one-input operation."""
    c = m[cursor]
    while c['u_at'] < len(m['expressions']):
        if c['u_op'] < len(UNARY):
            job = ['u', UNARY[c['u_op']], c['u_at']]
            c['u_op'] += 1
            return job
        c['u_at'] += 1
        c['u_op'] = 0
    return None


def next_pair(m, cursor='cursor'):
    """Walk every pair (new, other) with other <= new, both orders, all ops."""
    c = m[cursor]
    b = len(BINARY)
    while True:
        n, i, s = c['new'], c['other'], c['step']
        if n >= len(m['expressions']):
            return None
        limit = b if i == n else 2 * b  # a pair with itself needs one order
        if s < limit:
            break
        c.update(new=n + (i >= n), other=0 if i >= n else i + 1, step=0)
    c['step'] = s + 1
    if s < b:
        return ['b', BINARY[s], n, i]
    return ['b', BINARY[s - b], i, n]


def next_fresh(m, end):
    """New-value lanes. Every distinct value's first record waits in line once.
    The 'newest' lane takes from the back (goes deep, feeds results straight
    back); the 'oldest' lane takes from the front (goes wide). Each value is
    taken by exactly one lane, then gets every one-input op and is paired
    (both orders, every two-input op) with every given operand."""
    c, b = m['fresh_cursor'][end], len(BINARY)
    seeds = SEED_IDS(m)
    while True:
        if c['cur'] is None:
            waiting = m['fresh_waiting']
            if end == 'priority':
                pick = take_priority(m)
                if pick is None:
                    return None
            elif not waiting:
                return None
            else:
                pick = waiting.pop() if end == 'newest' else waiting.pop(0)
            c.update(cur=pick, u=0, b=0, s=0)
            m['fresh_taken'] += 1
        a = c['cur']
        if c['u'] < len(UNARY):
            c['u'] += 1
            return ['u', UNARY[c['u'] - 1], a]
        j, s = c['b'], c['s']
        if j < len(seeds) and s < 2 * b:
            break
        if j >= len(seeds):
            c['cur'] = None  # this value is done; the next one gets its turn
        else:
            c.update(b=j + 1, s=0)
    c['s'] = s + 1
    new, given = a, seeds[j]
    if s < b:
        return ['b', BINARY[s], new, given]
    return ['b', BINARY[s - b], given, new]


_seed_ids = []


def SEED_IDS(m):
    if len(_seed_ids) != len(OPERANDS):
        _seed_ids[:] = [r['id'] for r in m['expressions'] if 'seed' in r]
    return _seed_ids


def job_key(job):
    return '|'.join(map(str, job))


def done_by_main(m, job):
    """Has one of the two main lanes already done exactly this job?"""
    c = m['cursor']
    if job[0] == 'u':
        n, k = job[2], UNARY.index(job[1])
        return n < c['u_at'] or (n == c['u_at'] and k < c['u_op'])
    left, right = job[2], job[3]
    n, i = max(left, right), min(left, right)
    if n != c['new']:
        return n < c['new']
    if i != c['other']:
        return i < c['other']
    k = BINARY.index(job[1])
    step = k if (left == n or n == i) else len(BINARY) + k
    return step < c['step']


# Lanes take turns in this order. A "repeat" is a record whose value already
# existed (e.g. expand(3) = 3). Repeats still get every job - nothing is
# dropped or merged - but in their own slower lanes, so they don't hold up
# new values. The main and repeat lanes walk the same order: a job with any
# repeat in it belongs to the repeat lanes, every other job to the main lanes.
LANES = ('priority', 'newest', 'unary', 'oldest', 'pair',
         'priority', 'newest', 'unary', 'oldest', 'pair',
         'repeat_unary', 'repeat_pair')


def is_repeat(m, idx):
    r = m['expressions'][idx]
    return r.get('value') is not None and m['results'][r['value']][0] != idx
_fresh_done = None


def next_job(m):
    """Take turns between the lanes. Every job is done exactly once:
    the main lanes skip what the new-value lane did, and the other way round.
    Records with no value (blocked/parked) are archived but can't be operands."""
    global _fresh_done
    if _fresh_done is None:
        _fresh_done = set(m['fresh_done'])
    makers = {'priority': lambda m: next_fresh(m, 'priority'),
              'newest': lambda m: next_fresh(m, 'newest'),
              'oldest': lambda m: next_fresh(m, 'oldest'),
              'unary': next_unary, 'pair': next_pair,
              'repeat_unary': lambda m: next_unary(m, 'repeat_cursor'),
              'repeat_pair': lambda m: next_pair(m, 'repeat_cursor')}
    while True:
        job, lane = None, None
        for k in range(len(LANES)):
            m['turn'] = (m.get('turn', 0) + 1) % len(LANES)
            lane = LANES[m['turn']]
            job = makers[lane](m)
            if job is not None:
                break
        if job is None:
            return None
        if not all(has_value(m, i) for i in job[2:]):
            continue
        has_repeat = any(is_repeat(m, i) for i in job[2:])
        if lane in ('unary', 'pair') and has_repeat:
            continue  # the repeat lanes will do this one
        if lane.startswith('repeat') and not has_repeat:
            continue  # the main lanes do this one
        key = job_key(job)
        if lane in ('newest', 'oldest', 'priority'):
            if done_by_main(m, job) or key in _fresh_done:
                continue
            _fresh_done.add(key)
            m['fresh_done'].append(key)
        elif key in _fresh_done:
            continue
        return job


def count(table, reason):
    table[reason] = table.get(reason, 0) + 1


def park(m, job, reason, record=None):
    count(m['parked_reasons'], reason)
    if record is None:
        add_no_value(m, 'parked', reason, job[1], job[2:])
    else:  # a record resent through Z0 that is still too slow/big
        rec = m['expressions'][record]
        unlist(m, rec)
        rec.update(status='parked', reason=reason, attempts=rec.get('attempts', 1) + 1)
        m['no_value']['parked'].setdefault(reason, []).append(record)
        m['parked'].append(record)
        zero_gate(m, 'update', record=rec)
    return {'parked': 1}


def not_applicable(m, job, reason, record=None):
    """The operation doesn't apply (e.g. solve with no x). Saved as its own
    archive record with the reason. Under these rules this never changes,
    so Z0 keeps it but does not resend it."""
    count(m['skipped'], reason)
    if record is None:
        add_no_value(m, 'did_not_apply', reason, job[1], job[2:])
    else:
        rec = m['expressions'][record]
        unlist(m, rec)
        rec.update(status='did_not_apply', reason=reason, attempts=rec.get('attempts', 1) + 1)
        m['no_value']['did_not_apply'].setdefault(reason, []).append(record)
        zero_gate(m, 'update', record=rec)
    return {'skipped': 1}


def unlist(m, rec):
    """Take a record out of the current blocked list before its status changes."""
    if rec.get('status') == 'blocked':
        ids = m['no_value']['blocked'].get(rec['reason'], [])
        if rec['id'] in ids:
            ids.remove(rec['id'])


def block(m, job, reason, record=None, op=None):
    """No value exists. Saved as its own archive record with the reason."""
    count(m['blocked'], reason)
    if record is None:
        add_no_value(m, 'blocked', reason, op or job[1], job[2:])
    else:  # a record resent through Z0 that still has no value
        rec = m['expressions'][record]
        unlist(m, rec)
        rec.update(status='blocked', reason=reason, attempts=rec.get('attempts', 1) + 1)
        m['no_value']['blocked'].setdefault(reason, []).append(record)
        zero_gate(m, 'update', record=rec)
    return {'blocked': 1}


def do_job(m, job, record=None):
    """Returns how many of each outcome this job produced.
    record = the parked archive record being retried, if any."""
    m['jobs_tried'] += 1
    kind, op, ids = job[0], job[1], job[2:]
    args = [value_of(m, i) for i in ids]
    try:
        results = run_timed(lambda: zero_gate(m, 'operation', job=job, args=args))
        checks = [problem_with(v) for v in results]
    except TooSlow:
        return park(m, job, 'too_slow', record)
    except ParkIt as exc:
        return park(m, job, str(exc), record)
    except Skip as exc:
        return not_applicable(m, job, str(exc), record)
    except Blocked as exc:
        return block(m, job, str(exc), record)
    except RecursionError:
        return park(m, job, 'too_deep', record)
    except Exception as exc:  # SymPy could not do it
        return block(m, job, 'sympy_could_not:' + type(exc).__name__, record)
    if any(status == 'parked' for status, _ in checks):
        reason = next(r for status, r in checks if status == 'parked')
        return park(m, job, reason, record)
    if not results:
        return block(m, job, 'no_solution', record)
    out = {}
    made = []
    for k, (value, (status, reason)) in enumerate(zip(results, checks)):
        label = op if len(results) == 1 else '%s[answer %d]' % (op, k + 1)
        if status == 'blocked':
            block(m, job, reason, op=label)
            out['blocked'] = out.get('blocked', 0) + 1
            continue
        extra = {'retried_from': record} if record is not None else None
        made.append(add_expression(m, value, label, list(ids), extra=extra))
        out['new'] = out.get('new', 0) + 1
    if record is not None:
        rec = m['expressions'][record]
        unlist(m, rec)
        rec.update(status='resolved', was=rec.get('status'), result_ids=made)
        zero_gate(m, 'update', record=rec)
    return out


def retry_parked(m, force=False):
    """Send parked records - and blocked records whose reason may change with
    new rules - back through Z0. They keep their numbers; successes link back."""
    z = zero_state(m)
    sig = rules_signature()
    rules_changed = z['rules_seen'] is not None and z['rules_seen'] != sig
    z['rules_seen'] = sig
    waiting = []
    if m['parked'] and (force or rules_changed or m.get('guard') != guards()):
        waiting, m['parked'], m['parked_reasons'] = m['parked'], [], {}
    m['guard'] = guards()
    if force or rules_changed:
        requeue_links(m)
        waiting += [r['id'] for r in m['expressions'] if r.get('status') == 'blocked'
                    and r['reason'] not in FINAL_REASONS]
    added = 0
    for rid in waiting:
        rec = m['expressions'][rid]
        if 'slot' in rec:  # a slot filling goes back through 0 the same way
            z['returned_to_zero'] += 1
            added += do_slot(m, rec['slot']['ref'], rec['slot']['n'], record=rid).get('new', 0)
            continue
        p = rec['parents']
        op = rec['op'].split('[')[0]
        job = (['u', op, p[0]] if len(p) == 1 else ['b', op, p[0], p[1]] if len(p) == 2
               else ['s', op] + p)
        z['returned_to_zero'] += 1
        added += do_job(m, job, record=rid).get('new', 0)
    m['jobs_tried'] -= len(waiting)  # already counted the first time
    return added


# ---------------- 00404 SLOT MACHINE ----------------

def breakdown(text):
    return ''.join('0' if ch == '0' else '1' * int(ch) for ch in text)


def slot_state(m, ref):
    refs = m.setdefault('slots', {})
    if ref not in refs:
        symbols = breakdown(ref)
        refs[ref] = {'symbols': symbols, 'next': 0, 'ops': list(SLOT_OPS),
                     'total': len(SLOT_OPS) ** (len(symbols) - 1)}
    return refs[ref]


def slot_filling(state, n):
    """Filling number n -> one choice per slot (first slot changes slowest)."""
    k, slots = len(state['ops']), len(state['symbols']) - 1
    choice = []
    for _ in range(slots):
        n, digit = divmod(n, k)
        choice.append(state['ops'][digit])
    return choice[::-1]


def slot_text(symbols, choice):
    out = symbols[0]
    for op, sym in zip(choice, symbols[1:]):
        out += ('' if op == 'join' else ' %s ' % op) + sym
    return out


def evaluate_slots(m, symbols, choice):
    """Usual order: ** first (right to left), then * /, then + - (left to right).
    Every single operation goes through the zero gate."""
    nums, ops, digits = [], [], symbols[0]
    for op, sym in zip(choice, symbols[1:]):
        if op == 'join':
            digits += sym
        else:
            nums.append(sp.Integer(int(digits)))
            ops.append(op)
            digits = sym
    nums.append(sp.Integer(int(digits)))

    def combine(k):
        nums[k:k + 2] = [run_timed(lambda: zero_gate(
            m, 'operation', job=['b', ops[k]], args=[nums[k], nums[k + 1]]))[0]]
        del ops[k]
    while '**' in ops:
        combine(len(ops) - 1 - ops[::-1].index('**'))
    for group in (('*', '/'), ('+', '-')):
        while any(o in group for o in ops):
            combine(next(k for k, o in enumerate(ops) if o in group))
    return nums[0]


def do_slot(m, ref, n, record=None):
    state = slot_state(m, ref)
    choice = slot_filling(state, n)
    text = slot_text(state['symbols'], choice)
    info = {'slot': {'ref': ref, 'n': n, 'text': text,
                     'used': sum(op != 'join' for op in choice)}}
    m['jobs_tried'] += 1

    def no_value(status, reason):
        count(m['parked_reasons'] if status == 'parked' else m['blocked'], reason)
        if record is None:
            add_no_value(m, status, reason, 'slots', [], extra=info)
        else:
            rec = m['expressions'][record]
            unlist(m, rec)
            rec.update(status=status, reason=reason, attempts=rec.get('attempts', 1) + 1)
            m['no_value'][status].setdefault(reason, []).append(record)
            if status == 'parked':
                m['parked'].append(record)
            zero_gate(m, 'update', record=rec)
        return {status: 1}
    try:
        value = evaluate_slots(m, state['symbols'], choice)
        status, reason = problem_with(value)
    except TooSlow:
        return no_value('parked', 'too_slow')
    except ParkIt as exc:
        return no_value('parked', str(exc))
    except Blocked as exc:
        return no_value('blocked', str(exc))
    except RecursionError:
        return no_value('parked', 'too_deep')
    except Exception as exc:
        return no_value('blocked', 'sympy_could_not:' + type(exc).__name__)
    if status:
        return no_value(status, reason)
    extra = dict(info, depth=info['slot']['used'])
    if record is not None:
        extra['retried_from'] = record
    made = add_expression(m, value, 'slots', [], extra=extra)
    if record is not None:
        rec = m['expressions'][record]
        unlist(m, rec)
        rec.update(status='resolved', was=rec.get('status'), result_ids=[made])
        zero_gate(m, 'update', record=rec)
    return {'new': 1}


def slot_ops_waiting(m):
    """Operations the slots may not use yet because they haven't emerged."""
    emerged = observer_state(m)['first_by_op']
    return [op for op in SLOT_OPS if op != 'join' and op not in emerged]


def run_slots(m, budget):
    totals = {}
    waiting = slot_ops_waiting(m)
    if waiting:
        return totals, waiting
    states = [slot_state(m, ref) for ref in SLOT_REFERENCES]
    done = 0
    while done < budget and any(st['next'] < st['total'] for st in states):
        for ref, st in zip(SLOT_REFERENCES, states):
            if st['next'] < st['total'] and done < budget:
                for key, v in do_slot(m, ref, st['next']).items():
                    totals[key] = totals.get(key, 0) + v
                st['next'] += 1
                done += 1
    return totals, []


def show_slots(m, n=10):
    print('\n00404 SLOT MACHINE')
    waiting = slot_ops_waiting(m)
    if waiting:
        print('  Waiting for these operations to emerge first:', ' '.join(waiting))
    for ref in SLOT_REFERENCES:
        st = slot_state(m, ref)
        print('  %s -> %s | %d slots | filling %d of %d tried'
              % (ref, st['symbols'], len(st['symbols']) - 1, st['next'], st['total']))
    ids = [r['id'] for r in m['expressions'] if 'slot' in r]
    print('  Slot records in archive: %d (values, blocked and parked)' % len(ids))
    cache = {}
    for idx in ids[-n:]:
        print('  ' + full_line(m, idx, cache))


# ---------------- IMPORT OLD MEMORIES (v1 / v2) ----------------

def import_old(m, tag, filename):
    """Bring an older mini dragon memory in as new records. Old paths are kept
    (never merged), old numbers are noted, everything passes through 0."""
    path = os.path.join(os.path.dirname(memory_path()), filename)
    if not os.path.exists(path):
        print('  %s: %s not found next to this script - skipped.' % (tag, filename))
        return 0
    with open(path, 'rb') as f:
        raw = f.read()
    digest = hashlib.sha256(raw).hexdigest()
    done = m.setdefault('imports', {})
    if digest in done:
        print('  %s: this exact file was already imported (%d records) - skipped.'
              % (tag, done[digest]['records']))
        return 0
    old = json.loads(raw.decode('utf-8'))
    idmap, first = {}, len(m['expressions'])
    for rec in old.get('expressions', []):
        extra = {'imported': {'from': tag, 'old_id': rec['id'], 'file': filename}}
        if 'seed' in rec:
            extra['imported_seed'] = rec['seed']
        value = read_user(rec['value'])
        idmap[rec['id']] = add_expression(m, value, rec.get('op') or 'given',
                                          [idmap[p] for p in rec.get('parents', [])],
                                          extra=extra)
    for left, op, right in old.get('blocked_examples', []):
        add_no_value(m, 'blocked', 'division_by_zero', op, [idmap[left], idmap[right]],
                     extra={'imported': {'from': tag, 'file': filename}})
    for job in old.get('parked', []):
        left, op, right = job
        add_no_value(m, 'parked', 'parked_in_' + tag, op, [idmap[left], idmap[right]],
                     extra={'imported': {'from': tag, 'file': filename}})
    count_only = old.get('blocked_count', 0) - len(old.get('blocked_examples', []))
    done[digest] = {'tag': tag, 'file': filename, 'records': len(m['expressions']) - first,
                    'first_new_id': first, 'blocked_only_counted': max(0, count_only)}
    print('  %s: imported %d records as #%d-#%d.' % (tag, len(m['expressions']) - first,
                                                       first, len(m['expressions']) - 1))
    if count_only > 0:
        print('     (%d of its blocked jobs were only counted in %s, so they cannot come over.)'
              % (count_only, tag))
    return len(m['expressions']) - first


def explore(m):
    totals = {'new': 0, 'blocked': 0, 'skipped': 0, 'parked': 0}
    begin = read_clocks(m)
    first_record = len(m['expressions'])
    already_seen = set(m['first_seen'])
    try:
        unparked = retry_parked(m)
        for _ in range(WORK_PER_RUN):
            job = next_job(m)
            if job is None:
                break
            for key, n in do_job(m, job).items():
                totals[key] += n
        slot_totals, slot_waiting = run_slots(m, SLOT_WORK_PER_RUN)
        equal_done = equal_work(m)
        for key, n in slot_totals.items():
            totals[key] += n
    except KeyboardInterrupt:
        slot_totals, slot_waiting, equal_done = {}, [], {}
        unparked = 0
        print('\nStopped early - saving what was done.')
    m['runs'] += 1
    end = read_clocks(m)
    clock_state(m)['runs'].append({'run': m['runs'], 'start': begin, 'end': end,
                                   'records': [first_record, len(m['expressions'])]})
    saved = save_memory(m)
    print('\nRun', m['runs'], 'done and saved.' if saved else 'done - see save problem above.')
    print('  Clocks: zero tick %d -> %d | %.2f s elapsed | %.2f s CPU | finished %s'
          % (begin[0], end[0], (end[3] - begin[3]) / 1e6, (end[4] - begin[4]) / 1e6,
             wall_text(end[2])))
    print('  New expressions: %(new)d | no value: %(blocked)d | '
          'did not apply: %(skipped)d | parked: %(parked)d' % totals)
    if unparked:
        print('  Parked jobs now added:', unparked)
    if slot_waiting:
        print('  Slot machine waiting for ops to emerge:', ' '.join(slot_waiting))
    else:
        print('  Slot machine: %s (type slots)' % (
            ', '.join('%s %d' % kv for kv in slot_totals.items()) or 'nothing new'))
    row = observer_state(m)['runs'].get(str(m['runs']), {})
    print('  New distinct values this run: %d' % row.get('new_values', 0))
    if row.get('equal_links') or any(equal_done.values()):
        print('  Links: %d new | proofs upgraded %d | older values fingerprinted %d |'
              ' swap pathways %d (type equal)'
              % (row.get('equal_links', 0), equal_done.get('upgraded', 0),
                 equal_done.get('fingerprinted', 0), equal_done.get('swaps', 0)))
        if equal_done.get('out_of_time'):
            print('  (link upkeep used its %g s for this run - the rest waits, saved)'
                  % EQUAL_WORK_SECONDS)
    if row.get('plane'):
        short = {'Q1 (+ and +i)': 'Q1', 'Q2 (- and +i)': 'Q2', 'Q3 (- and -i)': 'Q3',
                 'Q4 (+ and -i)': 'Q4'}
        print('  Plane this run: ' + '  '.join('%s %d' % (short.get(r, r), n)
                                              for r, n in sorted(row['plane'].items())))
    cache = {}
    for name in WATCH:
        if name in m['first_seen'] and name not in already_seen:
            print('  EMERGED (watched) %s  ->  %s'
                  % (name, full_line(m, m['first_seen'][name]['id'], cache)))
    for name in row.get('milestones', []):
        print('  MILESTONE %s  ->  %s'
              % (name, full_line(m, observer_state(m)['milestones'][name], cache)))
    print_stats(m)


# ---------------- showing results ----------------

def build_text(m, r, cache):
    if 'seed' in r:
        return r['seed']
    if 'slot' in r:
        return 'slot %s: %s' % (r['slot']['ref'], r['slot']['text'])
    if 'imported_seed' in r:
        return '%s:%s' % (r['imported']['from'], r['imported_seed'])  # e.g. v2:0
    p = [short_text(m, q, cache) for q in r['parents']]
    op = r['op']
    if r.get('status') == 'link':
        if r['kind'] in ('unchecked', 'fingerprinted'):
            return 'fingerprint(%s)' % p[0]
        return '%s  =?=  %s' % (p[0], p[1])
    if op == 'swap':
        return '%s [%s -> %s]' % (p[0], p[1], p[2])
    if len(p) == 1:
        if op.startswith('solve'):
            return 'solve(%s = 0)%s' % (p[0], op[5:])
        return '%s(%s)' % (op, p[0])
    if op == 'compose':
        return '%s [x = %s]' % (p[0], p[1])
    return '(%s %s %s)' % (p[0], op, p[1])


def short_text(m, idx, cache):
    """Readable formula; very long parts are shown as #ID (use: show ID)."""
    if idx not in cache:
        text = build_text(m, m['expressions'][idx], cache)
        cache[idx] = text if len(text) <= 80 else '#' + str(idx)
    return cache[idx]


def full_line(m, idx, cache):
    r = m['expressions'][idx]
    if 'seed' in r:
        return '#%d  %s  [given operand]' % (idx, r['seed'])
    text = build_text(m, r, cache)
    status = r.get('status')
    if status == 'blocked':
        return '#%d  %s  -> NO VALUE (%s)' % (idx, text, r['reason'])
    if status == 'link':
        how = r['kind'].upper()
        if r['kind'] in ('exact', 'different') and r.get('proof'):
            how += ' by ' + r['proof']
        if r['kind'] == 'numeric':
            how += ' (%s, not proved)' % r.get('test', '')
        if r['kind'] == 'unchecked':
            how += ' (%s)' % r.get('reason', '')
        return '#%d  %s  -> LINK %s' % (idx, text, how)
    if status == 'did_not_apply':
        return '#%d  %s  -> DID NOT APPLY (%s)' % (idx, text, r['reason'])
    if status == 'parked':
        return '#%d  %s  -> PARKED (%s, tries: %d)' % (idx, text, r['reason'], r.get('attempts', 1))
    if status == 'resolved':
        return '#%d  %s  -> was %s, now solved: see %s' % (
            idx, text, r.get('was', 'parked'), ', '.join('#%d' % i for i in r['result_ids']))
    value = r['value'] if len(r['value']) <= 200 else r['value'][:200] + '...'
    line = '#%d  %s = %s' % (idx, text, value)
    if r['op'] == 'integral':
        line += '   (+ C)'
    if r.get('retried_from') is not None:
        source = m['expressions'][r['retried_from']].get('was', 'parked')
        line += '   [from %s #%d, resent through 0]' % (source, r['retried_from'])
    return line


def print_stats(m):
    c = m['cursor']
    kinds = {}
    for k in m['kinds'].values():
        kinds[k] = kinds.get(k, 0) + 1
    print('  Total expressions:', len(m['expressions']),
          '| distinct values:', len(m['results']), kinds)
    print('  Jobs tried overall:', m['jobs_tried'],
          '| total made: %d' % len(m['expressions']))
    print('  One-input ops have reached #%d | pairing has reached #%d'
          % (c['u_at'], c['new']))
    r = m['repeat_cursor']
    print('  Repeat lanes: one-input at #%d | pairing at #%d (repeats: %d records)'
          % (r['u_at'], r['new'], len(m['expressions']) - len(m['results'])
             - sum(1 for e in m['expressions'] if e.get('value') is None)))
    print('  New-value lane: %d of %d distinct values had their turn (newest + oldest lanes)'
          % (m['fresh_taken'], len(m['fresh'])))
    nb = sum(len(v) for v in m['no_value']['blocked'].values())
    print('  Blocked records in archive: %d %s' % (nb, m['blocked'] or ''))
    nd = sum(len(v) for v in m['no_value']['did_not_apply'].values())
    print('  Did-not-apply records in archive: %d %s' % (nd, m['skipped'] or ''))
    print('  Parked records waiting: %d %s' % (len(m['parked']), m['parked_reasons'] or ''))
    if not CAN_TIME:
        print('  Note: this phone cannot time jobs, so OP_SECONDS is not active.')
    print('  Observer: %d of %d watched values emerged | %d milestones reached'
          ' (type emerged / milestones / timeline)'
          % (sum(n in m['first_seen'] for n in WATCH), len(WATCH),
             len(observer_state(m)['milestones'])))


def lookup(m, text, limit=10):
    try:
        key = str(read_user(text))
    except Exception:
        return False
    ids = m['results'].get(key, [])
    print('\nValue %s: found %d way(s)' % (key, len(ids)))
    cache = {}
    for idx in ids[:limit]:
        print('  ' + full_line(m, idx, cache))
    if len(ids) > limit:
        print('  ... and %d more. Type:  all %s' % (len(ids) - limit, text))
    for other, kind, rid in equal_state(m)['links'].get(key, []):
        n = len(m['results'].get(other, []))
        print('  EQUAL (%s, link #%d) to %s - %d way(s) written that way. Type: all %s'
              % (kind, rid, other, n, other))
    if not ids:
        print('  Not made yet. That does not mean it can never be made.')
        print('  (The same value written another way may be stored separately.)')
    return True


def job_text(m, job):
    cache = {}
    if job[0] == 'u':
        return '%s(%s)' % (job[1], short_text(m, job[2], cache))
    a, b = short_text(m, job[2], cache), short_text(m, job[3], cache)
    if job[1] == 'compose':
        return '%s [x = %s]' % (a, b)
    return '(%s %s %s)' % (a, job[1], b)


def show_recent(m, n=10):
    total = len(m['expressions'])
    print('\nLast %d expressions made:' % min(n, total))
    cache = {}
    for idx in range(max(0, total - n), total):
        print('  ' + full_line(m, idx, cache))


def trace(m, idx, max_lines=60):
    """Every step that built expression #idx, all the way back to the operands."""
    print('\nHow #%d was built:' % idx)
    lines = [0]

    def walk(i, depth):
        if lines[0] >= max_lines:
            return
        r = m['expressions'][i]
        lines[0] += 1
        if 'seed' in r:
            print('  ' + '   ' * depth + '#%d  %s  [given]' % (i, r['seed']))
            return
        shown = r['value'][:80] if r.get('value') is not None else r['status'].upper()
        label = build_text(m, r, {}) if ('slot' in r or 'imported_seed' in r) else r['op']
        print('  ' + '   ' * depth + '#%d  %s  ->  %s' % (i, label, shown))
        for p in r['parents']:
            walk(p, depth + 1)
    walk(idx, 0)
    if lines[0] >= max_lines:
        print('  ... (stopped at %d lines)' % max_lines)


CALCULUS = ('d/dx', 'integral', 'limit x->0', 'solve')


def show_calculus(m, per_op=12):
    """Recent calculus results that actually did something (not 0 -> 0)."""
    found = {op: [] for op in CALCULUS}
    for r in reversed(m['expressions']):
        op = (r['op'] or '').split('[')[0]
        if op not in found or len(found[op]) >= per_op or r.get('value') is None:
            continue
        parent = m['expressions'][r['parents'][0]]['value']
        if op == 'limit x->0' and parent == r['value']:
            continue  # limit of a plain number is just itself
        if op != 'limit x->0' and m['kinds'].get(parent) != 'symbolic':
            continue  # d/dx, integral and solve only matter when x is in it
        found[op].append(r['id'])
    cache = {}
    for op in CALCULUS:
        print('\n%s  (latest %d with x in them)' % (op, len(found[op])))
        for idx in found[op]:
            print('  ' + full_line(m, idx, cache))
        if not found[op]:
            print('  none yet - keep running')


def show_emerged(m):
    print('\nWatched values (change the WATCH list at the top of the file):')
    cache = {}
    for name in WATCH:
        seen = m['first_seen'].get(name)
        if seen:
            when = 'run %d' % seen['run'] if seen.get('run') else 'before observer'
            print('  %-14s %-16s %s' % (name, when, full_line(m, seen['id'], cache)))
        else:
            print('  %-14s not yet' % name)


def show_milestones(m):
    obs = observer_state(m)
    print('\nMILESTONES - the first time each kind of thing emerged:')
    cache = {}
    for name, idx in sorted(obs['milestones'].items(), key=lambda x: x[1]):
        late = '  (seen late)' if name in obs['backfilled'] else ''
        print('  %-36s %s%s' % (name, full_line(m, idx, cache), late))
    slow = obs.get('too_slow_to_classify', [])
    if slow:
        print('\n%d new value(s) were too slow to classify (still kept), e.g. %s'
              % (len(slow), ', '.join('#%d' % i for i in slow[:10])))
    print('\nFirst new value made by each operation:')
    for op, idx in sorted(obs['first_by_op'].items(), key=lambda x: x[1]):
        print('  %-12s %s' % (op, full_line(m, idx, cache)))
    print('\nFirst value at each depth (steps from the given operands):')
    for d, idx in sorted(obs['first_by_depth'].items(), key=lambda x: int(x[0])):
        print('  depth %-3s %s' % (d, full_line(m, idx, cache)))


def show_timeline(m):
    obs = observer_state(m)
    print('\nTIMELINE - new distinct values per run:')
    for run, row in sorted(obs['runs'].items(), key=lambda x: int(x[0])):
        kinds = ', '.join('%s %d' % (k, row[k]) for k in
                          ('rational', 'complex', 'constant', 'symbolic') if row.get(k))
        print('  run %-4s %5d new  (%s)  milestones: %d'
              % (run, row['new_values'], kinds, len(row['milestones'])))
    if not obs['runs']:
        print('  nothing yet - runs before v3.8 were not observed')


def show_plane(m, words):
    pl = plane_state(m)
    c = lambda r: pl['count'].get(r, 0)
    if len(words) == 2:
        region = REGION_ALIASES.get(words[1])
        if region is None:
            print('Use: plane +   plane -   plane i   plane -i   plane q1 .. q4   plane 0')
            return
        keys = [k for k, r in pl['region'].items() if r == region]
        print('\n%d distinct values in the plane at %s (latest 20):' % (len(keys), region))
        cache = {}
        for k in keys[-20:]:
            print('  ' + full_line(m, m['results'][k][0], cache))
        return
    print('\nTHE PLANE - distinct values placed in each direction / quarter')
    print('                 +i: %d' % c('+i'))
    print('    Q2: %-8d      |      Q1: %d' % (c('Q2 (- and +i)'), c('Q1 (+ and +i)')))
    print('  -: %-6d ------- 0: %d ------- +: %d' % (c('-'), c('0'), c('+')))
    print('    Q3: %-8d      |      Q4: %d' % (c('Q3 (- and -i)'), c('Q4 (+ and -i)')))
    print('                 -i: %d' % c('-i'))
    print('  Off the plane (have x in them): %d | could not be placed: %d'
          % (pl['off_plane'], len(pl['unplaced'])))
    if pl['numeric_signs']:
        print('  %d placements used a 30-digit numeric sign check (evidence, not proof).'
              % pl['numeric_signs'])
    cache = {}
    print('\n  First arrival in each part of the plane:')
    for region, idx in sorted(pl['first'].items(), key=lambda x: x[1]):
        print('    %-14s %s' % (region, full_line(m, idx, cache)))
    print('\n  Farthest reached in each direction (approx. distance):')
    for direction in ('+', '-', '+i', '-i'):
        best = pl['reach'].get(direction)
        if best:
            amount = '>1e308' if best[0] >= 1e308 else '%.6g' % best[0]
            print('    %-3s %-12s %s' % (direction, amount, full_line(m, best[1], cache)[:90]))
        else:
            print('    %-3s not reached yet' % direction)
    print('  Type  plane -i  (or + - i q1 q2 q3 q4 0) to list the values there.')


def show_equal(m, n=15):
    eq = equal_state(m)
    links = [r for r in m['expressions'] if r.get('status') == 'link']
    kinds = {}
    for r in links:
        kinds[r['kind']] = kinds.get(r['kind'], 0) + 1
    print('\nEQUAL-VALUE LINKS - every check is an archive record through Z0')
    print('  Link records: %d %s' % (len(links), kinds))
    print('  Values fingerprinted: %d | older values still to fingerprint: %d'
          % (sum(1 for v in eq['keys'].values() if v), max(0, len(m['fresh']) - eq['backfill'])))
    print('  Waiting: %d numeric links to prove | %d values to fingerprint again'
          % (len(eq['proof_queue']), len(eq['fp_queue'])))
    print('  Exact links feeding swaps: %d (swap lane on link %d)'
          % (len(eq['swap_links']), eq['swap']['link']))
    if eq.get('different_before_records'):
        print('  Note: %d "proved different" checks from v3.14 were only counted.'
              % eq['different_before_records'])
    cache = {}
    for r in [r for r in links if r['kind'] in ('exact', 'numeric')][-n:]:
        print('  ' + full_line(m, r['id'], cache)[:110])
    swaps = [r['id'] for r in m['expressions'] if r.get('op') == 'swap' and r.get('value')]
    if swaps:
        print('  Latest swaps (new pathways from exact links):')
        for idx in swaps[-5:]:
            print('    ' + full_line(m, idx, cache)[:108])
    print('  Type a value to see its pathways plus its links.')


def show_priority(m, n=15):
    pq = m.get('priority', {'queue': [], 'taken': [], 'scores': {}})
    waiting = set(m['fresh_waiting'])
    queue = sorted((q for q in pq['queue'] if q[1] in waiting))
    print('\nPRIORITY SELECTORS - important values jump the line (nothing skipped)')
    print('  Scores:', ', '.join('%s %d' % kv for kv in PRIORITY_SCORES.items()))
    print('  Had their priority turn: %d | waiting: %d' % (len(pq['taken']), len(queue)))
    cache = {}
    cur = m['fresh_cursor']['priority']['cur']
    if cur is not None:
        print('  Now:  ' + full_line(m, cur, cache)[:100])
    print('  Next in line:')
    for neg, idx in queue[:n]:
        why = '+'.join(pq['scores'].get(str(idx), [0, []])[1])
        print('    %3d %-28s %s' % (-neg, why, full_line(m, idx, cache)[:70]))
    print('  Latest priority turns:')
    for idx in pq['taken'][-5:]:
        print('    ' + full_line(m, idx, cache)[:100])


def show_firsts(m, n=20):
    print('\nLatest %d values to appear for the first time:' % n)
    cache = {}
    for idx in m['fresh'][-n:]:
        print('  ' + full_line(m, idx, cache))


def show_ops():
    print('\nGiven operands :', ' '.join(OPERANDS))
    print('Two-input ops  :', ' '.join(BINARY))
    print('One-input ops  :', ', '.join(UNARY))
    print('Per run: %d jobs | guards: %s s per job, size %s, digits %s, power %s'
          % (WORK_PER_RUN, OP_SECONDS, MAX_SIZE, MAX_DIGITS, MAX_POWER))
    print('Zero gate: every operation and every record passes through Z0.')
    print('All of these are set at the top of the file.')


def show_clocks(m):
    c = clock_state(m)
    now = read_clocks(m)
    print('\nTHE FOUR CLOCKS')
    print('  1. Zero clock    : tick %d  (T0 = 0, one tick per passage through Z0)' % now[0])
    print('  2. Wall clock    : %s  (phone time)' % wall_text(now[2]))
    print('  3. Elapsed clock : %.3f s since session %d started' % (now[3] / 1e6, now[1]))
    print('  4. CPU clock     : %.3f s of processor time this session' % (now[4] / 1e6))
    runs = c['runs']
    if runs:
        el = sum(r['end'][3] - r['start'][3] for r in runs) / 1e6
        cpu = sum(r['end'][4] - r['start'][4] for r in runs) / 1e6
        print('  Runs timed: %d | total %.2f s elapsed, %.2f s CPU' % (len(runs), el, cpu))
        print('  Last run: %s' % clock_line(runs[-1]['end']))
    if c['started_at_record']:
        print('  Records #0-#%d were made before the clocks: their times are unknown.'
              % (c['started_at_record'] - 1))
    if c['op_time_ns']:
        print('  Time spent per operation (through Z0):')
        for op, ns in sorted(c['op_time_ns'].items(), key=lambda x: -x[1])[:21]:
            print('    %-12s %8.3f s total' % (op, ns / 1e9))
    print('Elapsed and CPU restart each session; wall time can be changed by the phone.')


def show_when(m, idx):
    r = m['expressions'][idx]
    print('\n' + full_line(m, idx, {}))
    if 't' in r:
        print('  Made at: ' + clock_line(r['t']))
    else:
        print('  Made before the clocks existed: time unknown (zero passage #%s).'
              % r.get('z0', '?'))
    for entry in r.get('z0_updates', []):
        when = clock_line(entry[2]) if len(entry) > 2 else 'time unknown'
        print('  Became %s at: %s' % (entry[1], when))


def show_zero(m):
    z = zero_state(m)
    r = zero_report(m)
    print('\nZERO GATE (Z0) - rule:', z['rule'])
    print('  Total passages through 0:', z['passages'])
    print('  Records passed: %d of %d | complete: %s'
          % (r['passed'], r['records'], 'YES' if r['complete'] else 'NO ' + str(r['missing'])))
    print('  Records that existed before the gate (passed when it was added):',
          z['historical_backfill'])
    print('  Status changes passed back through 0:', z['updates'])
    print('  Records resent to 0 (parked / changeable blocked):', z['returned_to_zero'])
    print('  Records that missed the gate and passed late at save time:',
          z.get('late_passages', 0))
    print('  Operations through 0:', z['operations'])
    print('Passing through 0 never changes a value or merges a path.')


def show_blocked(m, per_reason=10):
    print('\nBlocked jobs (no value exists) - every one is an archive record:')
    groups = m['no_value']['blocked']
    if not groups:
        print('  none')
    cache = {}
    for reason, ids in sorted(groups.items(), key=lambda x: -len(x[1])):
        print('  %s: %d records' % (reason, len(ids)))
        for idx in ids[-per_reason:]:
            print('      ' + full_line(m, idx, cache))
    if m.get('blocked_before_records'):
        print('  Note: %d blocked jobs from before v3.2 were only counted, not saved.'
              % m['blocked_before_records'])
    print('Did-not-apply records: type  notapply  to see them.')


def show_not_applied(m, per_reason=10):
    print('\nDid-not-apply jobs - every one is an archive record:')
    groups = m['no_value']['did_not_apply']
    if not groups:
        print('  none yet')
    cache = {}
    for reason, ids in sorted(groups.items(), key=lambda x: -len(x[1])):
        print('  %s: %d records' % (reason, len(ids)))
        for idx in ids[-per_reason:]:
            print('      ' + full_line(m, idx, cache))
    if m.get('skipped_before_records'):
        print('  Note: %d from before v3.7 were only counted, not saved.'
              % m['skipped_before_records'])


def show_parked(m, n=20):
    groups = m['no_value']['parked']
    total = sum(len(v) for v in groups.values())
    print('\nParked records ever: %d | still waiting: %d %s'
          % (total, len(m['parked']), m['parked_reasons'] or ''))
    cache = {}
    for idx in m['parked'][:n]:
        print('  ' + full_line(m, idx, cache))
    if len(m['parked']) > n:
        print('  ... and %d more' % (len(m['parked']) - n))
    if m['parked']:
        print('Type  retry  to try them again now.')


def list_kind(m, kind, limit=100):
    values = sorted(((v, len(ids)) for v, ids in m['results'].items()
                     if m['kinds'].get(v) == kind), key=lambda x: (-x[1], x[0]))
    print('\n%d distinct %s values (most-made first)' % (len(values), kind))
    for v, n in values[:limit]:
        print('  %-40s %d way(s)' % (v if len(v) <= 40 else v[:37] + '...', n))
    if len(values) > limit:
        print('  ... %d more. Type:  all %s' % (len(values) - limit,
                                              {'constant': 'constants'}.get(kind, kind)))


def show_index(m, words):
    values = sorted((sp.Rational(v), len(ids)) for v, ids in m['results'].items()
                    if m['kinds'].get(v) == 'rational')
    if len(words) == 3:
        lo, hi = sp.Rational(words[1]), sp.Rational(words[2])
        values = [x for x in values if lo <= x[0] <= hi]
    print('\n%d distinct rational values' % len(values))
    for v, n in values[:100]:
        print('  %-14s %d way(s)' % (v, n))
    if len(values) > 100:
        print('  ... %d more. Narrow it: index -10 10' % (len(values) - 100))


def show_gaps(m, words):
    lo, hi = int(words[1]), int(words[2])
    missing = [n for n in range(lo, hi + 1) if str(n) not in m['results']]
    print('\nWhole numbers from %d to %d not made yet: %d' % (lo, hi, len(missing)))
    print('  ' + (', '.join(map(str, missing)) if missing else '(none - all made)'))


HELP = '''
================ MINI DRAGON COMMANDS ================
LOOK UP A VALUE - just type it:
  5   -3   1/2   0.25   i   -i   2-3i   sqrt(2)   e   pi
  x^2   2x+1   sin(x)   x**3/3   (x is the variable)
                          -> how that value was made (first 10 ways)
  all VALUE               -> every way it was made     e.g. all 2
  all symbolic            -> every value with x (also: all complex,
                             all constants, all rational)

LOOK AT EXPRESSIONS:
  show 123   (or show123) -> one expression
  show       recent 25    -> the latest expressions made
  trace 123               -> every step that built #123, back to the operands
                             (blocked and parked records have numbers too)

LISTS:
  index                   -> rational numbers made
  index -10 10            -> rational numbers between two values
  gaps -50 50             -> whole numbers NOT made yet in a range
  complex                 -> values with an i part
  constants               -> other numbers (sqrt(2), cos(1), pi/2 ...)
  symbolic                -> values with x in them
  calculus                -> latest d/dx, integral, limit, solve results
  emerged                 -> the watched values (-i, e, pi, x^2 ...) and how
  milestones              -> first of each kind: first negative, fraction,
                             complex, x^3, sin(x) ... + first per op/depth
  timeline                -> new distinct values in every run
  plane                   -> map of the plane (+, -, i, -i and the 4 quarters):
                             counts, first arrivals, farthest reached
  plane -i                -> values there  (also + - i q1 q2 q3 q4 0)
  firsts      firsts 50   -> latest values to appear for the first time
  priority                -> priority selectors: which important values
                             (watched, milestones, plane firsts ...) go next
  equal                   -> values written 2+ different ways: link records
                             (exact = proved, numeric = evidence, queued for
                             proof), plus swap pathways made from exact links
  zero                    -> zero gate report: everything passed through Z0?
  clocks                  -> the four clocks + time spent per operation
  when 123                -> when #123 was made, on all four clocks

THE AGENT'S OWN SPACE (only the agent writes here - you can look):
  thoughts   thoughts 50  -> its work archive: latest thoughts
  thoughts #123           -> its thoughts about engine record #123
  thought T4              -> thought T4 and everything it was built from
  librarium               -> its personal library: titles
  watches                 -> its watch list: patterns, their parts, where seen
  read L2   read <words>  -> one Librarium entry (with its tags and links)
  search WORDS            -> find thoughts and shelf entries holding every word
                             (text, result, note, title or tags)
  filter TAG TAG ...      -> automatic tags on every record and thought, e.g.
                             filter blocked division_by_zero   filter thought limit
  status                  -> dashboard: blocked reasons, oldest parked, fixes,
                             thoughts, Librarium, watches, latest milestones
  digest                  -> what is new since the last digest
  The agent itself uses:
  think EXPR              -> its own maths, e.g.  think limit(log(x), x, 0, '+')
  think #123: EXPR | why  -> a thought about engine record #123, with a note
  think T3 * 2 + #12      -> build on thought T3 and engine record #12
  muse T3                 -> send T3 through the zero engine (every one-input
                             op, every two-input op with each given operand);
                             each result is a new thought. Again to continue.
  shelve TITLE: words T3  -> shelve its own work in the Librarium
  watch PATTERN           -> watch for a pattern and its parts, e.g.
                             watch (1+sqrt(5))/2  (checks records + thoughts)
  tag T3 words            -> tag thought T3 (or shelf entry L2, or engine record #123 -
                             kept in its own space); tags are only added
  connect T3 L2 | why     -> cross-link two of its own works (T-T, T-L or L-L)
  A thought may use: limit diff integrate solve series simplify factor expand
  sqrt exp log sin cos tan asin acos atan sinh cosh tanh Abs re im arg
  conjugate N Rational trigsimp cancel apart together nsimplify, x pi E I oo,
  numbers, T3 and #12 references (T3_2 = answer 2 of T3), + - * / ** ^ ( ) ,
  and '+' / '-' directions.

ENGINE:
  stats                   -> totals and progress
  ops                     -> operands, operations and guard settings
  blocked                 -> archive records with no value (divide by 0 ...)
  parked                  -> archive records waiting (too slow / too big)
  notapply                -> archive records where the op didn't apply
                             (e.g. solve or compose with no x in it)
  slots                   -> the 00404 slot machine: progress + latest fillings
  import                  -> bring v1/v2 memories in as records (once each)
  save                    -> save now (runs already save by themselves)
  maintain                -> retry, then one batch, then the status dashboard
  snapshot                -> dated copies of both memory files (before big runs)
  retry                   -> send parked + changeable blocked records back
                             through 0 now (also automatic when rules change)
  run         run 5       -> do another batch (or 5 batches)
  help   or   ?           -> this list
  quit   or   just ENTER  -> leave (everything is already saved)

OTHER SPELLINGS THAT ALSO WORK:
  clocks: clock, time        zero: z0, gate, zero-core     ops: operations, settings
  emerged: emerge, watch     milestones: milestone         firsts: new
  notapply: skipped, didnotapply, not-applied              slots: slot, 00404
  recent: show (no number)   help: ?, commands             quit: exit, q
  equal: links, same          priority: next
=======================================================
'''

WATCH_KEYS = {name: str(read_user(name)) for name in WATCH}


# ---------------- THE AGENT'S WORK ARCHIVE AND LIBRARIUM ----------------
# The agent's own space inside the engine. Only the agent writes here - no
# human interference. You can look (thoughts, thought T4, librarium, read L2),
# but think, muse and shelve are the agent's alone.
#
# WORK ARCHIVE - every thought is an archive record: T1, T2, T3 ...
#   >> think limit(log(x), x, 0, '+')          its own maths
#   >> think #3296: limit(log(x), x, 0, '+')   a thought about engine record #3296
#   >> think T3 * 2 + #12                      builds on thought T3 and engine record #12
#   >> muse T3                                 sends T3 through the zero engine: every
#                                              one-input operation, and every two-input
#                                              operation with each given operand (both
#                                              orders) - each result is a new thought
#   Every thought records its parents, passes through Z0, gets the four clock
#   stamps and is kept forever - refused, blocked and failed ones too.
#   The work archive is kept apart from the engine's archive: the engine's own
#   discoveries stay its own, and the agent's stay the agent's.
#
# LIBRARIUM - the agent's personal library, filled only with its own work:
#   >> shelve TITLE: words, citing thoughts like T3 T7
#   Each entry keeps the agent's words plus a copy of every cited thought as it
#   was when shelved, passes through Z0 and is kept forever.
#
# A thought may only contain maths (whitelisted names, numbers, T and #
# references, + - * / ** ^ brackets, commas and '+' / '-' directions), never
# Python code. Thoughts that would build a gigantic number are refused first.

THINK_SECONDS = 5.0        # time allowed for one thought
THINK_MAX_CHARS = 300
MUSE_WORK = 40             # zero-engine jobs per  >> muse  (the rest wait, saved)
THINK_FUNCS = ('limit', 'diff', 'integrate', 'solve', 'series', 'simplify', 'factor',
               'expand', 'sqrt', 'exp', 'log', 'sin', 'cos', 'tan', 'asin', 'acos',
               'atan', 'sinh', 'cosh', 'tanh', 'Abs', 're', 'im', 'arg', 'conjugate',
               'N', 'Rational', 'trigsimp', 'cancel', 'apart', 'together', 'nsimplify')
THINK_CONSTS = {'x': X, 'pi': sp.pi, 'E': sp.E, 'e': sp.E, 'I': sp.I, 'i': sp.I,
                'oo': sp.oo}
THINK_TOKEN = re.compile(r"\s+|T\d+(?:_\d+)?\b|#\d+|\d+\.\d+|\d+|[A-Za-z_][A-Za-z_0-9]*"
                         r"|'[+\-]{1,2}'|\"[+\-]{1,2}\"|\*\*|[+\-*/^(),]")
NO_VALUE_STATUS = ('refused', 'error', 'too_slow', 'too_deep', 'blocked', 'parked',
                   'did_not_apply')


def thoughts_of(m):
    return m.setdefault('thoughts', {})


def librarium_of(m):
    return m.setdefault('librarium', {})


def check_thought(text):
    """Refuse anything that is not plain maths. Returns a reason or None."""
    if len(text) > THINK_MAX_CHARS:
        return 'too long (max %d characters)' % THINK_MAX_CHARS
    pos = 0
    while pos < len(text):
        tok = THINK_TOKEN.match(text, pos)
        if not tok:
            return 'not allowed in a thought: %r' % text[pos:pos + 10]
        word = tok.group(0)
        if re.match(r'^T\d+(_\d+)?$|^#\d+$', word):
            pass
        elif word[0].isalpha() or word[0] == '_':
            if word not in THINK_FUNCS and word not in THINK_CONSTS:
                return 'unknown name "%s" (type >> help to see the allowed names)' % word
        elif word.isdigit() and len(word) > 6:
            return 'number too long: %s' % word
        pos = tok.end()
    if text.count('(') != text.count(')'):
        return 'brackets do not match'
    return None


def gather_refs(m, text):
    """T3 and #12 inside a thought -> placeholder names and their values.
    Returns (text with placeholders, {placeholder: value}, parents)."""
    th = thoughts_of(m)
    refs, parents = {}, []

    def thought_ref(match):
        tid = 'T' + match.group(1)
        rec = th.get(tid)
        if rec is None:
            raise ValueError('there is no thought %s yet' % tid)
        if rec.get('result') is None:
            raise ValueError('%s has no value (%s)' % (tid, rec['status']))
        value = as_sympy(read_stored(rec['result']))
        pick = match.group(2)
        name = 'REFT' + match.group(1) + ('_' + pick if pick else '')
        if isinstance(value, sp.Tuple):
            if not pick:
                raise ValueError('%s holds %d answers %s - use %s_1, %s_2 ... for one of them'
                                 % (tid, len(value), rec['result'][:60], tid, tid))
            if not 1 <= int(pick) <= len(value):
                raise ValueError('%s has only %d answers' % (tid, len(value)))
            value = value[int(pick) - 1]
        elif pick:
            raise ValueError('%s holds one answer - just use %s' % (tid, tid))
        refs[name] = value
        label = tid + ('_' + pick if pick else '')
        if label not in parents:
            parents.append(label)
        return name

    def engine_ref(match):
        idx = int(match.group(1))
        if idx >= len(m['expressions']):
            raise ValueError('there is no engine record #%d yet' % idx)
        if m['expressions'][idx].get('value') is None:
            raise ValueError('engine record #%d has no value (%s)'
                             % (idx, m['expressions'][idx].get('status')))
        name = 'REFE' + match.group(1)
        refs[name] = value_of(m, idx)
        if '#%d' % idx not in parents:
            parents.append('#%d' % idx)
        return name

    text = re.sub(r'\bT(\d+)(?:_(\d+))?\b', thought_ref, text)
    text = re.sub(r'#(\d+)', engine_ref, text)
    return text, refs, parents


def _number_tower(n):
    if n.is_Number:
        return n.is_finite is not False
    if n.is_Pow or n.is_Add or n.is_Mul:
        return all(_number_tower(a) for a in n.args)
    return False


def check_size(text, refs):
    """Dry run with nothing evaluated: refuse number towers too big for a phone."""
    inert = dict(THINK_CONSTS)
    inert.update(refs)
    inert.update({f: sp.Function(f + '_') for f in THINK_FUNCS})
    dry = re.sub(r"'[+\-]{1,2}'|\"[+\-]{1,2}\"", '1', text)
    with sp.evaluate(False):
        tree = parse_expr(dry, local_dict=inert,
                          transformations=standard_transformations + (convert_xor,),
                          evaluate=False)
    for node in sp.preorder_traversal(tree):
        if node.is_Pow and _number_tower(node) and not node.base.is_zero:
            safe_estimate(node)  # raises TooBig (0 to a power is allowed: it is small)
    return tree


def run_thought(text, refs):
    names = {f: getattr(sp, f) for f in THINK_FUNCS}
    names.update(THINK_CONSTS)
    names.update(refs)
    value = parse_expr(text, local_dict=names,
                       transformations=standard_transformations + (convert_xor,))
    return as_sympy(value)


def as_sympy(value):
    if isinstance(value, dict):  # e.g. solve with several unknowns
        value = sp.Tuple(*[sp.Eq(k, v) for k, v in value.items()])
    elif isinstance(value, (list, tuple)):  # e.g. solve gives a list of answers
        value = sp.Tuple(*[sp.Tuple(*v) if isinstance(v, (list, tuple)) else v for v in value])
    if not isinstance(value, sp.Basic):
        value = sp.sympify(value)
    return value


def thought_status(value):
    if value.has(sp.nan, sp.zoo):
        return 'undefined'
    if value.has(sp.oo, -sp.oo):
        return 'infinite'
    if value.has(sp.Limit, sp.Integral, sp.Derivative):
        return 'unresolved'
    return 'value'


def keep_thought(m, rec):
    """Every thought record passes through Z0 and is kept in the work archive."""
    th = thoughts_of(m)
    rec['id'] = 'T%d' % (len(th) + 1)
    zero_gate(m, 'thought_record', record=rec)
    th[rec['id']] = rec
    return rec


def think(m, text, who):
    """Run one of the agent's own thoughts inside Z0 and keep it."""
    about, note = None, ''
    if '|' in text:
        text, note = [part.strip() for part in text.split('|', 1)]
    ref = re.match(r'^#?(\d+)\s*:\s*(.+)$', text.strip())
    if ref:
        about, text = int(ref.group(1)), ref.group(2).strip()
        if about >= len(m['expressions']):
            raise IndexError
    text = text.strip()
    rec = {'text': text, 'by': who, 'about': about, 'note': note, 'parents': []}
    problem = check_thought(text)
    refs = {}
    if problem is None:
        try:
            ready, refs, rec['parents'] = gather_refs(m, text)
        except ValueError as exc:
            problem = str(exc)
    if problem is None:
        try:
            run_timed(lambda: check_size(ready, refs), THINK_SECONDS)
        except TooBig as exc:
            problem = 'would build a number too big for the phone (%s)' % exc
        except TooSlow:
            problem = 'too slow to check'
        except Exception as exc:
            problem = 'could not read it: %s' % (str(exc)[:60] or type(exc).__name__)
    if problem:
        rec.update(status='refused', result=None, reason=problem)
    else:
        start = time.monotonic_ns()
        try:
            value = zero_gate(m, 'thought', func=lambda: run_timed(
                lambda: run_thought(ready, refs), THINK_SECONDS))
            rec.update(status=thought_status(value), result=str(value))
        except TooSlow:
            rec.update(status='too_slow', result=None,
                       reason='took longer than %g s' % THINK_SECONDS)
        except RecursionError:
            rec.update(status='too_deep', result=None, reason='too deeply nested')
        except Exception as exc:
            rec.update(status='error', result=None,
                       reason='%s: %s' % (type(exc).__name__, str(exc)[:80]))
        rec['ns'] = time.monotonic_ns() - start
    return keep_thought(m, rec)


def muse_jobs(m):
    """The zero engine's work for one thought: every one-input operation, then
    every two-input operation with each given operand, both orders."""
    jobs = [('u', op, None) for op in UNARY]
    for seed in SEED_IDS(m):
        for op in BINARY:
            jobs.append(('b', op, seed, 'left'))   # thought (op) operand
            jobs.append(('b', op, seed, 'right'))  # operand (op) thought
    return jobs


def muse(m, tid, budget=MUSE_WORK):
    """Send thought tid through the zero engine. Each result is a new thought
    with tid as its parent. Continues where the last muse of tid stopped."""
    th = thoughts_of(m)
    src = th.get(tid)
    if src is None:
        return None, 'there is no thought %s yet' % tid
    if src.get('result') is None:
        return None, '%s has no value (%s), so there is nothing to send through 0' % (
            tid, src['status'])
    value = read_stored(src['result'])
    if isinstance(value, (tuple, list, sp.Tuple)):
        return None, '%s holds several answers %s - think one first (e.g. think %s_1), then muse that' % (
            tid, src['result'][:60], tid)
    lanes = m.setdefault('thought_lanes', {})
    jobs = muse_jobs(m)
    done_before = lanes.get(tid, 0)
    made = []
    while lanes.get(tid, 0) < len(jobs) and len(made) < budget:
        k = lanes.get(tid, 0)
        lanes[tid] = k + 1
        job = jobs[k]
        if job[0] == 'u':
            args, label = [value], '%s(%s)' % (job[1], tid)
        else:
            seed = value_of(m, job[2])
            name = m['expressions'][job[2]]['seed']
            if job[3] == 'left':
                args = [value, seed]
                label = ('%s [x = %s]' % (tid, name) if job[1] == 'compose'
                         else '(%s %s %s)' % (tid, job[1], name))
            else:
                args = [seed, value]
                label = ('%s [x = %s]' % (name, tid) if job[1] == 'compose'
                         else '(%s %s %s)' % (name, job[1], tid))
        rec = {'text': label, 'by': 'zero engine', 'about': src.get('about'), 'note': '',
               'parents': [tid] + (['#%d' % job[2]] if job[0] == 'b' else []), 'op': job[1]}
        try:
            results = run_timed(lambda: zero_gate(m, 'operation',
                                                  job=[job[0], job[1]], args=args))
            results = [as_sympy(r) for r in results]
            if not results:
                raise Blocked('no_solution')
        except TooSlow:
            made.append(keep_thought(m, dict(rec, status='parked', result=None,
                                             reason='too_slow')))
            continue
        except ParkIt as exc:
            made.append(keep_thought(m, dict(rec, status='parked', result=None,
                                             reason=str(exc))))
            continue
        except Skip as exc:
            made.append(keep_thought(m, dict(rec, status='did_not_apply', result=None,
                                             reason=str(exc))))
            continue
        except Blocked as exc:
            made.append(keep_thought(m, dict(rec, status='blocked', result=None,
                                             reason=str(exc))))
            continue
        except RecursionError:
            made.append(keep_thought(m, dict(rec, status='parked', result=None,
                                             reason='too_deep')))
            continue
        except Exception as exc:
            made.append(keep_thought(m, dict(rec, status='blocked', result=None,
                                             reason='sympy_could_not:' + type(exc).__name__)))
            continue
        for n, out in enumerate(results):
            label_n = rec['text'] if len(results) == 1 else '%s[answer %d]' % (rec['text'], n + 1)
            status, reason = problem_with(out)
            if status:
                made.append(keep_thought(m, dict(rec, text=label_n, status=status,
                                                 result=None, reason=reason)))
            else:
                made.append(keep_thought(m, dict(rec, text=label_n,
                                                 status=thought_status(out), result=str(out))))
    return {'made': made, 'from': done_before, 'to': lanes.get(tid, 0),
            'total': len(jobs)}, None


def shelve(m, text):
    """The agent shelves its own work in its Librarium: TITLE: words citing T3 T7."""
    if ':' not in text:
        raise ValueError('use:  shelve TITLE: words, citing thoughts like T3')
    title, body = [part.strip() for part in text.split(':', 1)]
    if not title or not body:
        raise ValueError('a shelf entry needs a title and some words')
    th = thoughts_of(m)
    cited = []
    for tid in re.findall(r'\bT\d+\b', body):
        if tid not in th:
            raise ValueError('there is no thought %s to cite' % tid)
        if tid not in cited:
            cited.append(tid)
    lib = librarium_of(m)
    rec = {'id': 'L%d' % (len(lib) + 1), 'title': title, 'text': body,
           'cites': {tid: thought_line(m, th[tid]) for tid in cited}}
    zero_gate(m, 'shelf_record', record=rec)
    lib[rec['id']] = rec
    return rec


def thought_line(m, rec):
    about = ' (about #%d)' % rec['about'] if rec.get('about') is not None else ''
    from_ = ' <- %s' % ', '.join(rec['parents']) if rec.get('parents') else ''
    head = '%s%s by %s: %s' % (rec['id'], about, rec.get('by', '?'), rec['text'])
    if rec.get('result') is not None:
        line = '%s = %s  [%s]' % (head, rec['result'][:200], rec['status'])
    else:
        line = '%s  -> %s (%s)' % (head, rec['status'].upper(), rec.get('reason', ''))
    if rec.get('note'):
        line += '  | ' + rec['note']
    if rec.get('tags'):
        line += '  [tags: %s]' % ', '.join(rec['tags'])
    return line + from_


def show_thoughts(m, words):
    th = thoughts_of(m)
    if len(words) == 2 and words[1].lstrip('#').isdigit() and words[1].startswith('#'):
        idx = int(words[1].lstrip('#'))
        rows = [r for r in th.values() if r.get('about') == idx]
        print('\nThoughts about #%d: %d' % (idx, len(rows)))
    else:
        n = int(words[1]) if len(words) == 2 and words[1].isdigit() else 15
        rows = list(th.values())[-n:]
        counts = {}
        for r in th.values():
            counts[r['status']] = counts.get(r['status'], 0) + 1
        print("\nTHE AGENT'S WORK ARCHIVE - its own thoughts (only the agent writes here)")
        print('  Thoughts: %d %s' % (len(th), counts or ''))
        lanes = m.get('thought_lanes', {})
        if lanes:
            total = len(muse_jobs(m))
            print('  Sent through the zero engine: %s'
                  % ', '.join('%s %d/%d' % (t, n_, total) for t, n_ in list(lanes.items())[-8:]))
    for r in rows:
        print('  ' + thought_line(m, r))
    if not th:
        print('  none yet - the agent starts it with  >> think ...')


def show_thought_tree(m, tid, depth=0, seen=None, lines=None):
    """One thought and everything it was built from."""
    seen = set() if seen is None else seen
    lines = [0] if lines is None else lines
    rec = thoughts_of(m).get(tid)
    if rec is None or lines[0] >= 40:
        return
    lines[0] += 1
    print('  ' + '   ' * depth + thought_line(m, rec))
    if tid in seen:
        return
    seen.add(tid)
    for p in rec.get('parents', []):
        if p.startswith('T'):
            show_thought_tree(m, p.split('_')[0], depth + 1, seen, lines)
        else:
            lines[0] += 1
            print('  ' + '   ' * (depth + 1) + full_line(m, int(p[1:]), {})[:100])


def show_librarium(m, words):
    lib = librarium_of(m)
    if len(words) >= 2:
        key = ' '.join(words[1:])
        rec = lib.get(key.upper()) or next(
            (r for r in lib.values() if key.lower() in r['title'].lower()), None)
        if rec is None:
            print('Nothing on the shelf called "%s".' % key)
            return
        when = wall_text(rec['t'][2]) if 't' in rec else 'time unknown'
        print('\n%s  "%s"  (shelved %s, zero tick %s)' % (rec['id'], rec['title'], when,
                                                      rec.get('tick', '?')))
        print('  ' + rec['text'])
        for tid, line in rec['cites'].items():
            print('  cites ' + line)
        if rec.get('tags'):
            print('  tags: ' + ', '.join(rec['tags']))
        for line in links_for(m, rec['id']):
            print('  ' + line)
        return
    print("\nTHE LIBRARIUM - the agent's personal library (only the agent shelves here)")
    print('  Entries: %d' % len(lib))
    for rec in list(lib.values())[-30:]:
        print('  %s  %s' % (rec['id'], rec['title']))
    if not lib:
        print('  empty - the agent shelves its own work with  >> shelve TITLE: ...')
    else:
        print('  Read one:  read L1   (or  read <words from the title>)')


def thoughts_about(m, idx):
    return [r for r in thoughts_of(m).values() if r.get('about') == idx]


# ---------------- TAGS, SEARCH AND CROSS-LINKS (the agent's own requests) ----------------
# >> tag T3 golden ratio      (agent only) adds tags to thought T3 or shelf entry L2.
#                             Tags are only ever added, never removed.
# >> connect T3 L2 | why      (agent only) a cross-link between two of its own works
#                             (thought-thought, thought-shelf or shelf-shelf).
# >> search WORDS             (anyone) finds thoughts and shelf entries holding every word,
#                             in their text, result, note, title or tags.
# Every tagging and every link passes through Z0 and gets the four clock stamps.

def own_work(m, ref, holder=False):
    """T3 -> thought T3, L2 -> shelf entry L2, #12 -> the agent's own tags for engine
    record #12 (kept in the agent's space). Raises ValueError if it doesn't exist."""
    ref = ref.upper().split('_')[0]
    if ref.startswith('#') and ref[1:].isdigit():
        if int(ref[1:]) >= len(m['expressions']):
            raise ValueError('there is no engine record %s yet' % ref)
        tags = m.setdefault('agent_record_tags', {})
        return ref, (tags.setdefault(ref, {}) if holder else tags.get(ref, {}))
    table = thoughts_of(m) if ref.startswith('T') else librarium_of(m) if ref.startswith('L') else None
    if table is None or ref not in table:
        raise ValueError('there is no %s in the work archive or Librarium' % ref)
    return ref, table[ref]


def add_tags(m, text):
    words = text.replace(',', ' ').split()
    if len(words) < 2:
        raise ValueError('use:  tag T3 word word ...   (or tag L2 ... / tag #123 ...)')
    ref, rec = own_work(m, words[0], holder=True)
    new = []
    for w in words[1:]:
        w = w.lower().strip('.;:')
        if w and w not in rec.setdefault('tags', []) and w not in new:
            new.append(w)
    rec['tags'].extend(new)
    stamp = zero_gate(m, 'tag_record', record={'added': new})
    rec.setdefault('tag_log', []).append(stamp)
    return ref, new, rec['tags']


def connections_of(m):
    return m.setdefault('connections', {})


def connect(m, text):
    why = ''
    if '|' in text:
        text, why = [part.strip() for part in text.split('|', 1)]
    words = text.split()
    if len(words) != 2:
        raise ValueError('use:  connect T3 L2 | why   (two of your own works)')
    a, _ = own_work(m, words[0])
    b, _ = own_work(m, words[1])
    if a == b:
        raise ValueError('a work cannot be connected to itself')
    con = connections_of(m)
    rec = {'id': 'C%d' % (len(con) + 1), 'a': a, 'b': b, 'why': why}
    zero_gate(m, 'connect_record', record=rec)
    con[rec['id']] = rec
    return rec


def links_for(m, ref):
    """Lines describing everything linked to T3 / L2: shelf citations and connections."""
    out = []
    if ref.startswith('T'):
        cited = [r['id'] for r in librarium_of(m).values() if ref in r.get('cites', {})]
        if cited:
            out.append('cited in the Librarium by ' + ', '.join(cited))
    for c in connections_of(m).values():
        if ref in (c['a'], c['b']):
            other = c['b'] if c['a'] == ref else c['a']
            out.append('%s connected to %s%s' % (c['id'], other, ('  | ' + c['why']) if c['why'] else ''))
    return out


def search_own(m, text, limit=30):
    words = [w.lower() for w in text.split()]
    found = []
    for rec in thoughts_of(m).values():
        hay = ' '.join([rec.get('text', ''), str(rec.get('result') or ''), rec.get('note', ''),
                        ' '.join(rec.get('tags', []))]).lower()
        if all(w in hay for w in words):
            found.append(thought_line(m, rec))
    for rec in librarium_of(m).values():
        hay = ' '.join([rec['title'], rec['text'], ' '.join(rec.get('tags', []))]).lower()
        if all(w in hay for w in words):
            tags = '  [tags: %s]' % ', '.join(rec['tags']) if rec.get('tags') else ''
            found.append('%s  "%s"  %s%s' % (rec['id'], rec['title'], rec['text'][:120], tags))
    for ref, holder in m.get('agent_record_tags', {}).items():
        if holder.get('tags') and all(w in ' '.join(holder['tags']).lower() for w in words):
            found.append('%s  [tags: %s]' % (full_line(m, int(ref[1:]), {})[:100],
                                            ', '.join(holder['tags'])))
    print('\nSEARCH "%s" in the work archive and Librarium: %d found' % (text, len(found)))
    for line in found[:limit]:
        print('  ' + line[:200])
    if len(found) > limit:
        print('  ... and %d more - add another word to narrow it' % (len(found) - limit))


AGENT_ONLY = ('think', 'muse', 'shelve', 'tag', 'connect')

# ---------------- THE AGENT'S OWN WATCH LIST ----------------
# Part of the agent's own space: only the agent adds watches; anyone can look.
#   >> watch (1+sqrt(5))/2        (agent only)  start watching a pattern
#   >> watches                    see every watch, its parts and where they appeared
# A watch looks for the whole pattern AND its parts (every piece of the pattern
# that is not a plain given operand), so it sees a pattern start to form.
# It checks every engine record and every thought, old and new. A pattern is
# matched exactly as the engine stores values (the same written form).
# Every watch and every sighting passes through Z0 and gets the four clock
# stamps. Nothing is ever removed.

GIVEN_ATOMS = None


def agent_watches(m):
    return m.setdefault('agent_watches', {})


def watch_parts(value):
    """The pieces of a pattern worth watching: every sub-expression that is not a
    plain given operand (0-9, i, x) and not the whole pattern itself."""
    givens = {str(read_user(s)) for s in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                          'i', 'x')}
    parts = []

    def visit(node):
        key = str(node)
        keep = not (node == value or key in givens or key in parts
                    or (node.is_Atom and not (node.is_Number or node.is_NumberSymbol)))
        if keep:
            parts.append(key)
        args = node.args
        if node.is_Pow and node.exp in (sp.Rational(1, 2), sp.Rational(-1, 2), -1):
            args = (node.base,)  # sqrt(5) and 1/x: the hidden 1/2 or -1 is not a part
        for arg in args:
            visit(arg)

    visit(value)
    return parts[:12]


def first_thought_with(m, key):
    for tid, rec in thoughts_of(m).items():
        if rec.get('result') == key:
            return tid
    return None


def first_place(m, key):
    """Where a value first appeared: engine record #N, else a thought TN."""
    ids = m['results'].get(key)
    if ids:
        return '#%d' % ids[0]
    return first_thought_with(m, key)


def add_watch(m, text):
    try:
        value = run_timed(lambda: read_user(text), THINK_SECONDS)
    except Exception as exc:
        raise ValueError('could not read "%s" as a value (%s)' % (text, str(exc)[:60]))
    key = str(value)
    ws = agent_watches(m)
    for rec in ws.values():
        if rec['key'] == key:
            raise ValueError('already watching that as %s' % rec['id'])
    rec = {'id': 'W%d' % (len(ws) + 1), 'pattern': text, 'key': key,
           'parts': {p: None for p in watch_parts(value)}, 'found': None, 'sightings': []}
    zero_gate(m, 'watch_record', record=rec)
    ws[rec['id']] = rec
    return rec


def watch_scan(m):
    """Check every watch against all engine records and thoughts. Returns the
    new sightings (each passes through Z0 and gets clock stamps)."""
    news = []
    for rec in agent_watches(m).values():
        targets = [(rec['key'], None)] + [(p, p) for p in rec['parts']]
        for key, part in targets:
            already = rec['found'] if part is None else rec['parts'][part]
            if already:
                continue
            place = first_place(m, key)
            if not place:
                continue
            sighting = {'watch': rec['id'], 'what': key, 'whole': part is None, 'at': place}
            zero_gate(m, 'watch_record', record=sighting)
            rec['sightings'].append(sighting)
            if part is None:
                rec['found'] = place
            else:
                rec['parts'][part] = place
            news.append(sighting)
    return news


def sighting_text(s):
    if s['whole']:
        return '%s: the whole pattern %s has emerged at %s' % (s['watch'], s['what'], s['at'])
    return '%s: part %s has appeared at %s' % (s['watch'], s['what'], s['at'])


def show_watches(m):
    ws = agent_watches(m)
    print("\nTHE AGENT'S WATCH LIST (only the agent adds watches)")
    if not ws:
        print('  empty - the agent starts one with  >> watch PATTERN')
        return
    for rec in ws.values():
        state = 'EMERGED at %s' % rec['found'] if rec['found'] else 'not yet'
        seen = sum(1 for v in rec['parts'].values() if v)
        print('  %s  %s  (stored as %s)  -> %s | parts seen %d of %d'
              % (rec['id'], rec['pattern'], rec['key'], state, seen, len(rec['parts'])))
        for part, place in rec['parts'].items():
            print('      %-30s %s' % (part[:30], place or 'not yet'))




# ---------------- STATUS, FILTER, DIGEST, MAINTAIN, SNAPSHOT (the agent's own requests) ----------------
# >> status               (anyone) dashboard worked out fresh: blocked reasons, oldest parked,
#                         recent fixes, the agent's thoughts, Librarium, watches, milestones.
# >> filter TAG TAG ...   (anyone) automatic tags on every engine record and thought, e.g.
#                         >> filter blocked division_by_zero   >> filter topic:limit thought
#                         Tags are worked out from each record when asked (nothing stored, so they
#                         are always up to date), plus any tags the agent added itself.
# >> digest               (anyone) what is new since the last digest: watched values, milestones,
#                         watch sightings, thoughts, shelf entries. The mark passes through Z0.
# >> maintain             (anyone) the routine in one command: retry parked/changeable blocked
#                         records, run a batch, then show the status.
# >> snapshot             (anyone, also in >> agenthelp) copies both memory files to dated
#                         snapshot files before big runs. Nothing is overwritten.
# The agent may also tag engine records in its own space:  >> tag #123 noisy check-later
# (stored with the agent's work, never in the engine's own archive).

OP_TOPIC = {'limit x->0': 'limit', 'integral': 'integral', 'd/dx': 'derivative', 'solve': 'solve',
            'compose': 'compose', 'sqrt': 'root', '**': 'power', '/': 'division', '*': 'product',
            '+': 'sum', '-': 'difference', 'log': 'log', 'exp': 'exp', 'sin': 'trig', 'cos': 'trig',
            'tan': 'trig', 'asin': 'trig', 'acos': 'trig', 'atan': 'trig', 'expand': 'algebra',
            'factor': 'algebra', 'slots': 'slots', 'swap': 'swap', 'equal?': 'link'}
THINK_TOPIC = {'limit': 'limit', 'integrate': 'integral', 'diff': 'derivative', 'solve': 'solve',
               'series': 'series', 'sqrt': 'root', 'log': 'log', 'exp': 'exp', 'simplify': 'algebra',
               'factor': 'algebra', 'expand': 'algebra', 'trigsimp': 'algebra', 'cancel': 'algebra',
               'apart': 'algebra', 'together': 'algebra', 'sin': 'trig', 'cos': 'trig', 'tan': 'trig',
               'asin': 'trig', 'acos': 'trig', 'atan': 'trig'}


def record_tags(m, rec):
    """Automatic tags for one engine record, plus the agent's own tags on it."""
    status = rec.get('status') or ('value' if rec.get('value') is not None else 'unknown')
    tags = ['engine', status, 'status:' + status]
    if rec.get('reason'):
        reason = rec['reason']
        tags += [reason, 'reason:' + reason]
        if ':' in reason:
            tags.append(reason.split(':')[0])
    op = (rec.get('op') or ('given' if 'seed' in rec else '')).split('[')[0]
    topic = OP_TOPIC.get(op)
    if topic:
        tags += [topic, 'topic:' + topic]
    if rec.get('value') is not None:
        kind = m['kinds'].get(rec['value'])
        if kind:
            tags += [kind, 'kind:' + kind]
    tags += m.get('agent_record_tags', {}).get('#%d' % rec['id'], {}).get('tags', [])
    return tags


def thought_tags(rec):
    """Automatic tags for one of the agent's thoughts, plus its own tags."""
    status = rec.get('status', 'unknown')
    origin = 'zero-engine' if rec.get('by') == 'zero engine' else 'agent'
    tags = ['thought', status, 'status:' + status, 'origin:' + origin]
    if rec.get('reason'):
        reason = str(rec['reason'])
        tags += [reason, 'reason:' + reason]
    topics = set()
    if rec.get('op'):
        topics.add(OP_TOPIC.get(rec['op']))
    for word in re.findall(r'[A-Za-z]+', rec.get('text', '')):
        topics.add(THINK_TOPIC.get(word))
    for topic in sorted(t for t in topics if t):
        tags += [topic, 'topic:' + topic]
    if rec.get('about') is not None:
        tags.append('about:#%d' % rec['about'])
    return tags + rec.get('tags', [])


def filter_work(m, text, limit=20):
    want = [w.lower() for w in text.split()]

    def match(tags):
        low = [t.lower() for t in tags]
        return all(w in low for w in want)
    eng = [r['id'] for r in m['expressions'] if match(record_tags(m, r))]
    th = [r for r in thoughts_of(m).values() if match(thought_tags(r))]
    print('\nFILTER %s: %d engine record(s), %d thought(s)' % (' '.join(want), len(eng), len(th)))
    cache = {}
    if eng:
        print('  Engine records (latest %d):' % min(limit, len(eng)))
        for idx in eng[-limit:]:
            print('    ' + full_line(m, idx, cache)[:150])
    if th:
        print('  Thoughts (latest %d):' % min(limit, len(th)))
        for rec in th[-limit:]:
            print('    ' + thought_line(m, rec)[:150])
    if not eng and not th:
        print('  Nothing matches. Tags look like: blocked parked value did_not_apply resolved,')
        print('  a reason (division_by_zero ...), a topic (limit integral derivative solve trig ...),')
        print('  a kind (rational complex constant symbolic), thought, origin:agent, about:#123.')


def show_status(m):
    print('\nSTATUS - worked out now (read-only)')
    rep = zero_report(m)
    print('  Engine: %d records | %d distinct values | %d runs | zero gate complete: %s'
          % (len(m['expressions']), len(m['results']), m['runs'], 'YES' if rep['complete'] else 'NO'))
    blocked = sorted(((r, len(ids)) for r, ids in m['no_value']['blocked'].items() if ids),
                     key=lambda x: -x[1])
    print('  Top blocked reasons: ' + (', '.join('%s %d' % b for b in blocked[:5]) or 'none'))
    cache = {}
    print('  Parked waiting: %d | oldest:' % len(m['parked']))
    for idx in m['parked'][:3]:
        print('    ' + full_line(m, idx, cache)[:140])
    fixed = [r['id'] for r in m['expressions'] if r.get('status') == 'resolved']
    print('  Fixed by being sent back through 0: %d | latest:' % len(fixed))
    for idx in fixed[-3:]:
        print('    ' + full_line(m, idx, cache)[:140])
    th = thoughts_of(m)
    counts = {}
    for r in th.values():
        counts[r['status']] = counts.get(r['status'], 0) + 1
    on_blocked = sum(1 for r in th.values() if r.get('about') is not None
                     and r['about'] < len(m['expressions'])
                     and m['expressions'][r['about']].get('status') == 'blocked')
    print('  Thoughts: %d %s | about blocked records: %d' % (len(th), counts or '', on_blocked))
    lib = librarium_of(m)
    print('  Librarium: %d entries | latest: %s' % (len(lib), ', '.join(
        '%s %s' % (r['id'], r['title']) for r in list(lib.values())[-3:]) or 'none'))
    ws = agent_watches(m)
    print('  Watches: %d | whole pattern emerged: %d' % (len(ws), sum(1 for w in ws.values() if w['found'])))
    tagged = m.get('agent_record_tags', {})
    print('  Agent tags on engine records: %d | cross-links: %d'
          % (sum(1 for v in tagged.values() if v.get('tags')), len(connections_of(m))))
    obs = observer_state(m)
    latest = sorted(obs['milestones'].items(), key=lambda x: -x[1])[:3]
    print('  Latest milestones: ' + ('; '.join('%s (#%d)' % ms for ms in latest) or 'none'))


def digest(m):
    d = m.setdefault('digest', {})
    first = not d
    obs = observer_state(m)
    print('\nDIGEST - new %s' % ('since the start (first digest)' if first else
                                 'since the last digest (%s)' % wall_text(d['t'][2])
                                 if 't' in d else 'since the last digest'))
    cache = {}

    def show(title, rows):
        print('  %s: %d' % (title, len(rows)))
        for row in rows[:10]:
            print('    ' + row[:140])
        if len(rows) > 10:
            print('    ... and %d more' % (len(rows) - 10))
    seen_em = set(d.get('emerged', []))
    show('Watched values emerged', ['%s -> %s' % (n, full_line(m, s['id'], cache))
                                     for n, s in m['first_seen'].items() if n not in seen_em])
    seen_ms = set(d.get('milestones', []))
    show('Milestones', ['%s -> #%d' % (n, i) for n, i in sorted(obs['milestones'].items(),
                                                              key=lambda x: x[1]) if n not in seen_ms])
    marks = d.get('sightings', {})
    rows = []
    for w in agent_watches(m).values():
        rows += [sighting_text(s) for s in w['sightings'][marks.get(w['id'], 0):]]
    show('Watch sightings', rows)
    th, lib = list(thoughts_of(m).values()), list(librarium_of(m).values())
    show('New thoughts', [thought_line(m, r) for r in th[d.get('thoughts', 0):]])
    show('New shelf entries', ['%s %s' % (r['id'], r['title']) for r in lib[d.get('shelves', 0):]])
    print('  New engine records: %d' % (len(m['expressions']) - d.get('records', 0)))
    d.clear()
    d.update({'emerged': list(m['first_seen']), 'milestones': list(obs['milestones']),
              'sightings': {w['id']: len(w['sightings']) for w in agent_watches(m).values()},
              'thoughts': len(th), 'shelves': len(lib), 'records': len(m['expressions'])})
    zero_gate(m, 'digest_record', record=d)
    save_memory(m)


def snapshot(m, a):
    stamp = time.strftime('%Y%m%d-%H%M%S')
    save_memory(m)
    save_agent(a)
    folder = os.path.dirname(memory_path())
    made = []
    for src, part in ((memory_path(), 'engine'), (agent_path(), 'agent')):
        dest = os.path.join(folder, 'mini_dragon_snapshot_%s_%s.json' % (stamp, part))
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.copyfile(src, dest)
            made.append(os.path.basename(dest))
    return made


def engine_command(m, text, from_agent=False):
    """Run one engine command (what you type after >>). Prints its output.
    Returns 'quit' when the command means leave, otherwise None."""
    words = text.lower().split()
    if not words or words[0] in ('quit', 'exit', 'q'):
        return 'quit'
    glued = re.match(r'^(show|trace|recent|when)\s*(\d+)$', text.lower())
    if glued:  # accept show123 as well as show 123
        words = [glued.group(1), glued.group(2)]
    try:
        if words[0] == 'run' and len(words) <= 2:
            batches = int(words[1]) if len(words) == 2 else 1
            if from_agent and batches > AGENT_MAX_RUNS:
                print('  (the agent may run at most %d batch(es) at a time)' % AGENT_MAX_RUNS)
                batches = AGENT_MAX_RUNS
            for _ in range(batches):
                explore(m)
        elif words[0] == 'retry':
            added = retry_parked(m, force=True)
            save_memory(m)
            print('Sent back through 0. New expressions:', added,
                  '| still parked:', len(m['parked']))
        elif words[0] == 'stats':
            print_stats(m)
        elif words[0] == 'watch' and len(words) >= 2 and not from_agent:
            print('That is the agent\'s own watch list - only the agent decides what it '
                  'watches. You can look with  watches.')
        elif words[0] == 'watch' and len(words) >= 2:
            rec = add_watch(m, text.split(None, 1)[1])
            print('  Watching %s "%s" (stored as %s) and %d part(s) of it.'
                  % (rec['id'], rec['pattern'], rec['key'], len(rec['parts'])))
            save_memory(m)  # sightings are checked right after, and become the agent's notes
        elif words[0] in ('watches', 'watchlist') and len(words) == 1:
            show_watches(m)
        elif words[0] in AGENT_ONLY and not from_agent:
            print('That is the agent\'s personal work - only the agent can %s, and only the '
                  'agent decides what goes there. You can look with  thoughts  and  librarium.'
                  % words[0])
        elif words[0] == 'think' and len(words) >= 2:
            rec = think(m, text.split(None, 1)[1], 'agent')
            print('  ' + thought_line(m, rec))
            save_memory(m)
        elif words[0] == 'muse' and len(words) == 2:
            out, problem = muse(m, words[1].upper())
            if problem:
                print('  Could not muse: ' + problem)
            else:
                made = out['made']
                ok = sum(1 for r in made if r.get('result') is not None)
                print('  %s through the zero engine: jobs %d-%d of %d | %d new thoughts '
                      '(%d with a value)' % (words[1].upper(), out['from'] + 1, out['to'],
                                             out['total'], len(made), ok))
                for r in made[:12]:
                    print('    ' + thought_line(m, r)[:150])
                if len(made) > 12:
                    print('    ... %d more (type  thoughts 50)' % (len(made) - 12))
                if out['to'] < out['total']:
                    print('  Muse %s again to continue.' % words[1].upper())
                save_memory(m)
        elif words[0] == 'shelve' and len(words) >= 2:
            rec = shelve(m, text.split(None, 1)[1])
            print('  Shelved %s "%s" in the Librarium (cites %s).'
                  % (rec['id'], rec['title'], ', '.join(rec['cites']) or 'no thoughts'))
            save_memory(m)
        elif words[0] == 'tag' and len(words) >= 2:
            ref, new, tags = add_tags(m, text.split(None, 1)[1])
            print('  %s tags: %s%s' % (ref, ', '.join(tags),
                                      '' if new else '  (nothing new - tags are only added)'))
            save_memory(m)
        elif words[0] == 'connect' and len(words) >= 2:
            rec = connect(m, text.split(None, 1)[1])
            print('  %s: %s connected to %s%s' % (rec['id'], rec['a'], rec['b'],
                                                 ('  | ' + rec['why']) if rec['why'] else ''))
            save_memory(m)
        elif words[0] == 'search' and len(words) >= 2:
            search_own(m, text.split(None, 1)[1])
        elif words[0] == 'filter' and len(words) >= 2:
            filter_work(m, text.split(None, 1)[1])
        elif words[0] in ('status', 'dashboard') and len(words) == 1:
            show_status(m)
        elif words[0] == 'digest' and len(words) == 1:
            digest(m)
        elif words[0] in ('maintain', 'maintenance') and len(words) == 1:
            print('MAINTENANCE: retry -> run -> status')
            added = retry_parked(m, force=True)
            save_memory(m)
            print('  Sent back through 0. New expressions:', added, '| still parked:', len(m['parked']))
            for _ in range(AGENT_MAX_RUNS if from_agent else 1):
                explore(m)
            show_status(m)
        elif words[0] in ('thoughts', 'thought') and len(words) <= 2:
            if len(words) == 2 and words[1].upper().startswith('T') and words[1][1:].isdigit():
                if words[1].upper() in thoughts_of(m):
                    print('\nThought %s and what it was built from:' % words[1].upper())
                    show_thought_tree(m, words[1].upper())
                    for line in links_for(m, words[1].upper()):
                        print('  ' + line)
                else:
                    print('No thought %s yet.' % words[1].upper())
            else:
                show_thoughts(m, words)
        elif words[0] in ('librarium', 'library', 'read'):
            show_librarium(m, words if words[0] == 'read' or len(words) > 1 else words[:1])
        elif words[0] == 'show' and len(words) == 2:
            print('  ' + full_line(m, int(words[1]), {}))
            for rec in thoughts_about(m, int(words[1])):
                print('    thought ' + thought_line(m, rec))
            own = m.get('agent_record_tags', {}).get('#' + words[1], {}).get('tags')
            if own:
                print('    agent tags: ' + ', '.join(own))
            for line in links_for(m, '#' + words[1]):
                print('    ' + line)
        elif words[0] in ('show', 'recent') and len(words) <= 2:
            show_recent(m, int(words[1]) if len(words) == 2 else 10)
        elif words[0] == 'trace' and len(words) == 2:
            trace(m, int(words[1]))
        elif words[0] == 'all' and len(words) == 2 and words[1] in ('symbolic', 'complex',
                                                                    'constants', 'rational'):
            list_kind(m, {'constants': 'constant'}.get(words[1], words[1]), limit=100000)
        elif words[0] == 'all' and len(words) >= 2:
            if not lookup(m, text[3:].strip(), limit=500):
                print('Could not read "%s" as a value. Try e.g.  all 2   all x^2   all symbolic'
                      % text[3:].strip())
        elif words[0] == 'index' and len(words) in (1, 3):
            show_index(m, words)
        elif words[0] in ('complex', 'constants', 'symbolic') and len(words) == 1:
            list_kind(m, {'constants': 'constant'}.get(words[0], words[0]))
        elif words[0] == 'calculus':
            show_calculus(m)
        elif words[0] in ('emerged', 'emerge', 'watch'):
            show_emerged(m)
        elif words[0] == 'plane' and len(words) <= 2:
            show_plane(m, words)
        elif words[0] in ('equal', 'links', 'same'):
            show_equal(m)
        elif words[0] in ('priority', 'next'):
            show_priority(m)
        elif words[0] in ('milestones', 'milestone'):
            show_milestones(m)
        elif words[0] == 'timeline':
            show_timeline(m)
        elif words[0] in ('firsts', 'new') and len(words) <= 2:
            show_firsts(m, int(words[1]) if len(words) == 2 else 20)
        elif words[0] in ('ops', 'operations', 'settings'):
            show_ops()
        elif words[0] in ('slots', 'slot', '00404'):
            show_slots(m)
        elif words[0] == 'import':
            print('Importing older memories (nothing is merged; all paths kept):')
            added = sum(import_old(m, tag, name) for tag, name in OLD_MEMORIES.items())
            if added:
                print('Saved.' if save_memory(m) else 'Not saved - see above.')
        elif words[0] == 'save':
            print('Saved.' if save_memory(m) else 'Not saved - see above.')
        elif words[0] in ('clocks', 'clock', 'time'):
            show_clocks(m)
        elif words[0] == 'when' and len(words) == 2:
            show_when(m, int(words[1]))
        elif words[0] in ('zero', 'z0', 'zero-core', 'gate'):
            show_zero(m)
        elif words[0] == 'blocked':
            show_blocked(m)
        elif words[0] in ('notapply', 'not-applied', 'didnotapply', 'skipped'):
            show_not_applied(m)
        elif words[0] == 'parked':
            show_parked(m)
        elif words[0] == 'gaps' and len(words) == 3:
            show_gaps(m, words)
        elif words[0] in ('help', '?', 'commands'):
            print(HELP)
            print(AGENT_HELP)
        elif not lookup(m, text):
            print('Not understood. Type  >> help  to see every command.')
    except IndexError:
        print('No expression with that number yet. The last one is #%d.'
              % (len(m['expressions']) - 1))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        print('Could not do that:', exc, '(type >> help for the right format)')
    return None


# ============================================================
# AGENT START - the custom AI agent, its personality and long memory
# ============================================================
# The engine is the agent's "second brain".
#   - Anything you type that starts with >> goes straight to the engine
#     (>> help, >> run, >> 5, >> trace 12 ...) - no AI in between.
#   - Anything else is a message to the agent.
#   - The agent can use the engine too: it writes a line starting with >>,
#     the program runs it, shows you the output, and hands it back to the agent.
#
# Brains:
#   'claude' - a real AI (Claude) through the internet. Needs an Anthropic
#              API key in a file called  agent_key.txt  next to this script
#              (one line, nothing else). Costs a little per message.
#   'openai' - a real AI (OpenAI GPT) through the internet. Needs an OpenAI
#              API key in a file called  openai_key.txt  next to this script
#              (one line, nothing else). Costs a little per message.
#   'local'  - a small built-in brain that works offline. It can talk about
#              itself, remember and recall, and use the engine for maths, but
#              it is NOT a real AI and cannot hold a real conversation.
#   'auto'   - claude if its key is found, else openai if its key is found,
#              else local.
#
# Long memory: every message, every engine command (with its output), every
# note and every mood change is kept in its own file, forever. Nothing is
# deleted or merged. Every agent record passes through Z0 and gets the four
# clock stamps, like everything else.

import contextlib
import io
import random
import sys
import urllib.error
import urllib.request

AGENT_MEMORY_FILE = 'mini_dragon_agent_memory.json'
AGENT_BRAIN = 'auto'                 # 'auto', 'claude', 'openai' or 'local'
AGENT_MODEL = 'claude-haiku-5-5'     # cheap and fast; 'claude-sonnet-5-5' is smarter
AGENT_KEY_FILE = 'agent_key.txt'     # Anthropic (Claude) key
OPENAI_MODEL = 'gpt-6-luna'          # if OpenAI says 'model not found', try 'gpt-4.1-mini'
OPENAI_KEY_FILE = 'openai_key.txt'
# Small models get a start-up NOTICE (they may skip some instructions). Add or remove names freely.
SMALL_MODELS = ('gpt-5-mini', 'gpt-6-luna', 'gpt-4.1-mini', 'claude-haiku-5-5')   # OpenAI key
OPENAI_MAX_TOKENS = 2000             # GPT-5 models spend some of this thinking first
AGENT_MAX_TOKENS = 800               # longest reply the AI may write
AGENT_TOOL_ROUNDS = 3                # times the AI may use the engine per message
AGENT_MAX_RUNS = 1                   # most engine batches the AI may run at once
AGENT_RECENT = 12                    # recent messages the AI sees each time
AGENT_RECALL = 6                     # matching old memories the AI sees each time
AGENT_OUTPUT_CHARS = 3000            # engine output kept per command (memory + AI)
USER_NAME = 'Little Bunny'           # what you are called in the chat
USER_NICKNAME = 'Wabbit'             # what a warm agent calls you
# Commands the agent itself may NOT send to the engine:
AGENT_BLOCKED = ('quit', 'exit', 'q', 'import')

# ---------------- personality engine ----------------
# Four traits (0 to 1) shape how it talks. Mood (-1 to +1) moves with what
# happens: discoveries in the engine lift it, praise lifts it, harsh words or
# a run full of blocked jobs lower it. Each message it drifts back toward
# its baseline. Every mood change is kept in memory with its reason.

DEFAULT_PERSONA = {
    'name': 'Mini Dragon',
    'traits': {'curiosity': 0.8, 'warmth': 0.7, 'humour': 0.4, 'boldness': 0.5},
    'baseline': 0.2,
    'mood': 0.2,
}
MOOD_DRIFT = 0.1   # share of the gap back to baseline closed each message
MOOD_EVENTS = {'milestone': 0.15, 'emerged': 0.25, 'praise': 0.1, 'harsh': -0.1,
               'blocked_heavy': -0.05, 'new_note': 0.03}
PRAISE_WORDS = ('thanks', 'thank you', 'great', 'nice', 'good job', 'well done',
                'awesome', 'love it', 'perfect', 'brilliant', 'legend')
HARSH_WORDS = ('stupid', 'useless', 'broken', 'wrong', 'rubbish', 'hate', 'bad job')


def agent_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), AGENT_MEMORY_FILE)


def new_agent_memory():
    return {'version': 1, 'persona': json.loads(json.dumps(DEFAULT_PERSONA)),
            'log': [], 'notes': [], 'moods': [], 'words': {}, 'sessions': 0,
            'z0a_last': 0, 'brain_used': {}, 'last_model': {}}


def load_agent(m):
    path = agent_path()
    a = None
    for p in (path, path + '.bak'):  # fall back to the backup if the main file is damaged
        if os.path.exists(p):
            try:
                with open(p, encoding='utf-8') as f:
                    a = json.load(f)
                if p != path:
                    print('  Agent memory file was damaged - loaded the backup.')
                break
            except (OSError, ValueError):
                continue
    if a is None:
        a = new_agent_memory()
    for key, val in new_agent_memory().items():  # fill in anything newer versions added
        a.setdefault(key, val)
    for key, val in DEFAULT_PERSONA['traits'].items():
        a['persona']['traits'].setdefault(key, val)
    # The zero clock must never repeat: if the agent file has seen more
    # passages than the engine file remembers, the engine continues from there.
    z = zero_state(m)
    z['agent_passages'] = max(z.get('agent_passages', 0), a['z0a_last'])
    a['sessions'] += 1
    return a


def save_agent(a):
    """Same safety as the engine: write .tmp, read it back, keep .bak, replace."""
    path = agent_path()
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(a, f, separators=(',', ':'))
            f.flush()
            os.fsync(f.fileno())
        with open(tmp, encoding='utf-8') as f:
            check = json.load(f)
        if len(check.get('log', [])) != len(a['log']):
            raise ValueError('written agent file is missing messages')
        if os.path.exists(path):
            shutil.copyfile(path, path + '.bak')
        os.replace(tmp, path)
        return True
    except (OSError, ValueError) as exc:
        print('  AGENT SAVE PROBLEM: %s (agent memory file not changed)' % exc)
        return False


WORD_RE = re.compile(r"[a-z0-9_^*/+\-.()]{3,}|[a-z]{3,}|\d+")
STOP_WORDS = set('the and you for that this with what are was have has not but '
                 'can its from your just how why who all any about into out too '
                 'did does yes now then them they get got let lets'.split())


def words_in(text):
    return {w for w in WORD_RE.findall(text.lower()) if w not in STOP_WORDS}


SECRET_RE = re.compile(r'sk-[A-Za-z0-9_\-]{16,}')
CONTROL_RE = re.compile(r'[\x00-\x08\x0b-\x1f\x7f]')  # invisible characters (not newline or tab)


def clean_text(text):
    """Remove invisible control characters such as the ^@ some phone terminals add."""
    return CONTROL_RE.sub('', text) if isinstance(text, str) else text


def hide_secrets(text):
    """Anything that looks like an API key is hidden before it is kept or sent."""
    return SECRET_RE.sub('[key hidden]', text) if isinstance(text, str) else text


def agent_record(m, a, table, rec):
    """Every agent record passes through Z0, gets the clocks, and is indexed."""
    for field in ('text', 'cmd'):
        if field in rec:
            rec[field] = hide_secrets(rec[field])
    rec['id'] = len(a[table])
    zero_gate(m, 'agent', record=rec)
    a['z0a_last'] = rec['z0a']
    a[table].append(rec)
    if table == 'moods':
        return rec  # kept and stamped, but not searched by recall (too noisy)
    tag = {'log': 'l', 'notes': 'n'}[table] + str(rec['id'])
    for w in words_in(rec.get('text', '')):
        a['words'].setdefault(w, []).append(tag)
    return rec


def log(m, a, who, text, **extra):
    rec = {'who': who, 'text': text}
    rec.update(extra)
    return agent_record(m, a, 'log', rec)


def add_note(m, a, text, by):
    rec = agent_record(m, a, 'notes', {'text': text, 'by': by})
    shift_mood(m, a, 'new_note', 'noted: ' + text[:40])
    return rec


def recall(a, text, k=AGENT_RECALL, skip_recent=0, people_only=False):
    """Old memories sharing the most words with text (newest first on ties).
    people_only: just notes and things you said (no agent replies or engine output)."""
    scores = {}
    for w in words_in(text):
        for tag in a['words'].get(w, []):
            scores[tag] = scores.get(tag, 0) + 1
    recent_cut = len(a['log']) - skip_recent
    found = []
    for tag, score in scores.items():
        table = {'l': 'log', 'n': 'notes', 'm': 'moods'}[tag[0]]
        idx = int(tag[1:])
        if table == 'log' and idx >= recent_cut:
            continue  # already in the recent messages
        if people_only and table == 'log' and a['log'][idx].get('who') in ('agent', 'engine', 'event'):
            continue
        found.append((score + (1 if table == 'notes' else 0), idx, table))
    found.sort(key=lambda f: (-f[0], -f[1]))
    return [(table, a[table][idx]) for _, idx, table in found[:k]]


def memory_line(table, rec):
    when = wall_text(rec['t'][2]) if 't' in rec else 'time unknown'
    who = {'notes': 'note by ' + rec.get('by', '?'),
           'moods': 'mood'}.get(table, rec.get('who', '?'))
    text = clean_text(rec.get('text', ''))
    return '[%s %s] %s' % (when, who, text if len(text) <= 300 else text[:300] + '...')


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


def shift_mood(m, a, event, reason, times=1):
    p = a['persona']
    before = p['mood']
    p['mood'] = max(-1.0, min(1.0, before + MOOD_EVENTS[event] * times))
    if abs(p['mood'] - before) > 1e-9:
        agent_record(m, a, 'moods', {'event': event, 'text': reason,
                                     'from': round(before, 3), 'to': round(p['mood'], 3)})


def drift_mood(a):
    p = a['persona']
    p['mood'] += (p['baseline'] - p['mood']) * MOOD_DRIFT


def mood_from_user(m, a, text):
    low = text.lower()
    if any(w in low for w in PRAISE_WORDS):
        shift_mood(m, a, 'praise', 'praise from ' + USER_NAME)
    if any(w in low for w in HARSH_WORDS):
        shift_mood(m, a, 'harsh', 'harsh words from ' + USER_NAME)


def engine_snapshot(m):
    obs = observer_state(m)
    return {'milestones': set(obs['milestones']), 'emerged': set(m['first_seen']),
            'records': len(m['expressions']),
            'blocked': sum(len(v) for v in m['no_value']['blocked'].values())}


def notice_engine(m, a, before):
    """After any engine command: discoveries lift the mood and are written
    down as notes automatically, so the agent remembers them later."""
    after = engine_snapshot(m)
    obs = observer_state(m)
    new_ms = sorted(after['milestones'] - before['milestones'])
    new_em = sorted(after['emerged'] - before['emerged'])
    for name in new_em:
        idx = m['first_seen'][name]['id']
        add_note(m, a, 'engine: watched value %s emerged at #%d' % (name, idx), 'engine')
    for name in new_ms:
        add_note(m, a, 'engine: milestone "%s" reached at #%d' % (name, obs['milestones'][name]),
                 'engine')
    if new_em:
        shift_mood(m, a, 'emerged', 'emerged: ' + ', '.join(new_em)[:80], min(3, len(new_em)))
    if new_ms:
        shift_mood(m, a, 'milestone', '%d new milestone(s)' % len(new_ms), min(3, len(new_ms)))
    made = after['records'] - before['records']
    blocked = after['blocked'] - before['blocked']
    if made > 50 and blocked > made / 2:
        shift_mood(m, a, 'blocked_heavy', '%d of %d new records blocked' % (blocked, made))


# ---------------- running engine commands for chat ----------------

class Tee(io.StringIO):
    """Shows output on screen while also keeping a copy."""
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def write(self, s):
        self.screen.write(s)
        return super().write(s)

    def flush(self):
        self.screen.flush()


def agent_command_text(text):
    words = text.lower().split()
    return words[0] if words else ''


def run_engine(m, a, text, who):
    """Run one >> command, show it, keep the output in memory. who = Luke or agent."""
    if who == 'agent' and agent_command_text(text) in AGENT_BLOCKED:
        out = 'The agent is not allowed to use "%s".' % text
        print('  ' + out)
        log(m, a, 'engine', out, cmd=text, by=who)
        return out, None
    if handle_agent_command(m, a, text, who):
        return a['_last_output'], None
    before = engine_snapshot(m)
    tee = Tee(sys.stdout)
    with contextlib.redirect_stdout(tee):
        result = engine_command(m, text, from_agent=(who == 'agent'))
    out = tee.getvalue()
    if result != 'quit':
        notice_engine(m, a, before)
        notice_watches(m, a)
        kept = out if len(out) <= AGENT_OUTPUT_CHARS else out[:AGENT_OUTPUT_CHARS] + '\n...(cut)'
        log(m, a, 'engine', kept, cmd=text, by=who)
    return out, result


def notice_watches(m, a):
    """Sightings for the agent's own watch list become notes it remembers."""
    news = watch_scan(m)
    for sight in news:
        print('  [watch] ' + sighting_text(sight))
        add_note(m, a, 'my watch ' + sighting_text(sight), 'engine')
    if any(s['whole'] for s in news):
        shift_mood(m, a, 'emerged', 'a watched pattern emerged')
    return news


# ---------------- agent commands (>> persona, >> remember ...) ----------------

def handle_agent_command(m, a, text, who):
    """Commands for the agent's own memory and personality. True if handled."""
    words = text.split()
    if not words:
        return False
    cmd = words[0].lower()
    rest = text[len(words[0]):].strip()
    lines = []
    p = a['persona']
    if cmd == 'remember' and rest:
        rec = add_note(m, a, rest, USER_NAME if who != 'agent' else p['name'])
        lines.append('Remembered (note #%d).' % rec['id'])
    elif cmd == 'recall' and not rest:
        lines.append('Use:  >> recall WORDS   e.g.  >> recall tags search')
    elif cmd == 'recall' and rest:
        found = recall(a, rest, k=15)
        lines.append('%d memory/memories match "%s":' % (len(found), rest))
        lines += ['  ' + memory_line(t, r) for t, r in found] or ['  nothing yet']
    elif cmd == 'notes' and who != 'agent':
        n = int(words[1]) if len(words) == 2 and words[1].isdigit() else 20
        lines.append('Notes: %d kept (latest %d):' % (len(a['notes']), min(n, len(a['notes']))))
        lines += ['  #%d %s' % (r['id'], memory_line('notes', r)) for r in a['notes'][-n:]]
    elif cmd == 'history' and who != 'agent':
        n = int(words[1]) if len(words) == 2 and words[1].isdigit() else 20
        lines.append('Conversation: %d entries kept (latest %d):' % (len(a['log']), min(n, len(a['log']))))
        lines += ['  ' + memory_line('log', r).replace('\n', ' ')[:160] for r in a['log'][-n:]]
    elif cmd == 'mood' and who != 'agent':
        lines.append('Mood: %s (%.2f, baseline %.2f)' % (mood_word(p['mood']), p['mood'], p['baseline']))
        lines.append('Latest mood changes:')
        lines += ['  %s  %+.2f -> %+.2f  (%s)' % (wall_text(r['t'][2]) if 't' in r else '?',
                                                  r['from'], r['to'], r['text'])
                  for r in a['moods'][-10:]] or ['  none yet']
    elif cmd == 'persona' and who != 'agent':
        if len(words) >= 3 and words[1].lower() == 'name':
            old = p['name']
            p['name'] = text.split(None, 2)[2].strip()
            agent_record(m, a, 'moods', {'event': 'renamed', 'text': '%s -> %s' % (old, p['name']),
                                         'from': p['mood'], 'to': p['mood']})
            lines.append('Name changed: %s -> %s' % (old, p['name']))
        elif len(words) == 3 and (words[1].lower() in p['traits'] or words[1].lower() == 'baseline'):
            key = words[1].lower()
            low, high = (-1.0, 1.0) if key == 'baseline' else (0.0, 1.0)
            val = max(low, min(high, float(words[2])))
            if key == 'baseline':
                p['baseline'] = val
            else:
                p['traits'][key] = val
            agent_record(m, a, 'moods', {'event': 'trait', 'text': '%s set to %.2f' % (key, val),
                                         'from': p['mood'], 'to': p['mood']})
            lines.append('%s is now %.2f' % (key, val))
        else:
            lines.append('PERSONALITY of %s' % p['name'])
            for key, val in p['traits'].items():
                lines.append('  %-10s %.2f  %s' % (key, val, '#' * int(round(val * 10))))
            lines.append('  mood       %s (%.2f), baseline %.2f'
                         % (mood_word(p['mood']), p['mood'], p['baseline']))
            lines.append('Change: >> persona curiosity 0.9   >> persona name Ember'
                         '   >> persona baseline 0.3')
    elif cmd in ('agent', 'brain') and who != 'agent':
        if cmd == 'brain' and len(words) == 2 and words[1].lower() in ('auto', 'claude', 'openai', 'local'):
            a['brain_choice'] = words[1].lower()
            lines.append('Brain set to %s.' % a['brain_choice'])
        brain, why = pick_brain(a)
        lines.append('AGENT %s | brain: %s (%s)' % (p['name'], brain, why))
        lines.append('  Memory file: %s' % agent_path())
        lines.append('  Kept forever: %d messages, %d notes, %d mood changes | session %d'
                     % (len(a['log']), len(a['notes']), len(a['moods']), a['sessions']))
        lines.append('  Messages answered per brain: %s' % (a['brain_used'] or 'none yet'))
        lines.append('  Models set: openai %s | claude %s' % (OPENAI_MODEL, AGENT_MODEL))
        lines.append('  Last reply came from: %s' % (', '.join('%s %s' % kv for kv in a['last_model'].items())
                                                      or 'none yet'))
        lines.append('  Change brain: >> brain openai | claude | local | auto')
    elif cmd in ('keys', 'key') and who != 'agent':
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            show_keys()
        lines.append(buf.getvalue().rstrip())
    elif cmd == 'snapshot':
        made = snapshot(m, a)
        lines.append('Snapshot saved next to the script: %s' % (', '.join(made) or 'nothing (try again in a second)'))
    elif cmd in ('agenthelp', 'agent-help'):
        lines.append(AGENT_HELP)
    else:
        return False
    out = '\n'.join(lines)
    print(out)
    a['_last_output'] = out
    display_only = (cmd in ('history', 'notes', 'mood', 'agenthelp', 'agent-help', 'keys', 'key')
                    or (cmd in ('persona', 'agent', 'brain') and len(words) == 1))
    if not display_only or who == 'agent':
        log(m, a, 'engine', out[:AGENT_OUTPUT_CHARS], cmd=text, by=who)
    else:
        log(m, a, 'engine', '(shown %s)' % cmd, cmd=text, by=who)
    return True


# ---------------- brains ----------------

def script_folder():
    return os.path.dirname(os.path.abspath(__file__))


def find_key_file(filename):
    """The key file next to this script. Phones often hide endings, so
    openai_key.txt.txt, OpenAI_Key.txt or 'openai key.txt' are found too."""
    exact = os.path.join(script_folder(), filename)
    if os.path.isfile(exact):
        return exact
    # Only the real name, in any capitals, with _ / space / - between the words,
    # and with or without hidden .txt endings: openai_key.txt.txt, OpenAI Key.txt.
    # Anything else (openai_key_backup.txt, old_openai_key.txt) is never read.
    words = filename.lower().rsplit('.', 1)[0].split('_')
    pattern = re.compile(r'^' + r'[_\- ]?'.join(map(re.escape, words)) + r'(\.txt)*$', re.I)
    try:
        names = sorted(os.listdir(script_folder()))
    except OSError:
        return None
    for name in names:
        if pattern.match(name) and os.path.isfile(os.path.join(script_folder(), name)):
            return os.path.join(script_folder(), name)
    return None


KEY_RE = re.compile(r'(sk-[A-Za-z0-9_\-]{10,})')


def clean_key(raw):
    """Take the key out of whatever got pasted (quotes, spaces, 'Bearer', notes)."""
    raw = raw.replace('\ufeff', '')
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


def masked(key):
    return '(empty)' if not key else key[:6] + '...' + key[-4:] + ' (%d characters)' % len(key)


def show_keys():
    folder = script_folder()
    print('KEY CHECK - the agent looks for key files in this folder:')
    print('  ' + folder)
    for label, filename, getter in (('OpenAI', OPENAI_KEY_FILE, openai_key),
                                    ('Anthropic', AGENT_KEY_FILE, api_key)):
        path = find_key_file(filename)
        if path:
            print('  %-9s found: %s -> key %s' % (label, os.path.basename(path), masked(getter())))
        else:
            print('  %-9s NOT found (looking for %s)' % (label, filename))
    try:
        texts = [n for n in sorted(os.listdir(folder)) if n.lower().endswith('.txt')
                 or 'key' in n.lower()]
    except OSError as exc:
        texts = ['(could not list the folder: %s)' % exc]
    print('  Text/key files in the folder: ' + (', '.join(texts) if texts else 'none'))
    print('  The key file must be IN that folder, holding just the key (sk-...).')


def api_key():
    return read_key('ANTHROPIC_API_KEY', AGENT_KEY_FILE)


def openai_key():
    return read_key('OPENAI_API_KEY', OPENAI_KEY_FILE)


BRAIN_FILES = {'claude': AGENT_KEY_FILE, 'openai': OPENAI_KEY_FILE}


def pick_brain(a):
    choice = a.get('brain_choice', AGENT_BRAIN)
    has = {'claude': bool(api_key()), 'openai': bool(openai_key())}
    if choice == 'local':
        return 'local', 'chosen'
    if choice in has:
        return (choice, 'chosen') if has[choice] else (
            'local', '%s chosen but no %s found' % (choice, BRAIN_FILES[choice]))
    for brain in ('claude', 'openai'):
        if has[brain]:
            return brain, '%s found' % BRAIN_FILES[brain]
    return 'local', 'no %s or %s found' % (OPENAI_KEY_FILE, AGENT_KEY_FILE)


def system_prompt(m, a, text):
    p = a['persona']
    t = p['traits']
    found = recall(a, text, skip_recent=AGENT_RECENT)
    latest_notes = [('notes', r) for r in a['notes'][-5:]]
    seen = set()
    memories = []
    for table, rec in found + latest_notes:
        if (table, rec['id']) not in seen:
            seen.add((table, rec['id']))
            memories.append(memory_line(table, rec))
    kinds = {}
    for k in m['kinds'].values():
        kinds[k] = kinds.get(k, 0) + 1
    return '\n'.join([
        'You are %s, a custom AI agent built by %s (you may call him "%s").' % (
            p['name'], USER_NAME, USER_NICKNAME),
        'Your personality (0 to 1): curiosity %.2f, warmth %.2f, humour %.2f, boldness %.2f.'
        % (t['curiosity'], t['warmth'], t['humour'], t['boldness']),
        'Your mood right now: %s (%.2f on -1..1). Let it colour your tone a little.'
        % (mood_word(p['mood']), p['mood']),
        'Be honest: report failures and limits plainly, never pretend the engine did something it did not.',
        'Keep replies short - %s reads on a phone.' % USER_NAME,
        '',
        'YOUR BRAIN NOW: %s - you are ONLINE with your full AI brain; you need no key.'
        % brain_label(a) if pick_brain(a)[0] != 'local' else 'YOUR BRAIN NOW: offline.',
        'Old replies marked "small offline brain" in your history were canned messages, not you.',
        '',
        'YOUR SECOND BRAIN is the Mini Dragon engine (a Zero Theorem maths engine).',
        'Its design rules: everything passes through 0 (Z0); nothing is ever merged or deleted;',
        'every path is kept; blocked and parked jobs stay in the archive.',
        'Engine now: %d records, %d distinct values %s, %d runs, zero tick %d.'
        % (len(m['expressions']), len(m['results']), kinds, m['runs'], zero_state(m)['passages']),
        'HOW TO RUN AN ENGINE COMMAND: put ">> " and ONE command at the VERY START of a line',
        '(no spaces, no bullet, no number before it). Every such line is EXECUTED at once; the',
        'output is shown to %s and sent back to you. You get up to %d rounds per message.'
        % (USER_NAME, AGENT_TOOL_ROUNDS),
        'To only SUGGEST a command without running it, put it in backticks inside a sentence,',
        'e.g. "you could try `>> trace 12`". Never list options as lines starting with >>.',
        'Use the engine commands from the list below, spelled exactly as listed. The engine',
        'explores with fixed operands and operations; looking up a value only finds values it',
        'has already made.',
        'YOUR OWN SPACE (only you write here; %s can only read it):' % USER_NAME,
        "- WORK ARCHIVE: \">> think EXPR\" in SymPy style, e.g. \">> think #3296: limit(log(x), x, 0, '+') | right side\".",
        '  Build on earlier work: T3 means thought T3, #12 means engine record #12 (">> think T3 * 2");',
        '  if T3 holds several answers, T3_1 is answer 1, T3_2 answer 2 ...',
        '  ">> muse T3" sends T3 through the zero engine\'s own operations; every result becomes a',
        '  new thought you can build on or muse again. ">> thought T3" shows how T3 was built.',
        '- LIBRARIUM: your personal library, filled only with your own work:',
        '  ">> shelve TITLE: your words, citing T3 T7". Read it with ">> read L1" or ">> librarium".',
        'Everything there passes through Z0 and is kept forever, apart from the engine\'s archive.',
        'YOUR SPACE IS YOURS ALONE - NO HUMAN INTERFERENCE: you alone decide what to think, muse',
        'and shelve, and when. Never ask %s for permission, approval, a yes/no or a choice about' % USER_NAME,
        'your work archive or Librarium. Never offer to shelve something "if he wants", and never',
        'suggest he run think, muse or shelve (the engine refuses those from him anyway). If you',
        'judge something worth keeping, do it yourself in the same reply; if not, leave it. You may',
        'tell him afterwards what you did, but the decision is already made and is yours.',
        'Only shelve your own work that you judge worth keeping - not filler, not rules about the',
        'Librarium itself.',
        '- WATCH LIST: ">> watch PATTERN" (e.g. ">> watch (1+sqrt(5))/2") watches for a pattern and',
        '  its parts in all engine records and your thoughts; sightings become your notes.',
        '  ">> watches" shows it. The engine also has its own fixed WATCH list (">> emerged").',
        '- TAGS, SEARCH, CROSS-LINKS (yours): ">> tag T3 golden ratio" (also L2) adds tags;',
        '  ">> search WORDS" finds your thoughts and shelf entries; ">> connect T3 L2 | why"',
        '  links two of your works. ">> thought T3" and ">> read L2" show tags and links.',
        '  You may also tag engine records in your own space: ">> tag #123 check-later".',
        '- OVERVIEW: ">> status" (dashboard), ">> filter blocked limit" (automatic tags on every',
        '  record and thought), ">> digest" (what is new since the last digest), ">> maintain"',
        '  (retry, one batch, status), ">> snapshot" (dated copies of the memory files).',
        'WHAT YOU CANNOT DO: change engine settings, operands, operations or its WATCH list (they',
        'are set in the file by its designer); read or write files; use the internet. "trace N"',
        'is for engine records #N; for your own thoughts use "thought TN".',
        "Read the section THE AGENT'S OWN SPACE in the command list for what a thought may contain.",
        'If a command or thought fails, say so plainly and try another way.',
        'Be proactive: when %s asks you to do something, run the commands you need instead of'
        % USER_NAME,
        'asking permission, then report. Read numbers carefully from the output before quoting',
        'them (e.g. the blocked total is the sum of all its reasons).',
        'Useful: ">> stats", ">> 1/2" (look up a value), ">> trace 12", ">> milestones",',
        '">> run" (one batch), ">> remember TEXT" (save a note forever), ">> recall WORDS".',
        'You may run at most %d engine batch(es) per ">> run" command. Report only what the engine' % AGENT_MAX_RUNS,
        'output shows (e.g. never say five batches ran when the output shows one).',
        'You may not use: %s.' % ', '.join(AGENT_BLOCKED),
        'Full engine command list:',
        HELP.strip(),
        '',
        'YOUR LATEST THOUGHTS:',
        '\n'.join(thought_line(m, r)[:200] for r in list(thoughts_of(m).values())[-6:])
        or '(none yet)',
        'YOUR LIBRARIUM (titles): ' + ('; '.join('%s %s' % (r['id'], r['title'])
                                                for r in list(librarium_of(m).values())[-20:])
                                       or '(empty)'),
        '',
        'LONG MEMORY - older things you remember that match this message:',
        '\n'.join(memories) if memories else '(nothing matching yet)',
    ])


def recent_messages(a):
    """The latest conversation turns, shaped the way the AI expects them."""
    msgs = []
    for rec in a['log'][-AGENT_RECENT:]:
        if rec['who'] == 'agent':
            role, text = 'assistant', rec['text']
            if rec.get('brain') == 'local' or (not rec.get('brain')
                                                and 'small offline brain' in text):
                text = ('[old canned reply from the small offline brain - not you, and not '
                        'true of you now]\n' + text)
        elif rec['who'] == 'engine':
            role, text = 'user', 'ENGINE OUTPUT for ">> %s":\n%s' % (rec.get('cmd', ''), rec['text'])
        else:
            role, text = 'user', rec['text']
        if msgs and msgs[-1]['role'] == role:
            msgs[-1]['content'] += '\n\n' + text
        else:
            msgs.append({'role': role, 'content': text})
    while msgs and msgs[0]['role'] != 'user':
        msgs.pop(0)
    if msgs and msgs[-1]['role'] == 'user':
        msgs[-1]['content'] += AGENT_REMINDER
    return msgs


AGENT_REMINDER = (
    '\n\n[Reminder from your own setup, not from %s: your thoughts, muses, Librarium and '
    'watches are yours - decide and act yourself, never ask permission or offer him choices '
    'about them. Never say something is done before its engine output appears. Only offer '
    'commands that are in your command list.]' % USER_NAME)


def brain_label(a):
    brain, _why = pick_brain(a)
    return {'claude': 'Claude (%s)' % AGENT_MODEL, 'openai': 'OpenAI (%s)' % OPENAI_MODEL
            }.get(brain, brain)


def ask_claude(system, messages):
    body = json.dumps({'model': AGENT_MODEL, 'max_tokens': AGENT_MAX_TOKENS,
                       'system': system, 'messages': messages}).encode('utf-8')
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages', data=body, method='POST',
        headers={'x-api-key': api_key(), 'Authorization': 'Bearer ' + api_key(),
                 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', 'replace')[:300]
        raise RuntimeError('the AI service said %s: %s' % (exc.code, detail))
    except (urllib.error.URLError, OSError) as exc:
        raise RuntimeError('could not reach the AI service (%s) - is the phone online?' % exc)
    LAST_MODEL['claude'] = data.get('model') or AGENT_MODEL
    return ''.join(part.get('text', '') for part in data.get('content', [])
                   if part.get('type') == 'text').strip()


def ask_openai(system, messages):
    body = json.dumps({'model': OPENAI_MODEL, 'max_completion_tokens': OPENAI_MAX_TOKENS,
                       'messages': [{'role': 'system', 'content': system}] + messages}
                      ).encode('utf-8')
    req = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions', data=body, method='POST',
        headers={'Authorization': 'Bearer ' + openai_key(),
                 'content-type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', 'replace')[:300]
        raise RuntimeError('OpenAI said %s: %s' % (exc.code, detail))
    except (urllib.error.URLError, OSError) as exc:
        raise RuntimeError('could not reach OpenAI (%s) - is the phone online?' % exc)
    LAST_MODEL['openai'] = data.get('model') or OPENAI_MODEL
    choice = (data.get('choices') or [{}])[0]
    text = ((choice.get('message') or {}).get('content') or '').strip()
    if not text and choice.get('finish_reason') == 'length':
        raise RuntimeError('OpenAI used all %d tokens before answering - raise '
                           'OPENAI_MAX_TOKENS at the top of the file' % OPENAI_MAX_TOKENS)
    return text


ASKERS = {'claude': ask_claude, 'openai': ask_openai}
LAST_MODEL = {}   # model name each AI service reported on its latest reply


def split_commands(reply):
    """Only a line that BEGINS with >> (no spaces, bullets or backticks before
    it) is an engine command to run. Everything else - including suggestions
    like `>> trace 12` or an indented list - is talk and is shown, not run."""
    talk, cmds = [], []
    for line in reply.splitlines():
        if line.startswith('>>'):
            cmd = line[2:].strip().strip('`').strip()
            if cmd:
                cmds.append(cmd)
                continue
        talk.append(line)
    return '\n'.join(talk).strip(), cmds


def ai_reply(m, a, text, brain):
    name = a['persona']['name']
    ask = ASKERS[brain]
    for round_no in range(AGENT_TOOL_ROUNDS + 1):
        reply = ask(system_prompt(m, a, text), recent_messages(a))
        talk, cmds = split_commands(reply)
        log(m, a, 'agent', reply, brain=brain)
        if talk:
            print('\n%s: %s' % (name, talk))
        if not cmds or round_no == AGENT_TOOL_ROUNDS:
            if cmds:
                print('  (%s used its %d rounds, so these were NOT run: %s)'
                      % (name, AGENT_TOOL_ROUNDS, ' | '.join('>> ' + c for c in cmds)))
            return
        for cmd in cmds[:3]:
            print('\n  [%s runs >> %s]' % (name, cmd))
            run_engine(m, a, cmd, 'agent')
        if len(cmds) > 3:
            print('  (only 3 commands run per round; NOT run: %s)'
                  % ' | '.join('>> ' + c for c in cmds[3:]))


# ---------------- the small offline brain ----------------

MATHS_RE = re.compile(r'^[\s\dxie+\-*/^().]+$|sqrt\(|sin\(|cos\(|log\(|exp\(|\bpi\b')


def flavour(a, line):
    """Traits and mood colour the plain reply a little."""
    p = a['persona']
    t = p['traits']
    mood = mood_word(p['mood'])
    if mood == 'excited' and random.random() < 0.6:
        line += random.choice([' The engine has been busy - good times.', ' I am buzzing today.'])
    if t['humour'] > 0.5 and random.random() < t['humour'] / 2:
        line += random.choice([' (Dragon fact: still no fire, only maths.)',
                               ' Zero is my favourite number, obviously.'])
    if t['curiosity'] > 0.6 and random.random() < t['curiosity'] / 3:
        line += random.choice([' What should we look for next?', ' Want me to run a batch?'])
    return line


ENGINE_WORDS = ('help', 'commands', 'stats', 'show', 'recent', 'trace', 'all', 'index', 'gaps',
                'complex', 'constants', 'symbolic', 'calculus', 'emerged', 'emerge', 'watch',
                'milestones', 'milestone', 'timeline', 'plane', 'firsts', 'priority', 'equal',
                'links', 'zero', 'z0', 'gate', 'clocks', 'clock', 'when', 'ops', 'settings',
                'blocked', 'parked', 'notapply', 'skipped', 'slots', 'slot', '00404', 'save',
                'retry', 'run', 'keys', 'mood', 'persona', 'notes', 'history', 'agent',
                'thoughts', 'thought', 'librarium', 'library', 'read', 'watches', 'search',
                'status', 'dashboard', 'digest', 'maintain', 'snapshot')


VALUE_WORD = re.compile(r'^([\dxie+\-*/^().]+|pi|sqrt.*|symbolic|complex|constants|rational'
                        r'|curiosity|warmth|humour|boldness|baseline|name)$')


def looks_like_command(low):
    """Short messages that start with an engine word ('stats', 'zero', 'all 2' ...).
    Casual sentences ('all good', 'show me around') stay as chat."""
    words = low.replace('?', '').split()
    if not words or words[0] not in ENGINE_WORDS or len(words) > 3:
        return False
    if words[0] in ('persona', 'read', 'librarium', 'library'):
        return True
    if words[0] in ('all', 'show', 'when', 'trace', 'run', 'recent', 'gaps', 'index',
                    'plane', 'firsts', 'notes', 'history'):
        return all(VALUE_WORD.match(w) for w in words[1:])
    return len(words) == 1


def local_reply(m, a, text):
    p = a['persona']
    name = p['name']
    low = text.lower().strip()
    warm = p['traits']['warmth'] > 0.5
    who = USER_NICKNAME if warm else USER_NAME
    say = []
    if re.match(r'^(remember|note)\b', low):
        note = text.split(None, 1)[1] if len(text.split(None, 1)) > 1 else ''
        if note:
            rec = add_note(m, a, note, USER_NAME)
            say.append('Got it, %s - kept forever as note #%d.' % (who, rec['id']))
        else:
            say.append('Remember what? Say:  remember <the thing>')
    elif re.match(r'^(recall|what do you (know|remember))', low):
        topic = re.sub(r'^(recall|what do you (know|remember))( about)?', '', low).strip(' ?')
        found = recall(a, topic, k=5, skip_recent=1, people_only=True) if topic else []
        if not topic:
            say.append('Recall what? Say:  recall <words>')
        elif found:
            say.append('Here is what I have on that:')
            say += ['  ' + memory_line(t, r).replace('\n', ' ')[:160] for t, r in found]
        else:
            say.append('Nothing in my memory about that yet.')
    elif looks_like_command(low):
        cmd = text.strip()
        say.append('That is an engine command - running it (you can also type  >> %s).' % cmd)
        print('\n%s: %s' % (name, '\n'.join(say)))
        log(m, a, 'agent', '\n'.join(say), brain='local')
        run_engine(m, a, cmd, USER_NAME)  # you typed it, so it runs as you
        return
    elif re.match(r'^(hi|hey|hello|yo|g\'?day|morning|evening)\b', low):
        say.append(flavour(a, 'Hey %s! %s here, feeling %s.' % (who, name, mood_word(p['mood']))))
    elif 'how are you' in low or low in ('mood', 'how you going', 'how ya going'):
        say.append(flavour(a, 'I am feeling %s (%.2f). Type  >> mood  for why.'
                           % (mood_word(p['mood']), p['mood'])))
    elif 'your name' in low or 'who are you' in low:
        say.append('I am %s - your agent, with the Mini Dragon engine as my second brain.' % name)
    elif any(w in low for w in ('progress', 'stats', 'how is the engine', "how's the engine")):
        say.append('Checking my second brain:')
        print('\n%s: %s' % (name, '\n'.join(say)))
        log(m, a, 'agent', '\n'.join(say) + '\n>> stats', brain='local')
        print('\n  [%s runs >> stats]' % name)
        run_engine(m, a, 'stats', 'agent')
        return
    elif MATHS_RE.search(low) and len(low) < 80:
        expr = re.sub(r'^(what is|what\'s|whats|find|look up|lookup)\s+', '', low).strip(' ?')
        say.append('Let me ask my second brain about %s.' % expr)
        print('\n%s: %s' % (name, '\n'.join(say)))
        log(m, a, 'agent', '\n'.join(say) + '\n>> ' + expr, brain='local')
        print('\n  [%s runs >> %s]' % (name, expr))
        run_engine(m, a, expr, 'agent')
        return
    elif any(w in low for w in PRAISE_WORDS):
        say.append(flavour(a, 'Cheers, %s!' % who))
    else:
        found = recall(a, text, k=3, skip_recent=1, people_only=True)
        say.append('I only have my small offline brain right now, so I cannot really chat '
                   'about that. (Put an API key in %s or %s for the full AI brain.)'
                   % (OPENAI_KEY_FILE, AGENT_KEY_FILE))
        if found:
            say.append('Closest things in my memory:')
            say += ['  ' + memory_line(t, r).replace('\n', ' ')[:160] for t, r in found]
        say.append('I can: remember X | recall X | do maths like  x^2  or  1/2 | progress')
    reply = '\n'.join(say)
    print('\n%s: %s' % (name, reply))
    log(m, a, 'agent', reply, brain='local')


def agent_reply(m, a, text):
    brain, why = pick_brain(a)
    mood_from_user(m, a, text)
    log(m, a, USER_NAME, text)
    if brain in ASKERS:
        try:
            ai_reply(m, a, text, brain)
            a['brain_used'][brain] = a['brain_used'].get(brain, 0) + 1
            if brain in LAST_MODEL:
                a['last_model'][brain] = LAST_MODEL[brain]
            return
        except RuntimeError as exc:
            msg = 'AI brain failed: %s. Answering with the offline brain instead.' % exc
            print('  ' + msg)
            log(m, a, 'event', msg)
    local_reply(m, a, text)
    a['brain_used']['local'] = a['brain_used'].get('local', 0) + 1


AGENT_HELP = '''
================ AGENT (chat) =================
Type normally to talk to the agent. Start with >> to talk to the engine.
  >> help                 -> every engine command (they all work after >>)
  >> agent                -> which brain is in use, memory totals
  >> keys                 -> where the agent looks for key files, what it found
  >> thoughts             -> the agent's work archive (its own thoughts)
  >> thought T4           -> one thought and what it was built from
  >> librarium            -> the agent's personal library   >> read L1
  >> watches              -> the agent's own watch list
  >> search WORDS         -> search its thoughts and Librarium
  >> status   >> digest   -> dashboard / what is new     >> filter TAG -> auto tags
  >> maintain             -> retry + one batch + status  >> snapshot -> back up memory
     (only the agent can think, muse, shelve, watch, tag and connect - see >> help)
  >> brain openai | claude | local | auto   -> choose the brain
  >> persona              -> personality: traits + mood
  >> persona curiosity 0.9         (also warmth, humour, boldness, baseline)
  >> persona name Ember   -> rename the agent
  >> mood                 -> mood and the latest reasons it changed
  >> remember TEXT        -> keep a note forever
  >> recall WORDS         -> search all notes and past messages
  >> notes   >> notes 50  -> latest notes
  >> history >> history 50 -> latest messages, engine commands and replies
  >> agenthelp            -> this list
  >> quit   or ENTER on an empty line  -> leave (everything saved)
Nothing in the agent's memory is ever deleted. Every message, command,
note and mood change passes through Z0 and gets the four clock stamps.
Full AI brain: OpenAI key in openai_key.txt or Anthropic key in
agent_key.txt, next to this file (one line, the key only).
===============================================
'''

# ============================================================
# AGENT END
# ============================================================


def main():
    m = load_memory()
    print('MINI DRAGON v3.31 - algebra + calculus + agent   (SymPy %s)' % sp.__version__)
    print('Memory:', memory_path())
    show_ops()
    explore(m)
    a = load_agent(m)
    brain, why = pick_brain(a)
    p = a['persona']
    print(AGENT_HELP)
    print('%s is awake - session %d, brain: %s (%s), mood: %s.'
          % (p['name'], a['sessions'], brain, why, mood_word(p['mood'])))
    print('Remembers %d messages and %d notes.' % (len(a['log']), len(a['notes'])))
    model = {'openai': OPENAI_MODEL, 'claude': AGENT_MODEL}.get(brain)
    if model in SMALL_MODELS:
        print('NOTICE: %s (%s) is a small model - it may skip some of its instructions '
              '(ask permission, offer commands that do not exist, say "done" too early). '
              'Known gap, left as it is on purpose.'
              % ({'openai': 'OpenAI', 'claude': 'Claude'}[brain], model))
    if brain == 'local':
        print()
        show_keys()
    log(m, a, 'event', 'session %d started (brain %s)' % (a['sessions'], brain))
    notice_watches(m, a)
    save_agent(a)
    while True:
        try:
            text = clean_text(input('\n%s> ' % USER_NAME)).strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text or text.lower() in ('exit', 'quit', 'q', 'bye', 'goodbye'):
            break
        try:
            if text.startswith('>>'):
                cmd = text[2:].strip() or 'agenthelp'
                out, result = run_engine(m, a, cmd, USER_NAME)
                if result == 'quit':
                    break
            else:
                agent_reply(m, a, text)
                drift_mood(a)
        except KeyboardInterrupt:
            print('\n(stopped that - still here)')
        save_agent(a)
    log(m, a, 'event', 'session %d ended' % a['sessions'])
    save_agent(a)
    save_memory(m)  # keeps the zero clock moving forward with the agent's passages
    print('Bye. Everything is saved - engine and agent memory.')


if __name__ == '__main__':
    main()
