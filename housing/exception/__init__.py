import os 
import sys 
from housing.logger import logging
class HousingException(Exception):
    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail)
    
    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        
        """
        error_message:Exception obj
        error_detail:obj of sys module
        """
        _,_,exec_tb=error_detail.exc_info()

        line_number=exec_tb.tb_frame.f_lineno
        file_name=exec_tb.tb_frame.f_code.co_filename

        error_message=f"error occured in script:[{file_name}] at linenumber [{line_number}] error message: [{error_message}]]"



        return error_message
    
    def __str__(self):
        return self.error_message
    
    def __repr__(self):
        return HousingException.__name__.str()
    
if __name__=='__main__':
    try:
         a=5
         b=0
         a/b
    except Exception as e:
        print('division by zero')
        raise HousingException(e,sys)


