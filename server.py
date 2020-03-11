"""
This is the top-level starting script for a flask server app
"""

from flask import Flask, request
import json 
import DataAnalysis_GP

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='', 
            static_folder='gui/build')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        pass

if __name__ == "__main__":
    app.run()
