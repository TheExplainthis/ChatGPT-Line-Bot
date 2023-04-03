from src.logger import logger


def get_event_id(event):
    """
    Returns the ID of the event source, which can be a user or a group.
    `user_id` and `group_id` can both be used to identify a user in the Line Bot API, 
    whether the user is in a one-on-one chat or a group chat.

    Args:
        event: A Line Bot API event object.

    Returns:
        The ID of the event source as a string.

    Raises:
        RuntimeError: If the event source type is unsupported.
    """
    if event.source.type == 'user':
        id = event.source.user_id
    elif event.source.type == 'group':
        id = event.source.group_id
    else:
        raise RuntimeError(f'Unsupported source type {event.source.type}')
    return id



def event_handler(func):
    def wrapper(event):
        try:
            reply_token = event.reply_token
            # If the event is a join event, the user ID is not available.
            if event.type == 'join':
                return func(reply_token)
            # If the event is a message event, the message type can be text or audio.
            id = get_event_id(event)
            if event.message.type == 'text':
                text = event.message.text.strip()
                return func(reply_token, id, text)
            elif event.message.type == 'audio':
                message_id = event.message.id
                return func(reply_token, id, message_id)
            else:
                raise RuntimeError(f'Unsupported message type {event.message.type}')
        except Exception as e:
            return func(reply_token, None, str(e))
    return wrapper