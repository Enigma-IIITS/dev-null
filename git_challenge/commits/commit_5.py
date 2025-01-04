#    ,ggggggg,                                                               
#  ,dP""""""Y8b                                                              
#  d8'    a  Y8                                                              
#  88     "Y8P'               gg                                             
#  `8baaaa                    ""                                             
# ,d8P""""      ,ggg,,ggg,    gg     ,gggg,gg   ,ggg,,ggg,,ggg,     ,gggg,gg 
# d8"          ,8" "8P" "8,   88    dP"  "Y8I  ,8" "8P" "8P" "8,   dP"  "Y8I 
# Y8,          I8   8I   8I   88   i8'    ,8I  I8   8I   8I   8I  i8'    ,8I 
# `Yba,,_____,,dP   8I   Yb,_,88,_,d8,   ,d8I ,dP   8I   8I   Yb,,d8,   ,d8b,
#   `"Y88888888P'   8I   `Y88P""Y8P"Y8888P"8888P'   8I   8I   `Y8P"Y8888P"`Y8
#                                        ,d8I'                               
#                                      ,dP'8I                                
#                                     ,8"  8I                                
#                                     I8   8I                                
#                                     `8, ,8I                                
#                                      `Y8P"                                 

import time


def typing(content: str):
    """
    Simulates a typing effect by printing characters one by one with a delay.

    Args:
        content (str): The text to display with the typing effect.

    Example:
        typing("Welcome! Are you here in search of the Flag? Best of luck!")

    This will print the text character by character with a slight pause, creating
    the effect of someone typing the message in real time.
    """
    for i in range(len(content)):
        print(f"\r{content[:i+1]}", end="")
        time.sleep(0.1)
    print("\n")


typing("FLAG_2}")
