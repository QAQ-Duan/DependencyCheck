import os
import rarfile
import zipfile
import tarfile
import gzip
from flask import Flask, redirect,  url_for, request, render_template, flash
from werkzeug.utils import secure_filename
from scannerPackages import Scanner
from pathlib import Path
import parse_CVE
base='C:/Users/Administrator.DESKTOP-B75U3IK/Desktop/作品赛/'
save_route='C:/Users/Administrator.DESKTOP-B75U3IK/Desktop/作品赛/saver/'
app = Flask(__name__)
versions=dict()
def unrar(path,route):
    notgz=True
    if path.endswith('.rar'):
        z=rarfile.RarFile(path)
    elif path.endswith('.zip'):
        z=zipfile.ZipFile(path)
    elif path.endswith('.tar.gz') or path.endswith('.tar'):
        z=tarfile.open(path)
    elif path.endswith('.gz') and path.endswith('.tar.gz')==False:
        notgz=False
        z=gzip.GzipFile(path)
        f_name = path.replace(".gz", "")
        with open(f_name, "w+") as o:
            o.write(z.read())
        z.close()
    if notgz:
        z.extractall(route)
        z.close()

def prosrar(full_path,save_route):
    pyfiles=list()
    unrar(full_path,save_route)
    for root,dirs, files in os.walk(save_route):
        for name in files:
            if name.endswith('.py'):
                filepath=os.path.join(root,name)
                filepath= Path(filepath).as_posix()
                pyfiles.append(filepath)
            elif name=="requirements.txt":
                filepath=os.path.join(root,name)
                with open(filepath,'r',encoding='utf-16')as f:
                    vers=f.readlines()
                global versions
                for each in vers:
                    loc=each.find('==')
                    if loc<0:
                        continue
                    else:
                        package=each[0:loc]
                        Ver=each[loc+2:-1]
                        versions[package]=Ver
    return pyfiles

@app.route('/')
def upload():
    
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        for root,dirs, files in os.walk(save_route):
            for name in files:
                os.remove(os.path.join(root,name))
        fname=secure_filename(f.filename)
        save_path=os.path.join(save_route,fname)
        f.save(save_path)
        full_path=os.path.join(save_route,fname)
        if full_path.endswith('.rar') or full_path.endswith('.zip') or full_path.endswith('.gz') or full_path.endswith('.tar'):
            pyfiles=prosrar(full_path,save_route)
            contents=Scanner(pyfiles).scanFiles()[1]
        elif full_path.endswith('.py'):
            pyfiles=[full_path]
            contents=Scanner(pyfiles).scanFiles()[1]
        else:
            with open(full_path,'r',encoding='utf-8') as g:
                contents=[g.read()]
        global packages
        packages=list()
        for i in contents:
            packages.append((i,versions.get(i)))
        return redirect(url_for('result',file=fname))
    
@app.route('/result',methods=['GET'])
def result():
    file=request.args.get("file")
    for pack in packages:
        redirect(url_for('license',pack=pack[0]))
        redirect(url_for('cve',pack=pack[0]))
    return render_template("result.html",contents=packages,file=file)

@app.route('/licenses',methods=['GET'])
def licenses():
    file=request.args.get("file")
    return render_template("result.html",contents=packages,file=file)

@app.route('/license',methods=['GET'])
def license():
    file=request.args.get("file")
    pack=request.args.get('pack')
    ver=versions.get(pack)
    return render_template("result.html",contents=[(pack,ver)],file=file)

@app.route('/cve',methods=['GET'])
def cve():
    file=request.args.get("file")
    pack=request.args.get('pack')
    ver=versions.get(pack)
    packs=[(pack,ver)]
    cve_dict=parse_CVE.parse_CVE(packs)
    return render_template("cves.html",packs=packs,holes=cve_dict,file=file)

@app.route('/cves',methods=['GET'])
def cves():
    file=request.args.get("file")
    cve_dict = parse_CVE.parse_CVE(packages)
    return render_template("cves.html",packs=packages,holes=cve_dict,file=file)

if __name__ == '__main__':
    app.run(debug=True,port=5678)
