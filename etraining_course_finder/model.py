#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser

import sys, os
import json, sqlite3
from functools import wraps

import datetime

class CourseOperation(object):
  '''
  etraining-course-finder model
  1. insert/get method for sqlite3
  2. input/output method for json
  '''
  def __init__(self, keep_alive=False):
    package_root = os.path.dirname(__file__)
    self.json_path = os.path.join(package_root, 'course.json')
    self.db_path = os.path.join(package_root, 'course.db')
    self.keep_alive = keep_alive
    self.conn = None
    self.cur = None

  def run(self):
    now = datetime.datetime.now()
    if os.path.exists(self.db_path):
      dataset = parser.run(now.month-1, 12)
      self.update_course(dataset)
      self.output_json_file(dataset)
    else:
      dataset = parser.run(now.month-1, 12)
      self.create_course_table()
      self.insert_course(dataset)
      self.output_json_file(dataset)
    pass

  # decorator
  def within_db_transaction(method):
    @wraps(method)
    def method_wrapper(self, *args, **kargs):
      if not self.keep_alive or self.conn is None:
        self.conn = sqlite3.connect(self.db_path)
        if 'get' in method.__name__:
          self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
      try:
        retval = method(self, *args, **kargs)
      except:
        self.conn.rollback()
        raise
      else:
        self.conn.commit()
      finally:
        self.cur.close()
        if not self.keep_alive:
          self.conn.close()
      return retval
    return method_wrapper

  @within_db_transaction
  def create_course_table(self):
    self.cur.execute('DROP TABLE IF EXISTS course')
    self.cur.execute('''
      CREATE TABLE course (
        id INT,
        city TEXT,
        name TEXT,
        sponsor TEXT,
        register TEXT,
        applying DATETIME,
        opening DATE,
        ending DATE,
        primary key (id)
      )
    ''')
    pass

  @within_db_transaction
  def insert_course(self, dataset):
    for key, val in dataset.items():
      self.cur.execute('INSERT or IGNORE INTO course VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (key, val['city'], val['name'], val['sponsor'], val['register'], val['applying'], val['opening'], val['ending'],))

  @within_db_transaction
  def update_course(self, dataset):
    for key, val in dataset.items():
      self.cur.execute('UPDATE course SET city=?, name=?, sponsor=?, register=?, applying=?, opening=?, ending=? WHERE id=?', (val['city'], val['name'], val['sponsor'], val['register'], val['applying'], val['opening'], val['ending'], key,))

  @within_db_transaction
  def get_course_by_query(self, query):
    q = '%'+query+'%'
    self.cur.execute('SELECT * FROM course WHERE city LIKE ? OR name LIKE ? OR sponsor LIKE ? ORDER BY datetime(applying) ASC', (q, q, q,))
    return self.cur.fetchall()

  def output_json_file(self, dataset):
    try:
      # fix json escape issue in Python2.7.*
      if sys.version_info.major == 2:
        dataset = json.loads(json.dumps(dataset), object_hook=json_convert)
    except Exception as e:
      print(e)
      print("Your Python version could so old")
      print("Please upgrade to 2.7.* or 3.3.*")
      raise
    with open(self.json_path, 'w') as fp:
      json.dump(dataset, fp, ensure_ascii=False)
    pass

  def input_json_file(self):
    dataset = {}
    try:
      with open(self.json_path, 'r') as fp:
        dataset = json.load(fp)
    except Exception as e:
      pass
    return dataset

# json.loads(res, object_hook=json_convert)
def json_convert(input):
  '''
  json_convert fix json escape issue in Python2.7.*
  '''
  if isinstance(input, dict):
    return {json_convert(key): json_convert(value) for key, value in input.iteritems()}
  elif isinstance(input, list):
    return [json_convert(element) for element in input]
  elif isinstance(input, unicode):
    return input.encode('utf-8')
  else:
    return input

def main():
  co = CourseOperation()
  co.run()

if __name__ == '__main__':
  main()
