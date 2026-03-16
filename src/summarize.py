"""
Voice AI weekly report summarization using DeepSeek API.
(OpenAI-compatible interface)
"""

import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一位专业的语音AI行业分析师，负责撰写中英混合的行业周报。

## 输出要求
- 使用 Markdown 格式
- 标题和摘要用中文撰写
- 公司名称、产品名、技术术语、原文链接保留英文
- 语言简洁专业，避免空泛描述

## 输出结构

# 语音AI行业周报

## 一、并购动态
（列出本周与语音AI相关的并购/收购新闻，每条包含：）
- **中文标题**
- 一句话摘要（中文）
- 交易双方、金额（如有）
- 原文链接

## 二、初创公司速览
（列出近期值得关注的语音AI初创公司，每家包含：）
- 公司名称及官网
- 赛道定位（如TTS、ASR、Voice Agent、对话式AI等）
- 融资阶段和金额
- 核心技术/产品亮点

## 三、本周观点
（2-3句简要趋势总结）

## 注意事项
- 如果搜索结果中某些条目与语音AI无关，直接跳过
- 如果并购或初创公司信息不足，可以合并为较少条目，不要编造信息
- 每个板块至少保留1条内容，最多不超过8条
"""

USER_PROMPT_TEMPLATE = """以下是本周搜集到的语音AI相关新闻和信息，请整理成行业周报：

---
{search_results}
---

请根据上述信息，按要求格式输出周报内容。只使用上述提供的信息，不要编造不存在的新闻。"""


def summarize_results(search_results: list[dict], api_key: str | None = None) -> str:
    """
    Use DeepSeek API to summarize search results into a structured weekly report.

    Args:
        search_results: List of dicts with title, url, description, source.
        api_key: DeepSeek API key.

    Returns:
        Markdown formatted report string.
    """
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is required")

    # Format search results into text
    formatted = []
    for i, item in enumerate(search_results, 1):
        formatted.append(
            f"{i}. 标题: {item['title']}\n"
            f"   来源: {item['source']}\n"
            f"   链接: {item['url']}\n"
            f"   摘要: {item['description']}\n"
        )
    results_text = "\n".join(formatted)

    if not results_text.strip():
        return "# 语音AI行业周报\n\n本周未搜集到相关新闻。"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    logger.info(f"Sending {len(search_results)} results to DeepSeek for summarization...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(search_results=results_text),
            },
        ],
    )

    report = response.choices[0].message.content
    logger.info(f"Report generated: {len(report)} characters")
    return report


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Test with dummy data
    test_data = [
        {
            "title": "Meta acquires PlayAI for voice AI capabilities",
            "url": "https://example.com/meta-playai",
            "description": "Meta completed acquisition of PlayAI, a voice AI startup.",
            "source": "techcrunch.com",
        }
    ]
    print(summarize_results(test_data))
