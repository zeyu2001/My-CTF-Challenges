from flask import Flask, redirect

app = Flask(__name__)

i = 0

@app.route('/')
def index():
    global i

    if i == 0:
        i += 1
        return 'Nothing to see here'

    else:
        return redirect('http://localhost/flag')


if __name__ == '__main__':
    app.run()