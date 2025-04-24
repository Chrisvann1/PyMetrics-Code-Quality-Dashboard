import pytest
from api import cyclomatic_score, documentation_score, code_style_score


#Just type "pytest" in terminal to run


#This document just provides some basic testing to 
#make sure the application works as planned


#The output should be a perfect score for cyclomatic
def test_cyclomatic_positive(): 
    test = """
def stuff(): 
    return 1
    """

    score = cyclomatic_score(test) 
    assert score == 100


#should output a bad score
def test_cyclomatic_negative(): 
    test = """
def stuff(): 
    for i in range(5):
        for i in range(5):
            for i in range(5):
                for i in range(5):
                    for i in range(5):
                        for i in range(5):
                            for i in range(5):
                                for i in range(5):
                                    for i in range(5):
                                        for i in range(5):
                                            for i in range(5):
                                                for i in range(5):
                                                    for i in range(5):
                                                        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5):
        pass
    for i in range(5): 
        pass 
    for i in range(5): 
        pass 
    for i in range(5): 
        pass
    """

    score = cyclomatic_score(test) 
    assert score < 30


#makes sure code is well documented
def test_documentation_positive(): 
    test = """
def add(x,y): 
    #This code is used to add numbers
    #x and y being variables
    return x + y
"""
    score = documentation_score(test) 
    assert score == 100

#checks for poor documentation
def test_documentation_negative(): 
    test = """
def stuff(): 
    return 1
"""
    score = documentation_score(test) 
    assert score == 0


#Checks for positive code style 
def test_code_style_positive(): 
    test = "def stuff():\n    return 1\n\n\n"

    score = code_style_score(test)
    assert score == 100


#Checks for negative code style
def test_code_style_negative(): 
    test = "def stuff():\nreturn 1\n\n\n"

    score = code_style_score(test)
    assert score != 100