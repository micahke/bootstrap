from llama_index import PromptHelper
from llama_index.llms import ChatMessage, MessageRole, OpenAI
from data.chat import ChatHistory, ChatItem, ChatRole, get_latest_chat_id, load_chat_history, save_chat_history
from data.config import Config
from llm.llama_index import LlamaClient
from process.process import Process
from typing import Any, List

class GenerationProcess(Process):
    def __init__(self, config: Config, client: LlamaClient, prompt: str) -> None:
        super().__init__()
        self.config = config
        self.client = client
        self.prompt = prompt


    def history_to_li_history(self, history: ChatHistory) -> List[ChatMessage]:
        msgs: List[ChatMessage] = []
        for item in history.messages:
            msg = ChatMessage(
                content=item.message,
                role=MessageRole.USER if item.role is ChatRole.USER else MessageRole.ASSISTANT
            )
            msgs.append(msg)

        return msgs


    def run(self, args: Any = None):
        llm = OpenAI(model=self.config.llm_params.model_type.value[1], temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        # print(self.config.max_tokens, self.config.llm_params.model_type.value[2])
        prompt_helper = PromptHelper(
          context_window=self.config.llm_params.model_type.value[2],
          num_output=self.config.max_tokens or 512,
          chunk_overlap_ratio=0.5,
          chunk_size_limit=None
        )
        history = load_chat_history(get_latest_chat_id())
        # print(self.history_to_li_history(history))
        index = self.client.load_index(llm, prompt_helper)
        response = self.client.query(index, self.prompt, self.history_to_li_history(history))
        if response is not None:
            history.messages.append(ChatItem(message=self.prompt, role=ChatRole.USER))
            history.messages.append(ChatItem(message=response, role=ChatRole.ASSISTANT))
            save_chat_history(get_latest_chat_id(), history)



