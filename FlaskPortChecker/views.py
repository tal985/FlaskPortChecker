import os
import subprocess 

from datetime import datetime
from flask import render_template, request, send_from_directory, flash
from FlaskPortChecker import app

"""Renders the icon."""
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

"""Renders the home page."""
@app.route('/', methods = ['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        status = nmapScan(ip, port)
        flash(ip + ':' + port + ' is ' + status + '.')

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

"""Renders the contact page."""
@app.route('/contact')
def contact():
    
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='How to reach me.'
    )

"""Renders the about page."""
@app.route('/about')
def about():
    
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='A Basic Portchecker'
    )

"""Wrapper function for using nmap."""
def nmapScan(ip, port):
    
    status = subprocess.run('nmap ' + ip + ' -p ' + port, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')

    if 'open' in status and 'filtered' not in status:
        status = 'open'
    elif 'closed' in status:
        status = 'closed'
    else:
        status = 'filtered'

    return status