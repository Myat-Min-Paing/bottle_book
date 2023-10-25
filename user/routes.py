from bottle import Bottle, \
    jinja2_template as template, \
        static_file, request, redirect
from bottle import response
from utils.session import Session

app = Bottle()
sess = Session()
app_sess = sess.create_session(app)

@app.get('/static/<filePath:path>')
def static(filePath):
    return static_file(filePath, root='./static')

@app.route('/test')
def test():
    aaa = request.query.test
    return aaa