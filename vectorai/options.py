OPTIONS = {
    'return_curl': False,
    'maximum_num_of_http_retries': 3,
    'maximum_http_timeout': 5
}

def get_option(option_field):
    return OPTIONS[option_field]

def set_option(option_field, value):
    OPTIONS[option_field]= value
