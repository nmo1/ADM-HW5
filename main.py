# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 21:28:45 2019

@author: Giorgio
"""
import func_1
import func_2
import func_3
import func_4

def main(i):
    if i == 1:
        func_1.main()
    if i == 2:
        func_2.find_smartest()
    if i == 3:
        func_3.main()
    if i == 4:
        func_4.main()

main()       #choose between 1,2,3,4(Ex: main(1)) and read the code. In the 3th and 4th function you neet to insert the
            # input
