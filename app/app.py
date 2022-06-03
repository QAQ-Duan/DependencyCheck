import os
import re
import rarfile
import zipfile
import tarfile
import gzip
from flask import Flask, redirect,  url_for, request, render_template, flash
from werkzeug.utils import secure_filename
from scannerPackages import Scanner
from pathlib import Path
import parse_CVE
from Utils import package_license,license_detail

def isver(ver):
    if type(ver)!=type(''):
        return False
    elif len(ver)==0:
        return False
    else:
        return ver[0]<='9' and ver[0]>='0'

class IgnoreCaseDict(dict):
    
    def lower_key(self, key):
        if isinstance(key, str):
            return key.lower()
        return key

    def __setitem__(self, key, value):
        super().__setitem__(self.lower_key(key), value)

    def __getitem__(self, item):
        return super().__getitem__(self.lower_key(item))

    def __delitem__(self, key):
        super().__delitem__(self.lower_key(key))

    def update(self, another=None, **F):
        for key, value in another.items():
            self.__setitem__(key, value)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"
    
base='C:/Users/Administrator.DESKTOP-B75U3IK/Desktop/作品赛/'
save_route='C:/Users/Administrator.DESKTOP-B75U3IK/Desktop/作品赛/saver/'
app = Flask(__name__)
versions=IgnoreCaseDict()
license_dict=dict()
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
                try:
                    with open(filepath,'r',encoding='utf-8')as f:
                        vers=f.readlines()
                except:
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
        global license_dict
        license_dict=dict()
        for i in contents:
            pack=i
            ver=versions.get(pack)
            if ver==None:
                if i=='bs4':
                    ver=versions.get("beautifulsoup4")
                    pack='beautifulsoup4'
                elif i=='PIL':
                    ver=versions.get("pillow")
                    if ver!=None:
                        pack='pillow'
                elif i=='cv2':
                    ver=versions.get("opencv_python")
                    pack='opencv'
            tmp_dict={'name':None,'version':None,'license_expression':'','licenses_summary':'[]'}
            t1=package_license([(pack,ver)])
            if len(t1):
                t2=t1[0]
                if len(t2):
                    tmp_dict=t2[0]
            package_lic=tmp_dict
            lic_ver=package_lic['version']
            if ver==None and isver(lic_ver):
                ver=lic_ver
            license_dict[pack]=package_lic
            versions[pack]=ver
            packages.append((pack,ver))
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
    return render_template("licenses.html")

@app.route('/license',methods=['GET'])
def license():
    file=request.args.get("file")
    pack=request.args.get('pack')
    ver=versions.get(pack)
    checklst=[]
    flag_for_license=(license_dict[pack]['license_expression']!='')
    license_summary=eval(license_dict[pack]['licenses_summary'])
    length=len(license_summary)
    counter=list(range(length))
    for diction in license_summary:
        checklst.append(diction['key'])
    detail=license_detail(checklst)
    return render_template("license.html",pack=pack,ver=ver,counter=counter,flag=flag_for_license,detail=detail,summary=license_summary,file=file)

@app.route('/cve',methods=['GET'])
def cve():
    file=request.args.get("file")
    pack=request.args.get('pack')
    ver=versions.get(pack)
    packs=[(pack,ver)]
    cve_dict=parse_CVE.parse_CVE(packs)
    has_vul=dict()
    for pack in packs:
        if(len(cve_dict[pack[0]])):
            has_vul[pack[0]]=True
    return render_template("cves.html",packs=packs,has_vul=has_vul,holes=cve_dict,file=file)

@app.route('/cves',methods=['GET'])
def cves():
    file=request.args.get("file")
    cve_dict = parse_CVE.parse_CVE(packages)
    has_vul=dict()
    for pack in packages:
        if(len(cve_dict[pack[0]])):
            has_vul[pack[0]]=True
    return render_template("cves.html",packs=packages,has_vul=has_vul,holes=cve_dict,file=file)

if __name__ == '__main__':
    app.run(debug=True,port=5678)
