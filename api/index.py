"""
Vercel Serverless Function for Video Creator Agent
"""
from agent import run_agent

def handler(request):
    """Vercel serverless function handler"""
    from http.server import BaseHTTPRequestHandler
    from io import BytesIO

    class Handler(BaseHTTPRequestHandler):
        def __init__(self, request_text, response):
            self.rfile = BytesIO(request_text)
            self.wfile = BytesIO()
            self.response = response

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            import json
            data = json.loads(post_data)
            message = data.get('message', '')

            # Run agent
            result = run_agent(message)

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'result': result}).encode())

    # Parse request
    import json
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method not allowed'}

    try:
        body = json.loads(request.body)
        message = body.get('message', '')

        if not message:
            return {'statusCode': 400, 'body': 'Missing message'}

        # Run agent
        result = run_agent(message)

        return {
            'statusCode': 200,
            'body': json.dumps({'result': result}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
