import json

class MessageParser(object):
    def __init__(self, message_handler):
        self.message_handler = message_handler

    def parse(self, handle, message):
        decoded_message = json.loads(message)
        if decoded_message['type'] == 'register':
            self.message_handler.register(handle, decoded_message['args']['channel_id'])
        self.message_handler.handle(decoded_message, handle)


class MessageHandler(object):

    def __init__(self, boards_controller):
        self.boards_controller = boards_controller

    def register(self, handle, channel_id):
        connected_users = self.boards_controller.count_users(channel_id)
        self.boards_controller.register(channel_id, handle)
        message = Message("info",{"users":connected_users})
        handle.send(message.as_json())

    def handle(self, decoded_message, source):
        message = Message(decoded_message['type'],decoded_message['args'])
        channel_id = decoded_message['args']['channel_id']
        self.publish(message, channel_id, source)

    def publish(self, message, channel_id, excluded_handle=None):
        for board_handle in self.boards_controller.get_board_handles(channel_id):
            if board_handle!=excluded_handle:
                board_handle.send(json.dumps(message.as_dict()))


class Message(object):

    def __init__(self, type, args=None):
        self.type = type
        self.args = args

    def as_dict(self):
        return {"type":self.type, "args": self.args}

    def as_json(self):
        return json.dumps(self.as_dict())
