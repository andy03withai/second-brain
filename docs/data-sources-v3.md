# 每日简报 - 信息源配置 v3.0

## 📰 国际科技媒体 (Tier 1)

| 名称 | 类型 | 网址 | 覆盖领域 | 更新频率 |
|------|------|------|----------|----------|
| **TechCrunch AI** | 科技新闻 | techcrunch.com/category/artificial-intelligence/ | 初创公司、产品发布、融资 | 每日 |
| **The Verge AI** | 科技新闻 | theverge.com/ai-artificial-intelligence | 消费科技、政策、深度报道 | 每日 |
| **MIT Technology Review** | 科技媒体 | technologyreview.com/topic/artificial-intelligence/ | 研究突破、政策、伦理 | 每周 |
| **Wired AI** | 科技媒体 | wired.com/tag/artificial-intelligence/ | 深度调查、未来趋势 | 每日 |
| **Ars Technica** | 技术新闻 | arstechnica.com/tag/artificial-intelligence/ | 技术深度分析、安全 | 每日 |
| **Bloomberg AI** | 财经媒体 | bloomberg.com/artificial-intelligence | 商业、投资、市场 | 每日 |
| **The Information** | 科技订阅 | theinformation.com/topics/artificial-intelligence | 独家报道、深度调查 | 每日 |

## 📧 国际AI Newsletter (Tier 1)

| 名称 | 作者/机构 | 网址 | 特点 | 频率 |
|------|-----------|------|------|------|
| **The Batch** | Andrew Ng/DeepLearning.AI | deeplearning.ai/the-batch | 权威研究综述、教育导向 | 每周 |
| **Import AI** | Jack Clark (Anthropic联创) | importai.substack.com | 研究深度分析、政策视角 | 每周 |
| **TLDR AI** | TLDR团队 | tldr.tech/ai | 简洁技术摘要、开发者友好 | 每日 |
| **The Rundown AI** | Rowan Cheung | therundown.ai | 快速工具/新闻更新 | 每日 |
| **Superhuman AI** | Zain Kahn | superhuman.ai | 生产力工具、商业应用 | 每日 |
| **AlphaSignal** | - | alphasignal.ai | ML工程、GitHub趋势 | 每周 |
| **AI Weekly** | - | aiweekly.co | 深度长文、研究趋势 | 每周 |
| **The Neuron** | - | theneurondaily.com | 轻松易读、带meme | 每日 |
| **Ben's Bites** | Ben Tossell | bensbites.co | 产品新闻、创业用例 | 每日 |
| **Mindstream** | HubSpot | mindstream.beehiiv.com | 每日AI新闻、工具 | 每日 |

## 🎓 学术资源 (Tier 1)

| 名称 | 类型 | 网址 | 说明 |
|------|------|------|------|
| **Hugging Face Daily Papers** | 论文聚合 | huggingface.co/papers | 社区投票Top论文 | 每日 |
| **Hugging Face Trending Papers** | 论文趋势 | huggingface.co/trending-papers | GitHub关联、趋势排序 | 实时 |
| **Papers with Code** | 论文+代码 | paperswithcode.com | 代码实现、基准测试 | 每日 |
| **arXiv** | 预印本 | arxiv.org | cs.AI, cs.LG, cs.CL, cs.CV, cs.RO | 每日 |
| **Semantic Scholar** | 学术搜索 | semanticscholar.org | 引用数、影响力指标 | 实时 |
| **Google AI Blog** | 官方博客 | ai.googleblog.com | Google研究进展 | 不定期 |
| **DeepMind Blog** | 官方博客 | deepmind.com/blog | DeepMind研究突破 | 不定期 |
| **OpenAI Blog** | 官方博客 | openai.com/blog | OpenAI产品/研究 | 不定期 |
| **Anthropic Blog** | 官方博客 | anthropic.com/news | Anthropic安全/研究 | 不定期 |

## 🏢 企业/官方发布

| 公司 | 博客/新闻 | 说明 |
|------|-----------|------|
| **OpenAI** | openai.com/blog | 模型发布、API更新 |
| **Anthropic** | anthropic.com/news | Claude更新、安全研究 |
| **Google DeepMind** | deepmind.com/blog | 研究突破、Gemini更新 |
| **Microsoft AI** | blogs.microsoft.com/ai/ | Copilot、Azure AI |
| **Meta AI** | ai.meta.com/blog/ | Llama、PyTorch、研究 |
| **NVIDIA** | blogs.nvidia.com/ai/ | 芯片、CUDA、推理优化 |
| **Hugging Face** | huggingface.co/blog | 开源模型、工具更新 |

## 🔧 开发者社区

| 名称 | 类型 | 网址 |
|------|------|------|
| **GitHub Trending** | 代码趋势 | github.com/trending | 
| **Hacker News** | 技术社区 | news.ycombinator.com |
| **Lobsters** | 技术社区 | lobste.rs |
| **Reddit r/MachineLearning** | 社区论坛 | reddit.com/r/MachineLearning |
| **Reddit r/LocalLLaMA** | 社区论坛 | reddit.com/r/LocalLLaMA |

## 📊 当前脚本已对接的数据源

- ✅ Hugging Face Daily Papers (API)
- ✅ arXiv (API)
- ✅ Semantic Scholar (API)
- ❌ TechCrunch (需搜索)
- ❌ The Verge (需搜索)
- ❌ MIT Technology Review (需搜索)
- ❌ Newsletters (需搜索)

## 🎯 推荐的信息源更新策略

### 方案A: 增强搜索 (推荐)
使用 `kimi_search` 定时搜索以下关键词组合:
1. "AI news today site:techcrunch.com"
2. "artificial intelligence site:mit.edu"
3. "AI breakthrough site:deepmind.com"
4. "Import AI newsletter"

### 方案B: RSS聚合
搭建RSS聚合器订阅各媒体RSS，统一抓取。

### 方案C: 混合方案
- 学术论文: HF Daily + arXiv + Semantic Scholar (保持现有)
- 行业新闻: 定时搜索TechCrunch/MIT Tech Review等
- Newsletter: 定时搜索Import AI/TLDR等归档

---

*信息源配置 v3.0 - 更新于 2026-03-10*
*目标: 从中文为主转向国际视野*
