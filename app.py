from flask import Flask, render_template, request, flash, session
import os, uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def exists(secret_id):
    path = f'{os.getcwd()}/templates/{secret_id}.html'
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.readlines()[0]
    else:
        return False

def create_secret(secret_id, secret):

    template = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1 style="text-align: center; color: black;">Secret: {secret}</h1>
    </body>
    </html>'''

    try:
        path = f'{os.getcwd()}/templates/{secret_id}.html'
        with open(path, 'w') as f:
            f.write(template) 
        return True
    except Exception as e:
        return e

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        secret = request.form['secret']
        pin = request.form['pin'] # not yet in use
        secret_id = uuid.uuid4()

        create = create_secret(secret_id, secret)
        if create == True:
            url = f'{request.url}{secret_id}'
            return render_template('index.html', url=url)
        else:
            flash(create)
            return render_template('index.html', url='')
    else:
        return render_template('index.html', url='')

@app.route('/<secret_id>')
def reveal(secret_id):
    if exists(secret_id) != False:
        if 'viewed' in session:
            os.remove(f'os.getcwd()/templates/{secret_id}.html')
            return render_template('404.html')
        else:
            session['viewed'] = True
            return render_template(f'{secret_id}.html')
    else:
        return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)