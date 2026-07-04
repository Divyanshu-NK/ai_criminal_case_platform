import logging
import time
from typing import Any, Dict, List, Optional
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult

logger = logging.getLogger("agent_logger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

class AgentLoggingCallbackHandler(AsyncCallbackHandler):
    """Callback handler to log Prompt -> Latency -> Tokens -> Cost -> Output."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.start_time: float = 0.0
        
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        self.start_time = time.time()
        logger.info(f"[{self.agent_name}] Starting LLM call. Prompt: {prompts[0][:200]}...")

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        latency = time.time() - self.start_time
        
        # Try to extract tokens and cost
        llm_output = response.llm_output or {}
        token_usage = llm_output.get("token_usage", {})
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", 0)
        
        # Basic cost estimation (Google Gemini 1.5/2.5 Flash prices approximate)
        cost = (prompt_tokens * 0.075 / 1_000_000) + (completion_tokens * 0.30 / 1_000_000)
        
        output_str = ""
        if response.generations and response.generations[0]:
            output_str = response.generations[0][0].text
            
        logger.info(
            f"[{self.agent_name}] Finished LLM call. "
            f"Latency: {latency:.2f}s | "
            f"Tokens: {total_tokens} (Prompt: {prompt_tokens}, Completion: {completion_tokens}) | "
            f"Cost: ${cost:.6f} | "
            f"Output: {output_str[:200]}..."
        )

    async def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        latency = time.time() - self.start_time
        logger.error(f"[{self.agent_name}] LLM Error after {latency:.2f}s: {error}")
