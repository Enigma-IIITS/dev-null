# EEEEEEEEEEEEEEEEEEEEEE                    iiii                                                                
# E::::::::::::::::::::E                   i::::i                                                               
# E::::::::::::::::::::E                    iiii                                                                
# EE::::::EEEEEEEEE::::E                                                                                        
#   E:::::E       EEEEEEnnnn  nnnnnnnn    iiiiiii    ggggggggg   ggggg   mmmmmmm    mmmmmmm     aaaaaaaaaaaaa   
#   E:::::E             n:::nn::::::::nn  i:::::i   g:::::::::ggg::::g mm:::::::m  m:::::::mm   a::::::::::::a  
#   E::::::EEEEEEEEEE   n::::::::::::::nn  i::::i  g:::::::::::::::::gm::::::::::mm::::::::::m  aaaaaaaaa:::::a 
#   E:::::::::::::::E   nn:::::::::::::::n i::::i g::::::ggggg::::::ggm::::::::::::::::::::::m           a::::a 
#   E:::::::::::::::E     n:::::nnnn:::::n i::::i g:::::g     g:::::g m:::::mmm::::::mmm:::::m    aaaaaaa:::::a 
#   E::::::EEEEEEEEEE     n::::n    n::::n i::::i g:::::g     g:::::g m::::m   m::::m   m::::m  aa::::::::::::a 
#   E:::::E               n::::n    n::::n i::::i g:::::g     g:::::g m::::m   m::::m   m::::m a::::aaaa::::::a 
#   E:::::E       EEEEEE  n::::n    n::::n i::::i g::::::g    g:::::g m::::m   m::::m   m::::ma::::a    a:::::a 
# EE::::::EEEEEEEE:::::E  n::::n    n::::ni::::::ig:::::::ggggg:::::g m::::m   m::::m   m::::ma::::a    a:::::a 
# E::::::::::::::::::::E  n::::n    n::::ni::::::i g::::::::::::::::g m::::m   m::::m   m::::ma:::::aaaa::::::a 
# E::::::::::::::::::::E  n::::n    n::::ni::::::i  gg::::::::::::::g m::::m   m::::m   m::::m a::::::::::aa:::a
# EEEEEEEEEEEEEEEEEEEEEE  nnnnnn    nnnnnniiiiiiii    gggggggg::::::g mmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaa
#                                                             g:::::g                                           
#                                                 gggggg      g:::::g                                           
#                                                 g:::::gg   gg:::::g                                           
#                                                  g::::::ggg:::::::g                                           
#                                                   gg:::::::::::::g                                            
#                                                     ggg::::::ggg                                              
#                                                        gggggg                                                 

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


typing("ENIGMA{FLAG_1")
