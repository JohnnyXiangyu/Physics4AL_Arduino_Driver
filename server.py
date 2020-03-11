"""
This is the top-level starting script for a flask server app
"""

from flask import Flask, request
import json
import devices

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='',
            static_folder='gui/build')


@app.route('/api/connect', methods=['POST'])
def connect():
    """
    construct device object using information provided in body Json, then connect
    """
    pass


@app.route('/api/start', methods=['POST'])
def start():
    """
    start a trial (with intention that there might be preparation before getting data)
    """
    pass


@app.route('/api/end', methods=['POST'])
def end():
    """
    finish a trial (free any allocated resource)
    """
    pass


@app.route('/api/getData', methods=['POST'])
def getData():
    """
    get all data lines in buffer, and flush them into stored data structure
    """
    pass


@app.route('/api/markEvent', methods=['POST'])
def markEvent():
    """
    mark the next coming line from 
    """
    pass


if __name__ == "__main__":
    app.run()
