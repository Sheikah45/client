from chat.chat_widget import ChatWidget
from chat.channel_view import ChannelView


class ChatView:
    def __init__(self, chat, controller, widget, channel_view_builder):
        self._chat = chat
        self._controller = controller
        self.widget = widget
        self._channel_view_builder = channel_view_builder
        self._channels = {}
        self._chat.channels.added.connect(self._add_channel)
        self._chat.channels.removed.connect(self._remove_channel)
        self._chat.new_server_message.connect(self._new_server_message)
        self.widget.channel_quit_request.connect(self._at_channel_quit_request)
        self._add_channels()

    @classmethod
    def build(cls, chat, controller, **kwargs):
        chat_widget = ChatWidget.build(**kwargs)
        channel_view_builder = ChannelView.builder(controller, **kwargs)
        return cls(chat, controller, chat_widget, channel_view_builder)

    def _add_channels(self):
        for channel in self._chat.channels.values():
            self._add_channel(channel)

    def _add_channel(self, channel):
        if channel.id_key in self._channels:
            return
        view = self._channel_view_builder(channel)
        self._channels[channel.id_key] = view
        self.widget.add_channel(view.widget, channel.id_key.name)

    def _remove_channel(self, channel):
        if channel.id_key not in self._channels:
            return
        view = self._channels[channel.id_key]
        self.widget.remove_channel(view.widget)
        del self._channels[channel.id_key]

    def _new_server_message(self, msg):
        self.widget.write_server_message(msg)

    def _at_channel_quit_request(self, cid):
        self._controller.leave_channel(cid, "tab closed")