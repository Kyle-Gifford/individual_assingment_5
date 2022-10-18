# python version 3.9.7
# pip install -Iv flask==2.2.2
# pip install -Iv flask-mysqldb==1.0.1

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import sys



print(f'version running: {sys.version}')