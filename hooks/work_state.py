"""Faces state hooks: the state is the directory's, in .faces/state (or
.faces/state.local, which overrides it), as `faces state:create --use` and `faces state:use <id>`
write it. The state is a boolean proof; these hooks only show it.

start:  set FACES_SESSION for the session (every faces write records it), and print the
        directory's state as `faces state:get` renders it (the whole proof and its last line).
stop:   (Stop and SubagentStop) print the proof's last line. Never blocks.
end:    release the claims this session took (`faces premise:claim --release --session`).

The key is FACES_API_KEY, else ~/.faces/work_key. Every line is the server's text, as it is."""
import json
import os
import subprocess
import sys

HOME = os.path.expanduser("~/.faces")


def state_file(cwd):
    d = os.path.abspath(cwd or os.getcwd())
    while True:
        for name in ("state.local", "state"):
            p = os.path.join(d, ".faces", name)
            try:
                sid = open(p).read().strip().split()[0]
                if sid:
                    return p, sid
            except (OSError, IndexError):
                pass
        up = os.path.dirname(d)
        if up == d:
            return None, None
        d = up


def session_name(ev):
    s = ev.get("session_id") or ""
    return "claude-code:%s" % s if s else os.environ.get("FACES_SESSION", "")


def env(ev):
    e = dict(os.environ)
    if not e.get("FACES_API_KEY"):
        try:
            e["FACES_API_KEY"] = open(os.path.join(HOME, "work_key")).read().strip()
        except OSError:
            pass
    s = session_name(ev)
    if s:
        e["FACES_SESSION"] = s
    return e


def faces(ev, *args, timeout=30):
    """The command's JSON output, or None."""
    r = subprocess.run(["faces", *args, "--json"], capture_output=True, text=True, env=env(ev),
                       cwd=ev.get("cwd") or None, timeout=timeout)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def proof(ev):
    """`faces state:get`'s text, or (None, the reason it could not be read)."""
    r = subprocess.run(["faces", "state:get"], capture_output=True, text=True, env=env(ev),
                       cwd=ev.get("cwd") or None, timeout=30)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.rstrip(), None
    return None, (r.stderr or r.stdout).strip()[:300] or "no reply"


def start(ev):
    s = session_name(ev)
    envf = os.environ.get("CLAUDE_ENV_FILE")
    if s and envf:
        with open(envf, "a") as f:
            f.write("export FACES_SESSION=%s\n" % s)
    path, sid = state_file(ev.get("cwd"))
    if not sid:
        ctx = ("No Faces state in this directory (no .faces/state). faces state:create --use creates one; "
               "faces state:use <id> uses one of yours.")
    else:
        text, why = proof(ev)
        ctx = ("Faces state %s (%s):\n%s" % (sid, path, text)) if text else \
            "Faces state %s (%s) could not be read: %s" % (sid, path, why)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx}}))


def stop(ev):
    """The proof's last line, shown; never a block."""
    _path, sid = state_file(ev.get("cwd"))
    if not sid:
        return
    y = faces(ev, "state:get") or {}
    last = [x for x in y.get("summary") or [] if x]
    if last:
        print(json.dumps({"systemMessage": "Faces state %s: %s" % (sid, " ".join(last))}))


def end(ev):
    _path, sid = state_file(ev.get("cwd"))
    s = session_name(ev)
    if sid and s:
        faces(ev, "premise:claim", "--release", "--session", s)


if __name__ == "__main__":
    mode = sys.argv[1]
    try:
        ev = json.load(sys.stdin)
    except ValueError:
        ev = {}
    try:
        {"start": start, "stop": stop, "end": end}[mode](ev)
    except Exception:
        pass
    sys.exit(0)
