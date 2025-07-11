from openai import OpenAI
import yaml
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_agent(agent_name: str, user_input: str) -> str:
    cfg = load_config()

    client = OpenAI(
        api_key=cfg["open_ai_key"],
        base_url=cfg["openai_api_base"]
    )

    prompt_path = Path(__file__).parent.parent / "prompts" / f"{agent_name}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"No prompt found for agent '{agent_name}'")

    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content