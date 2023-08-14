from .modelhelper import num_tokens_from_messages


class MessageBuilder:
    """
      A class for building and managing messages in a chat conversation.
      Attributes:
          messages: A list of dictionaries representing chat messages.
          model: The name of the ChatGPT model.
          token_length: The total number of tokens in the conversation.
      """

    messages: list[dict[str, str]]
    model: str
    token_length: int


    def __init__(self, system_content: str, chatgpt_model: str):
        """Initializes the MessageBuilder instance."""
        self.messages = [{'role': 'system', 'content': system_content}]
        self.model = chatgpt_model
        self.token_length = num_tokens_from_messages(
            self.messages[-1], self.model)

    def append_message(self, role: str, content: str, index: int = 1):
        """Appends a new message to the conversation."""
        self.messages.insert(index, {'role': role, 'content': content})
        self.token_length += num_tokens_from_messages(
            self.messages[index], self.model)
