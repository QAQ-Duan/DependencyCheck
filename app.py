
from flask import Flask, redirect,  url_for, request, render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload():
    
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return redirect(url_for('result',file=f.filename))
    
@app.route('/result',methods=['GET'])
def result():
    file=request.args.get('file')
    with open(file,'r',encoding='utf-8')as g:
        content=g.read()
    return render_template("result.html",content=content)

if __name__ == '__main__':
    app.run(debug=True,port=5678)
