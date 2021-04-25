def greetings(name):
    def print_greetings(*args):
        return f'Hello {name(*args).title()}'
    return print_greetings

def is_palindrome(fun):
    def palindrome_check(*args):
        to_analyse = ''
        for c in fun(*args):
            if c.isalnum():
                to_analyse += c.lower()
        
        for i in range(int(len(to_analyse)/2)):
            if to_analyse[i] != to_analyse[len(to_analyse)-1-i]:
                return f'{fun(*args)} - is not palindrome'
        return f'{fun(*args)} - is palindrome'
    return palindrome_check

def format_output(*args):
    keys_to_check = args
    def real_dec(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            out_dict = {}
            for key in keys_to_check:
                keys_split = key.split('__')
                for key_part in keys_split:
                    if key_part in result.keys():
                        if key not in out_dict.keys():
                            out_dict[key] = result[key_part]
                        else:
                            out_dict[key] += (' ' + result[key_part])
                    else:
                        raise ValueError
            return out_dict
        return wrapper
    return real_dec                

def add_class_method(input_class):
    def real_dec(func):
        setattr(input_class, func.__name__, func)
        return func
    return real_dec            
    
def add_instance_method(input_class):
    def real_dec(func):     
        self_func = lambda self : func()
        setattr(input_class, func.__name__, self_func)
        return func
    return real_dec
