import os
import rarfile
import zipfile
import tarfile
import gzip
from flask import Flask, redirect,  url_for, request, render_template, flash
from werkzeug.utils import secure_filename
from Scanner import Scanner
base='C:/Users/Administrator.DESKTOP-B75U3IK/Desktop/作品赛/'
save_route='C:/Users/Administrator.DESKTOP-B75U3IK/Desktop/作品赛/saver/'
app = Flask(__name__)
def unrar(path,route):
    if path.endswith('.rar'):
        z=rarfile.RarFile(path)
    elif path.endswith('.zip'):
        z=zipfile.ZipFile(path)
    z.extractall(route)
    z.close()
    

def prosrar(full_path,save_route):
    contents=list()
    unrar(full_path,save_route)
    for root,dirs, files in os.walk(save_route):
        for name in files:
            if name.endswith('.py'):
                filepath=os.path.join(root,name)
                modlist=Scanner(filepath).findPackage()
                for i in modlist:
                    contents.append(i)
        for name in files:
            os.remove(os.path.join(root,name))
    contents=list(set(contents))
    return contents

@app.route('/')
def upload():
    
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        fname=secure_filename(f.filename)
        save_path=os.path.join(save_route,fname)
        f.save(save_path)
        return redirect(url_for('result',file=fname))
    
@app.route('/result',methods=['GET'])
def result():
    file=request.args.get('file')
    full_path=os.path.join(save_route,file)
    if full_path.endswith('.rar') or full_path.endswith('.zip'):
        contents=prosrar(full_path,save_route)
    elif full_path.endswith('.py'):
        contents=Scanner(full_path).findPackage()
    else:
        with open(full_path,'r',encoding='utf-8') as g:
            contents=[g.read()]
    return render_template("result.html",contents=contents)

if __name__ == '__main__':
    app.run(debug=True,port=5678)