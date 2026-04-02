from pathlib import Path
from llama_cpp import Llama

MODEL_PATH = "./assets/models/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"
PROMPT_PATH = Path("./assets/prompts/system_prompt.txt")

def _load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()

llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,
    n_ctx=4096,
    verbose=False,
)


async def generate_response(user_message: str, context: str = "") -> str:
    system = _load_system_prompt()
    if context:
        system += f"\n\n[참고 문서]\n{context}\n\n위 참고 문서에서 질문과 관련된 내용만 간결하게 답변하세요."

    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
        max_tokens=512,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]
