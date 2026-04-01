from llama_cpp import Llama

MODEL_PATH = "./assets/models/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"

SYSTEM_PROMPT = "당신은 친절한 AI 상담원입니다. 고객의 질문에 한국어로 간결하고 정확하게 답변해주세요."

llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,   # GPU 최대 활용
    n_ctx=4096,        # 컨텍스트 길이
    verbose=False,
)


async def generate_response(user_message: str, context: str = "") -> str:
    system = SYSTEM_PROMPT
    if context:
        system += f"\n\n아래 참고 문서를 바탕으로 답변하세요:\n{context}"

    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
        max_tokens=512,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]
