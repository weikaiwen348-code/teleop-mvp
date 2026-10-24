"""Bounded authenticated JSON datagrams. HMAC provides integrity, not encryption."""
from dataclasses import dataclass
import hashlib
import hmac
import json
import secrets
from .config import vector

MAX_PACKET = 8192


def encode(message, key):
    if len(key) < 32:
        raise ValueError("use a random key of at least 32 bytes")
    payload = json.dumps(message, separators=(",", ":"), allow_nan=False).encode()
    wire = hmac.new(key, payload, hashlib.sha256).hexdigest().encode() + b"\n" + payload
    if len(wire) > MAX_PACKET:
        raise ValueError("packet too large")
    return wire


def decode(wire, key):
    if len(key) < 32 or len(wire) > MAX_PACKET:
        raise ValueError("invalid key or oversized packet")
    try:
        sig, payload = wire.split(b"\n", 1)
        expected = hmac.new(key, payload, hashlib.sha256).hexdigest().encode()
        if not hmac.compare_digest(sig, expected):
            raise ValueError("authentication failed")
        value = json.loads(payload, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
        if not isinstance(value, dict) or value.get("v") != 1:
            raise ValueError("unsupported envelope")
        return value
    except (UnicodeError, RecursionError, TypeError) as e:
        raise ValueError("invalid packet") from e


@dataclass
class Command:
    seq: int
    q: list
    gripper: float
    deadman: bool
    arm_epoch: str = ""
    estop: bool = False

    def validate(self, n):
        if type(self.seq) is not int or not 0 <= self.seq < 2**53:
            raise ValueError("invalid sequence")
        if not isinstance(self.q, list) or len(self.q) != n or any(type(x) not in (int, float) or abs(x) > 1e6 for x in self.q):
            raise ValueError("q must be a list of bounded numeric radians")
        vector(self.q, n, "command.q")
        if type(self.gripper) not in (float, int) or not 0 <= self.gripper <= 1:
            raise ValueError("gripper must be normalized [0,1], 0=open, 1=closed")
        if type(self.deadman) is not bool or type(self.estop) is not bool:
            raise ValueError("deadman and estop must be booleans")
        if not isinstance(self.arm_epoch, str) or len(self.arm_epoch) > 64:
            raise ValueError("invalid arm epoch")
        return self


class LeaseBook:
    """Robot-issued freshness challenges avoid subtracting unrelated host clocks.

    Client must sample leader AFTER receiving the challenge. Age from challenge
    creation bounds age of correctly implemented fresh sampling, not malicious input.
    """
    def __init__(self, lifetime):
        self.session = secrets.token_hex(16)
        self.lifetime = lifetime
        self.leases = {}

    def issue(self, now):
        self.leases = {k: v for k, v in self.leases.items() if v > now}
        token = secrets.token_hex(16)
        self.leases[token] = now + self.lifetime
        return token

    def check(self, session, token, now):
        if not isinstance(session, str) or not isinstance(token, str):
            raise ValueError("invalid session or challenge type")
        expiry = self.leases.get(token, -1)
        if session != self.session or expiry <= now:
            raise ValueError("wrong session or expired challenge")
        return expiry
