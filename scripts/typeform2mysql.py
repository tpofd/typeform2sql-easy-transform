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
questions_dict = forms.get(form_id)
questions_ids = []

db_cursor.execute('drop table if exists questions_dictionary')
db_cursor.execute('create table questions_dictionary (id VARCHAR(255), question_title VARCHAR(255), question_type VARCHAR(255))')

for i in range(len(questions_dict['fields'])):
    question_insert_query = 'insert into questions_dictionary (id, question_title, question_type) values ("{0}", "{1}", "{2}")'.format(
        questions_dict['fields'][i]['id'],
        questions_dict['fields'][i]['title'],
        questions_dict['fields'][i]['type']
    )
    questions_ids.append(questions_dict['fields'][i]['id'])
    db_cursor.execute(question_insert_query)

db_connection.commit()

# create responses table
responses = Typeform(api_key).responses
responses_dict = responses.list(form_id)

db_cursor.execute('drop table if exists responses')
create_response_table_query = 'create table responses (response_id VARCHAR(255)'
for i in range(len(questions_ids)):
    create_response_table_query += ', {0} VARCHAR(255)'.format(questions_ids[i])
create_response_table_query += ')'
db_cursor.execute(create_response_table_query)

for i in range(len(responses_dict['items'])):
    insert_part_query = 'insert into responses (response_id'
    values_part_query = 'values ("{0}"'.format(responses_dict['items'][i]['response_id'])
    for j in range(len(responses_dict['items'][i]['answers'])):
        if (responses_dict['items'][i]['answers'][j]['type'] == 'choice'):
            insert_part_query += ', {}'.format(responses_dict['items'][i]['answers'][j]['field']['id'])
            values_part_query += ', "{}"'.format(responses_dict['items'][i]['answers'][j]['choice']['label'])
    responses_all_insert_query = insert_part_query + ')' + values_part_query + ')'
    db_cursor.execute(responses_all_insert_query)
db_connection.commit()