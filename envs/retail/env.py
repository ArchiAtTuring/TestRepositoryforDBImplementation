from envs.retail.data import load_data
from envs.retail.rules import RULES
from envs.retail.tools import (
    ALL_TOOLS_INTERFACE_1,
)
from envs.base import Env
from typing import Optional, Union
from envs.user import UserStrategy
import os


class MockRetailDomainEnv(Env):
    def __init__(
        self,
        user_strategy: Union[str, UserStrategy] = UserStrategy.LLM,
        user_model: str = "gpt-4o",
        user_provider: Optional[str] = None,
        task_split: str = "test",
        task_index: Optional[int] = None,
        interface_num: Optional[int] = 2,  # Default to Interface 2 (Retail Ops)
    ):
        match task_split:
            case "test":
                from envs.retail.tasks import tasks
            case _:
                raise ValueError(f"Unknown task split: {task_split}")
        
        # Select tools based on interface_num
        match interface_num:
            case 1:
                tools = ALL_TOOLS_INTERFACE_1
            case _:
                raise ValueError(f"Unknown interface_num: {interface_num}")
            
        # Load policy (System Prompt) based on interface_num
        folder_path = os.path.dirname(__file__)
        match interface_num:
            case 2:
                # Loads the 'Retail Operations' policy we wrote in Step 1
                policy_path = os.path.join(folder_path, "policy.txt")
            case _:
                raise ValueError(f"Unknown interface_num: {interface_num}")
        
        with open(policy_path, "r") as f:
            wiki = f.read()
        
        super().__init__(
            data_load_func=load_data,
            tools=tools,
            tasks=tasks,
            wiki=wiki,
            rules=RULES,
            user_strategy=user_strategy,
            user_model=user_model,
            user_provider=user_provider,
            task_index=task_index,
        )
        self.terminate_tools = ["transfer_to_human"]