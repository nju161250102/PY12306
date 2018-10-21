# coding=utf-8
import sqlite3


conn = sqlite3.connect('train.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS rail;")
c.execute('''
CREATE TABLE rail (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT DEFAULT NULL,
  lineNum INTEGER DEFAULT NULL,
  speed TEXT DEFAULT NULL,
  elec TEXT DEFAULT NULL,
  service TEXT DEFAULT NULL,
  type  TEXT DEFAULT NULL);
''')
c.execute("DROP TABLE IF EXISTS station;")
c.execute('''
CREATE TABLE station (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT DEFAULT NULL,
  teleCode TEXT DEFAULT NULL,
  pinyinCode TEXT DEFAULT NULL,
  location TEXT DEFAULT NULL,
  bureau TEXT DEFAULT NULL,
  service  TEXT DEFAULT NULL);
''')
c.execute("DROP TABLE IF EXISTS rs_relation;")
c.execute('''
CREATE TABLE rs_relation (
  rid INTEGER NOT NULL,
  sid INTEGER NOT NULL,
  mileage INTEGER DEFAULT NULL,
  PRIMARY KEY (rid, sid));
''')
