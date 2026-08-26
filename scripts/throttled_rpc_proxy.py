#!/usr/bin/env python3
"""Serialize JSON-RPC calls to a heavily rate-limited upstream endpoint.

Foundry can issue several concurrent and batch requests while initializing a
fork. This proxy accepts those requests locally, splits batches, and forwards
one upstream request at a time with a configurable minimum interval.
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class UpstreamClient:
    def __init__(self, url: str, interval: float, retries: int, timeout: float) -> None:
        self.url = url
        self.interval = interval
        self.retries = retries
        self.timeout = timeout
        self._lock = threading.Lock()
        self._last_request_at = 0.0

    def call(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            for attempt in range(1, self.retries + 1):
                elapsed = time.monotonic() - self._last_request_at
                delay = self.interval - elapsed
                if delay > 0:
                    time.sleep(delay)

                body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
                request = urllib.request.Request(
                    self.url,
                    data=body,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "wintermute-alpha-ci-rpc-proxy/1.0",
                    },
                    method="POST",
                )

                method = payload.get("method", "<unknown>")
                request_id = payload.get("id")
                print(
                    f"upstream attempt={attempt} method={method} id={request_id}",
                    file=sys.stderr,
                    flush=True,
                )

                try:
                    with urllib.request.urlopen(request, timeout=self.timeout) as response:
                        raw = response.read()
                    self._last_request_at = time.monotonic()
                    decoded = json.loads(raw.decode("utf-8"))
                    if not isinstance(decoded, dict):
                        raise RuntimeError("upstream returned a non-object JSON-RPC response")
                    return decoded
                except urllib.error.HTTPError as exc:
                    self._last_request_at = time.monotonic()
                    error_body = exc.read().decode("utf-8", errors="replace")
                    print(
                        f"upstream HTTP {exc.code}: {error_body[:500]}",
                        file=sys.stderr,
                        flush=True,
                    )
                    if exc.code != 429 or attempt == self.retries:
                        raise RuntimeError(
                            f"upstream HTTP {exc.code}: {error_body[:500]}"
                        ) from exc
                    retry_after = exc.headers.get("Retry-After")
                    if retry_after:
                        try:
                            time.sleep(max(float(retry_after), self.interval))
                        except ValueError:
                            time.sleep(self.interval)
                except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                    self._last_request_at = time.monotonic()
                    print(f"upstream error: {exc}", file=sys.stderr, flush=True)
                    if attempt == self.retries:
                        raise RuntimeError(f"upstream request failed: {exc}") from exc
                    time.sleep(self.interval)

        raise RuntimeError("upstream request exhausted retries")


class RpcHandler(BaseHTTPRequestHandler):
    server_version = "ThrottledRpcProxy/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"proxy {self.address_string()} {fmt % args}", file=sys.stderr, flush=True)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self.send_error(404)
            return
        data = b"ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))

            client: UpstreamClient = self.server.upstream_client  # type: ignore[attr-defined]
            if isinstance(payload, list):
                if not payload:
                    raise ValueError("empty JSON-RPC batch")
                responses = []
                for item in payload:
                    if not isinstance(item, dict):
                        raise ValueError("JSON-RPC batch entries must be objects")
                    response = client.call(item)
                    # JSON-RPC notifications omit an id and require no response.
                    if "id" in item:
                        responses.append(response)
                result: Any = responses
            elif isinstance(payload, dict):
                result = client.call(payload)
            else:
                raise ValueError("JSON-RPC request must be an object or array")

            encoded = json.dumps(result, separators=(",", ":")).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
        except Exception as exc:  # noqa: BLE001
            print(f"proxy error: {exc}", file=sys.stderr, flush=True)
            error = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32098, "message": str(exc)},
            }
            encoded = json.dumps(error, separators=(",", ":")).encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8547)
    parser.add_argument("--interval", type=float, default=10.5)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=120.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.interval < 0:
        raise SystemExit("--interval must be non-negative")
    if args.retries < 1:
        raise SystemExit("--retries must be at least 1")

    server = ThreadingHTTPServer((args.host, args.port), RpcHandler)
    server.daemon_threads = True
    server.upstream_client = UpstreamClient(  # type: ignore[attr-defined]
        args.upstream,
        args.interval,
        args.retries,
        args.timeout,
    )
    print(
        f"proxy listening on http://{args.host}:{args.port}; "
        f"upstream={args.upstream}; interval={args.interval}s",
        file=sys.stderr,
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
