from wsgiref.simple_server import make_server


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/templates')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print('Serving http on port 8000...')
    httpd.serve_forever()
