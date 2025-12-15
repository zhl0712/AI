import http.server
from http.server import BaseHTTPRequestHandler
import json
import logging
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import threading

HOST = '0.0.0.0'
PORT = 3001

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('http_server.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('HTTP_SERVER')

class RequestHandler(BaseHTTPRequestHandler):
    # 支持CORS
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, HEAD, PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
    
    # 解析查询参数
    def _parse_query_params(self):
        if '?' in self.path:
            path, query_string = self.path.split('?', 1)
            return urllib.parse.parse_qs(query_string)
        return {}
    
    # 解析请求体
    def _parse_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            content_type = self.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                try:
                    return json.loads(body.decode('utf-8'))
                except json.JSONDecodeError:
                    logger.error('Invalid JSON format in request body')
                    return None
            elif 'application/x-www-form-urlencoded' in content_type:
                return urllib.parse.parse_qs(body.decode('utf-8'))
            else:
                # 返回原始字符串
                return body.decode('utf-8')
        return None
    
    # 发送JSON响应
    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    # 发送文本响应
    def _send_text_response(self, status_code, message):
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
    
    # 统一请求处理
    def handle_request(self):
        try:
            # 解析请求信息
            query_params = self._parse_query_params()
            body = self._parse_body()
            
            # 记录请求信息
            logger.info(f"Request: {self.command} {self.path}")
            logger.info(f"Headers: {dict(self.headers)}")
            if query_params:
                logger.info(f"Query Params: {query_params}")
            if body is not None:
                logger.info(f"Body: {body}")
            
            # 处理OPTIONS请求
            if self.command == 'OPTIONS':
                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                return
            
            # 这里可以添加路由处理逻辑
            # 示例：根据路径返回不同响应
            if self.path == '/health':
                self._send_json_response(200, {
                    'status': 'ok',
                    'message': 'Server is running',
                    'timestamp': threading.current_thread().name
                })
            elif self.path.startswith('/api'):
                self._send_json_response(200, {
                    'status': 'success',
                    'method': self.command,
                    'path': self.path,
                    'query_params': query_params,
                    'body': body
                })
            else:
                self._send_text_response(200, f"Request received: {self.command} {self.path}\n")
                
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            self._send_text_response(500, f'Internal Server Error: {str(e)}\n')
    
    # 禁用默认日志输出
    def log_message(self, format, *args):
        pass
    
    # 支持常见HTTP方法
    def do_GET(self):
        self.handle_request()
    
    def do_POST(self):
        self.handle_request()
    
    def do_PUT(self):
        self.handle_request()
    
    def do_DELETE(self):
        self.handle_request()
    
    def do_HEAD(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_PATCH(self):
        self.handle_request()
    
    def do_OPTIONS(self):
        self.handle_request()

# 多线程HTTP服务器
class ThreadedHTTPServer(http.server.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, max_workers=10):
        super().__init__(server_address, RequestHandlerClass)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def process_request(self, request, client_address):
        self.executor.submit(self._process_request_thread, request, client_address)

    def _process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

if __name__ == '__main__':
    try:
        server = ThreadedHTTPServer((HOST, PORT), RequestHandler, max_workers=20)
        logger.info(f"Server running at http://{HOST}:{PORT}/")
        logger.info(f"Using {server.executor._max_workers} worker threads")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server is shutting down...")
        server.executor.shutdown(wait=True)
        server.server_close()
        logger.info("Server has been shut down successfully")
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}", exc_info=True)
