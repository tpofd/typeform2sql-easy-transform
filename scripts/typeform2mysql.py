from typeform import Typeform
import mysql.connector

api_key = '{PASTE YOUR API KEY HERE}'
form_id = '{PASTE YOUR FORM ID HERE}'
user = '{PASTE YOUR DATABASE USER HERE}'
password = '{PASTE YOUR DATABASE PASSWORD HERE}'
host = '{PASTE YOUR HOST HERE}'
database = '{PASTE NAME OF YOUR DATABASE HERE}'

# connect to database
db_connection = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    database=database
)
db_cursor = db_connection.cursor()

# create questions dictionary table
forms = Typeform(api_key).forms
result = forms.get(form_id)

db_cursor.execute('drop table if exists questions_dictionary')
db_cursor.execute('create table questions_dictionary (id VARCHAR(255), title VARCHAR(255))')

for i in range(len(result['fields'])):
    question_insert_query = 'insert into questions_dictionary (id, title) values ("{0}", "{1}")'.format(
        result['fields'][i]['id'],
        result['fields'][i]['title']
    )
    db_cursor.execute(question_insert_query)

db_connection.commit()