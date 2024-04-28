from typing import List, Dict, Union
from transformers import AutoTokenizer


class ContextManagement:

    def __init__(self, max_available_tokens: int = 3000):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct")
        self.max_available_tokens = max_available_tokens

    def __count__tokens__(self, content: str):
        return len(self.tokenizer.tokenize(content)) + 2

    def __pad_tokens__(self, content: str, num_tokens: int):
        return self.tokenizer.decode(
            self.tokenizer.encode(content, max_length=num_tokens))

    def __manage_context__(self, messages: List[Dict]):
        managed_messages = []
        system_message = None
        if messages[0]["role"] == "system":
            system_message = messages[0]
        current_length = 0
        if system_message:
            current_length += self.__count__tokens__(
                system_message.get("content"))
        current_messsage_role = None
        for ix, message in enumerate(messages[1::-1]):
            content = message.get("content")
            message_tokens = self.__count__tokens__(message.get("content"))
            if ix > 1:
                if current_length + message_tokens >= self.max_available_tokens:
                    tokens_to_keep = self.max_available_tokens - current_length
                    if tokens_to_keep > 0:
                        content = self.__pad_tokens__(content, tokens_to_keep)
                        current_length += tokens_to_keep
                    else:
                        break
                if message.get("role") == current_messsage_role:
                    managed_messages[-1]["content"] = f"\n\n{content}"
                else:
                    managed_messages.append({
                        "role": message.get('role'),
                        "content": content
                    })
                    current_messsage_role = message.get("role")
                    current_messsage_role = message.get("role")
                    current_length += message_tokens
            else:
                if current_length + message_tokens >= self.max_available_tokens:
                    tokens_to_keep = self.max_available_tokens - current_length
                    if tokens_to_keep > 0:
                        content = self.__pad_tokens__(content, tokens_to_keep)
                        current_length += tokens_to_keep
                        managed_messages.append({
                            "role": message.get("role"),
                            "content": content
                        })
                    else:
                        break
                else:
                    managed_messages.append({
                        "role": message.get("role"),
                        "content": content
                    })
                    current_length += message_tokens
                current_messsage_role = message.get("role")
            print(f"TOTAL TOKENS: ", current_length)
            managed_messages = managed_messages[::-1]
            if system_message:
                managed_messages = [system_message] + managed_messages
            return managed_messages

    def __create_message_input__(self, messages: List[Dict]):
        return self.tokenizer.apply_chat_template(messages, tokenize=False)

    def __call__(self, messages: List[Dict]):
        managed_messages = self.__manage_context__(messages)
        return self.__create_message_input__(managed_messages)
