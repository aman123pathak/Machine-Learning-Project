import sys
#from logger import logging

def error_message_detail(error, error_detail):
    try:
        _, _, exc_tb = error_detail.exc_info()
        
        if exc_tb is None :
            return f"Error message: {str(error)}"
        
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = (
            "Error occurred in Python script "
            f"[{file_name}] at line number [{line_number}]: "
            f"{str(error)}"
        )
        return error_message
    
    except Exception:
        return f"Error message: {str(error)}"

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
        
    def __str__(self):
           return self.error_message
       
'''
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by Zero error")
        raise CustomException(e, sys)
'''  
        
        
        
        