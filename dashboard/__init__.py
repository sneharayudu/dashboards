from flask import Flask


app = Flask('dashboard')
app.secret_key = 'some_key'

from dashboard import api
