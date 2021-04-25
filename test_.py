import pytest
from dekoratory_zadania import greetings, is_palindrome, format_output, add_class_method, add_instance_method

def test_greetings():
    
    @greetings
    def show_greetings(blob):
        return blob

    assert show_greetings("jOE doe") == "Hello Joe Doe"
    
def test_palindrome():
    
    @is_palindrome
    def show_sentence():
        return "Eva, can I see bees in a cave?"

    assert show_sentence() == "Eva, can I see bees in a cave? - is palindrome"
    
def test_format_output():
    
    @format_output("first_name__last_name", "age")
    def first_func():
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "city": "Warszawa",
        }
        
    #assert first_func() == {"first_name__last_name": "Jan Kowalski", "city": "Warszawa"}
    with pytest.raises(ValueError):
        first_func()
        
def test_add_class_method():
    
    class A:
        pass
    
    @add_class_method(A)
    def foo():
        return "Hello!"
    
    assert A.foo() == "Hello!"
    
def test_add_instance_method():
    
    class A:
        pass
    
    @add_instance_method(A)
    def bar():
        return "Hello again!"
    
    assert A().bar() == "Hello again!"
    
def test_methods_issues():
    class Dummy:
        def method(self):
            return "instance method called"

        @classmethod
        def classmethod(cls):
            return "class method called"

        @staticmethod
        def staticmethod():
            return "static method called"
    
    @add_class_method(Dummy)
    def foo():
        return "Hello!"
    
    @add_instance_method(Dummy)
    def bar():
        return "Hello again!"
    
    assert Dummy().bar() == "Hello again!"
    assert Dummy.foo() == "Hello!"
    
  