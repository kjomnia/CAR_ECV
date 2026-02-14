import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8000
DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class DataHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            plate_number = data.get('plateNumber', 'unknown').replace('/', '_').replace('\\', '_')
            file_path = os.path.join(DATA_DIR, f"{plate_number}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "success", "message": f"Saved to {file_path}"}
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/api/delete':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            plate_number = data.get('plateNumber', '').replace('/', '_').replace('\\', '_')
            file_path = os.path.join(DATA_DIR, f"{plate_number}.json")
            
            if os.path.exists(file_path):
                os.remove(file_path)
                status = "success"
            else:
                status = "not_found"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": status}).encode())

    def do_GET(self):
        if self.path == '/api/load-all':
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
            all_data = {"vehicles": [], "vehicleData": {}}
            
            for f_name in files:
                with open(os.path.join(DATA_DIR, f_name), 'r', encoding='utf-8') as f:
                    vehicle_pkg = json.load(f)
                    all_data["vehicles"].append(vehicle_pkg["vehicle"])
                    all_data["vehicleData"][vehicle_pkg["vehicle"]["id"]] = {"items": vehicle_pkg["items"]}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(all_data, ensure_ascii=False).encode())
        else:
            return super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"Serving at http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), DataHandler) as httpd:
    httpd.serve_forever()
