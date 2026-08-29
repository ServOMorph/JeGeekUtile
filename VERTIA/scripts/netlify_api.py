#!/usr/bin/env python3
"""Client REST minimal pour l'API Netlify v1."""

import argparse
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


API_ROOT = "https://api.netlify.com/api/v1/"


def load_token(project_root):
    token = os.environ.get("NETLIFY_AUTH_TOKEN")
    if token:
        return token
    env_file = project_root / ".env.netlify"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == "NETLIFY_AUTH_TOKEN":
                return value.strip().strip('"').strip("'")
    return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Route API, par exemple /sites")
    parser.add_argument("--method", default="GET")
    parser.add_argument("--data")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    token = load_token(project_root)
    if not token:
        parser.error("NETLIFY_AUTH_TOKEN est requis.")

    body = args.data.encode("utf-8") if args.data else None
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if body:
        headers["Content-Type"] = "application/json"
    request = Request(urljoin(API_ROOT, args.path.lstrip("/")), data=body, headers=headers, method=args.method.upper())
    try:
        with urlopen(request, timeout=60) as response:
            print(response.read().decode("utf-8"))
    except HTTPError as error:
        print(f"Netlify API HTTP {error.code}: {error.read().decode('utf-8', errors='replace')}")
        return 1
    except URLError as error:
        print(f"Appel Netlify impossible: {error.reason}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
