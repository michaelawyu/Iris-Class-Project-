#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://project:6156@localhost/Iris"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#


@app.route('/message', methods = ['GET','POST'])
def test():
    print request.form
    return 'Test Message'

@app.route('/', methods = ['POST'])
def index():
    """
    request is a special object that Flask provides to access web request information:
        
    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2
        
    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
        """
            
    def list2string(newList):
        result = ''
        for i in newList:
            result = result + ';' + str(i)
        return result[1:]
    
            
    # DEBUG: this is debugging code to see what request looks like
    #print request.args
                
                
    #
    # example of a database query
    #
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





#@app.route('/', methods = ['GET'])
#def index():
#  """
#  request is a special object that Flask provides to access web request information:
#
#  request.method:   "GET" or "POST"
#  request.form:     if the browser submitted a form, this contains the data in the form
#  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2
#
#  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
#  """
#  
#
#
#
#
#  # DEBUG: this is debugging code to see what request looks like
#  print request.args
#
#
#  #
#  # example of a database query
#  #
#  cursor = g.conn.execute("select post_title from posts where product_id = 1")
#  names = []
#
#  for result in cursor:
#    print result[0]
#    names.append(result[0])  # can also be accessed using result[0]
#  cursor.close()
#
#  return str(names)
#




  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
#  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
#  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
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
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
