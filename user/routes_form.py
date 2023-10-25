from bottle import Bottle, \
    jinja2_template as template, \
        static_file, request, redirect

from bottle import Bottle,response, TEMPLATE_PATH
import routes
from models import connection, Books
from utils.util import Utils
from utils.auth import Auth

app = routes.app
auth = Auth()

@app.route('/add', method=["GET", "POST"])
def add():
    auth.check_login()
    registId = ""
    form = {}
    kind = "登録"
    errorMsg = []
    if request.method == "GET":
        if request.query.get('id') is not None:
            book = connection.query(Books).filter(Books.id_ == request.query.get('id')).first()
            form['name'] = book.name
            form['volume'] = book.volume
            form['author'] = book.author
            form['publisher'] = book.publisher
            form['memo'] = book.memo
            registId = book.id_
            kind = '更新'
        if request.forms.get('next') == 'back':
            return template('list.html')
        return template('add.html',kind=kind, form=form, registId=registId)
    else:
        form = request.forms.dict
        if request.forms.getunicode('id') != '' and request.forms.getunicode('id') != '#':
            registId = request.forms.getunicode('id')
            form['id'] = request.forms.getunicode('id')
        else:
            registId = ''
            form['id'] = '#'
        form['name'] = request.forms.getunicode('name')
        form['volume'] = request.forms.getunicode('volume')
        form['author'] = request.forms.getunicode('author')
        form['publisher'] = request.forms.getunicode('publisher')
        form['memo'] = request.forms.getunicode('memo')
        errorMsg = Utils.validate(data=form)
        print(errorMsg)
        if request.forms.get('next') == 'back':
            return template('add.html', form=form, kind=kind,registId=registId)
                
        if errorMsg == []:
            headers = ["id", "書名", "巻数", "著者", "出版社", "メモ"]
            return template('confirm.html', form=form, headers=headers,registId=registId)
        else:
            return template('add.html', error=errorMsg, kind=kind, form=form, registId=registId)
            

@app.route('/regist', method=["POST"])
def regist():
    auth.check_login()
    form = request.forms.dict
    name = request.forms.decode().getunicode('name')
    volume = request.forms.decode().getunicode('volume')
    author = request.forms.decode().getunicode('author')
    publisher = request.forms.decode().getunicode('publisher')
    memo = request.forms.decode().getunicode('memo')
    if request.forms.decode().getunicode('id') == '#':
        registId = None
    else:
        registId = request.forms.decode().getunicode('id')
    
    if request.forms.decode().get('next') == 'back':
        response.status = 307
        response.set_header("Location", "/add")
        return response
    
    books = Books(
        id_ = registId,
        name = name,
        volume = volume,
        author = author,
        publisher = publisher,
        memo = memo,
        delFlg = False
    )
    if request.forms.get('next') == 'update': 
        connection.merge(books)
        connection.commit()
        connection.close()
    elif request.forms.get('next') == 'regist':
        connection.add(books)
        connection.commit()
        connection.close()
    elif request.forms.get('next') == 'back':
        return template('add.html', form=form, registId=registId)
    
    redirect('/list')
    

@app.route('/delete/<dataId>')
def delete(dataId):
    auth.check_login()
    book = connection.query(Books).filter(Books.id_==dataId).first()
    book.delFlg = True
    connection.commit()
    connection.close()
    redirect('/list')