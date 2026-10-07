import http.server
import socketserver
import json
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class BirthdayHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'running', 'server': 'birthday-server'}).encode('utf-8'))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path in ('/api/save', '/save'):
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_length)
                data = json.loads(post_body.decode('utf-8'))

                json_path = os.path.join(DIRECTORY, 'content.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write('\n')

                js_path = os.path.join(DIRECTORY, 'content.js')
                with open(js_path, 'w', encoding='utf-8') as f:
                    f.write('window.SITE_CONTENT = ')
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write(';\n')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'message': 'تم حفظ الملفات بنجاح في المجلد'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode('utf-8'))
            return
        
        self.send_response(404)
        self.end_headers()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BirthdayHandler) as httpd:
        print(f"====================================================")
        print(f" خادم موقع عيد الميلاد يعمل بنجاح!")
        print(f" الموقع: http://localhost:{PORT}/index.html")
        print(f" لوحة التحكم: http://localhost:{PORT}/admin.html")
        print(f"====================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nتم إيقاف الخادم.")

if __name__ == '__main__':
    run()
