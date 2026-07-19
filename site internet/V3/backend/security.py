from collections import defaultdict, deque
from datetime import datetime, timedelta
from functools import wraps
from secrets import token_urlsafe

from flask import abort, current_app, jsonify, request, session


_RATE_LIMIT_STORAGE = defaultdict(deque)


def get_csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def validate_csrf_token(submitted_token):
    expected_token = session.get("_csrf_token")
    return bool(expected_token and submitted_token and expected_token == submitted_token)


def csrf_protect():
    if not current_app.config.get("CSRF_ENABLED", True):
        return

    submitted_token = request.headers.get("X-CSRF-Token")
    if not submitted_token:
        submitted_token = request.form.get("csrf_token")

    if validate_csrf_token(submitted_token):
        return

    if request.is_json:
        return jsonify({"error": "CSRF token invalide"}), 400

    abort(400, description="CSRF token invalide")


def rate_limit(key_prefix, max_requests, window_seconds):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_app.config.get("RATE_LIMIT_ENABLED", True):
                return view(*args, **kwargs)

            max_allowed = current_app.config.get(max_requests, max_requests) if isinstance(max_requests, str) else max_requests
            window = current_app.config.get(window_seconds, window_seconds) if isinstance(window_seconds, str) else window_seconds

            remote_addr = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")
            bucket_key = f"{key_prefix}:{remote_addr}"
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window)
            bucket = _RATE_LIMIT_STORAGE[bucket_key]

            while bucket and bucket[0] < window_start:
                bucket.popleft()

            if len(bucket) >= max_allowed:
                return jsonify({"error": "Trop de requêtes, réessayez plus tard"}), 429

            bucket.append(now)
            return view(*args, **kwargs)

        return wrapped

    return decorator
