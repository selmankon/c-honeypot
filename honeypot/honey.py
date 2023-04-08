
def honey(data):
    # This is the honey function
    # It will be called when the honeypot is triggered
    # It will send a fake response to the client
    # and then close the connection
    response = ""

    if data == 'whoami':
        response = 'anadolufs'

    return response
