
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler

from .logger import Logger

class LangChainLoggingHandler(BaseCallbackHandler, Logger):
    def __init__(self, log_mode=True):
        Logger.__init__(self, log_mode)

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        #chain_name = serialized.get('name') if serialized else 'Unknown'
        #self.langchain_logger.info(f"Chain {chain_name} started")
        pass
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        #self.langchain_logger.info(f"Chain ended, outputs: {outputs}")
        pass

    def on_text(self, text: str, **kwargs) -> None:
        #self.langchain_logger.info(text)
        pass