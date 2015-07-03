#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import CourseOperation

from flask import Flask, request, render_template
from flask import redirect, url_for

app = Flask(__name__)
app.config.from_envvar('publishconf.py')

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST' and request.form['query'] != '':
    return redirect(url_for('finder', query=request.form['query']))
  return render_template('base.html')

@app.route('/search/<query>')
def finder(query):
  co = CourseOperation()
  course_list = co.get_course_by_query(query)
  return render_template('finder.html', query=query, course_list=course_list)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=True)
