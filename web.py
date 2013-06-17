#coding=utf-8
import os
from functools import partial

from pesto import DispatcherApp, Response
from pesto.wsgiutils import serve_static_file
from pesto.wsgiutils import normpath as wsgi_normpath

from lxml.etree import tostring
import lxml.html

import zipfile
import StringIO

import blogbus
import os.path

import webmail
app = DispatcherApp()

thisdir = os.path.dirname(__file__)
staticdir = os.path.join(thisdir, 'static')
staticpath = partial(os.path.join, staticdir)


@app.match('/b2w', 'GET')
def b2w(request):
    blogname=request.form.get('blogname')
    email=request.form.get('email')
    xml=blogbus.blogbus2wordpress(blogname)

    if(xml==''):
        return Response("无法获取相关数据，有问题请发邮件enginespot@gmail.com",'200 OK')

    o=StringIO.StringIO()
    if os.path.isfile('temp.zip'):
        os.remove("temp.zip")

    zf=zipfile.ZipFile("temp.zip",'w',zipfile.ZIP_DEFLATED,False)
#    zf.writestr(xml)
    zf.writestr(blogname+'.xml',xml)
#    for zfile in zf.filelist:
#        zfile.create_system = 0
    zf.close()
    subject='附件符合wordpress导入标准，只需要导入此附件即可，有任何问题，请联系enginespot@gmail.com'
    webmail.send_mail(email,subject,['temp.zip'])
#    with open("temp.zip", 'rb') as f:
#        return Response(f.read(),"200 OK",[('Content-Type', 'octet-stream'),('Content-disposition','attachment; filename='+blogname+'.zip')])

#    return Response(xml,"200 OK",[('Content-Type', 'text/xml')])
    return Response("succeed!",'200 OK')


@app.match('<path:path>', 'POST')
def aaa():
    a=10


@app.match('<path:path>', 'GET')
def staticpages(request, path):
    serve_file = partial(serve_static_file, request, default_charset='utf-8')
    path = wsgi_normpath(path)

    while path and path[0] == '/':
        path = path[1:]

    # Special case for root page
    if path == '':
        path = 'index.html'

    fs_path = os.path.join(*path.split('/'))
    abs_path = staticpath(fs_path)

    response = serve_file(abs_path)
    if response.status_code == 404 and os.path.isdir(abs_path):
        if path != "" and not path.endswith('/'):
            redirect = '/' + path + '/'
            if request.script_name != '':
                redirect = request.script_name + redirect
            return Response.redirect(redirect, status=302)

        return serve_file(os.path.join(abs_path, 'index.html'))

    return response
