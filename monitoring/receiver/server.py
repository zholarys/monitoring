import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length))
        for alert in payload.get("alerts", []):
            print(json.dumps({
                "status": alert["status"],
                "alert": alert["labels"].get("alertname"),
                "instance": alert["labels"].get("instance"),
                "summary": alert.get("annotations", {}).get("summary"),
            }, ensure_ascii=False), flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

print("Receiver listening on port 8080", flush=True)
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
