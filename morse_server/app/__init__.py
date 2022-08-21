# This has to be in a certain order - routes after app - and Code is reformatting it wrong. Use vi.

from flask import Flask

app = Flask(__name__)

from app import routes

