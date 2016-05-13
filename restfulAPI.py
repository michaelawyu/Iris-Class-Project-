#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://project:6156@localhost/Iris"


engine = create_engine(DATABASEURI)

@app.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):

  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/message', methods = ['GET','POST'])
def test():
    print request.form
    return 'Test Message'

@app.route('/', methods = ['POST'])
def index():

            
    def list2string(newList):
        result = ''
        for i in newList:
            result = result + ';' + str(i)
        return result[1:]
    
    print 1
    print request.form['username']
    cursor = g.conn.execute("select password from users where username = %s", request.form['username'])
    names = []
                        
    for result in cursor:
        print result[0]
        names.append(result[0])  # can also be accessed using result[0]
    cursor.close()

    print 2


    cursor2 = g.conn.execute("select dp.product_name from devs_products dp, signup, users where dp.product_id = signup.product_id and signup.user_id = users.user_id and users.username = %s", request.form['username'])
    names2 = []
    
    for result in cursor2:
        print result[0]
        names2.append(result[0])  # can also be accessed using result[0]
    cursor2.close()
    
    print 3
    
    cursor3 = g.conn.execute("select s.section_name from sections s, signup, users where users.user_id = signup. user_id and signup.product_id = s.product_id and users.username = %s", request.form['username'])
    names3 = []
    
    for result in cursor3:
        print result[0]
        names3.append(result[0])  # can also be accessed using result[0]
    cursor3.close()
    
    
    
    print 4
    
    cursor4 = g.conn.execute("select p.post_title from posts p, signup s, users where users.user_id = s.user_id and s.product_id = p.product_id and users.username = %s", request.form['username'])
    names4 = []
    
    for result in cursor4:
        print result[0]
        names4.append(result[0])  # can also be accessed using result[0]
    cursor4.close()
    
    cursor5 = g.conn.execute("select p.post_content from posts p, signup s, users where users.user_id = s.user_id and s.product_id = p.product_id and users.username = %s", request.form['username'])
    names5 = []
    
    for result in cursor5:
        print result[0]
        names5.append(result[0])  # can also be accessed using result[0]
    cursor5.close()


    cursor6 = g.conn.execute("select p.upvotes from posts p, signup s, users where users.user_id = s.user_id and s.product_id = p.product_id and users.username = %s", request.form['username'])
    names6 = []
    
    for result in cursor6:
        print result[0]
        names6.append(result[0])  # can also be accessed using result[0]
    cursor6.close()


    cursor7 = g.conn.execute("select p.downvotes from posts p, signup s, users where users.user_id = s.user_id and s.product_id = p.product_id and users.username = %s", request.form['username'])
    names7 = []
    
    for result in cursor7:
        print result[0]
        names7.append(result[0])  # can also be accessed using result[0]
    cursor7.close()



    print 5

    s1 = 'ok'+ ';' + list2string(names2)
    print 8
    s2 = list2string(names3)
    s3 = list2string(names4)
    s4 = list2string(names5)
    s5 = list2string(names6)
    s6 = list2string(names7)
    s = s1+s2+s3+s4+s5+s6
    print 6

    print request.form.keys()
    print names[0]

    print 7
    if request.form['password'] == names[0]:
        
        return s
    else:
        
        return 'FAIL'


@app.route('/', methods = ['GET'])
def test2():

    try :
        newValue = request.form['countFor']
        g.conn.execute("update posts set upvotes = %s where post_content = %s",newValue, request.form['review'])
    except:
        pass
    try :
        newValue = request.form['countAgainst']
        g.conn.execute("update posts set downvotes = %s where post_content = %s",newValue, request.form['review'])
    except:
        pass

@app.route('/another')
def another():
  return render_template("another.html")


# Example of adding new data to the database

"""
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')
"""


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=5001, type=int)
  def run(debug, threaded, host, port):


    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
