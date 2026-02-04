from router import route

def handler(event, context):
    """
    Lambda entrypoint
    """
    return route(event)
