import asyncio
import os

os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"

from browser_use import Agent
from browser_use.llm import ChatOllama

async def main():
    models_to_test = [
        ("qwen3:4b", "Qwen 3 4B"),
    ]
    
    model_id, model_name = models_to_test[0]
    print(f"測試模型: {model_name} ({model_id})")
    
    llm = ChatOllama(model=model_id)
    
    agent = Agent(
        task="請開啟 Google Maps 搜尋「光嶼咖啡 楊梅」，找到營業時間並回報。只回報營業時間資訊。",
        llm=llm,
        use_vision=False,
        max_steps=15,
    )
    
    try:
        result = await agent.run()
        print(f"\n=== 結果 ===")
        print(result)
        print(f"\n模型 {model_name} 測試完成！")
    except Exception as e:
        print(f"\n=== 錯誤 ===")
        print(f"模型 {model_name} 失敗: {e}")

if __name__ == "__main__":
    asyncio.run(main())