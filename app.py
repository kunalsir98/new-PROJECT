from flask import Flask
from housing.logger import logging
import sys 
from housing.exception import HousingException

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home_page():
    try:
        raise Exception('this is my exception class')
    except Exception as e:
        housing=HousingException(e,sys)
        logging.info(housing.error_message)
        logging.info('this is my logging info')
    return 'this is our house prediction project'

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)