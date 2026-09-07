---
title: 低价 Token 渠道记录
domain: projects
type: reference
status: active
updated: 2026-04-20
tags: [infrastructure, llm, token, pricing]
---

# 低价 Token 渠道记录

基于 hvoy https://hvoy.ai/APIreview.html 的《AI API中转站推荐与评测》。

## 结论

- 最稳妥的综合首选：RightCode
  - 原因：在 hvoy 的“推荐的”列表靠前，明确面向编程场景，文档清晰，最低充值门槛低，Claude / GPT / Gemini 都覆盖。
  - 价格：`/claude` 渠道 Sonnet 4.6 为 `¥4.5 / ¥22.5`，Opus 4.6 为 `¥7.5 / ¥37.5`（输入 / 输出，每 1M token）。
  - 评价：价格不是全网最低，但 hvoy 给出的评价是“质量也不错，对得起这个价格”，比单纯追求超低价更靠谱。

- 如果更重视稳定性和上游质量：PackyCode
  - 原因：hvoy 直接写到它是很多中转站的上游供应商，站长活跃，客服响应快，Gemini 速度表现也最好。
  - 价格：便宜线路 Opus 4.6 为 `¥4 / ¥20`，但 hvoy 标注“质量一般”；质量较好的 Opus 4.6 为 `¥12.5 / ¥62.5`。
  - 评价：更像“高质量、长期可用”的选择，不是最低价选择。

- 不建议把 SSSAICode 或 LinkAPI 直接当作“最好”
  - 原因：它们可能便宜，但 hvoy 的推荐区并没有把它们列为最值得优先用的站点；这类低价站更适合作为补充渠道或短期试用。
  - 原因：hvoy 明确提醒，行业里“价格异常便宜”的模型存在掺水、稳定性差、计费不透明等风险。

## 已记录渠道

| Provider     | 人民币/1M token (Claude Opus 4.6) | 链接                               | 备注                                                                                                                                                  |
| ------------ | ------------------------------ | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 云仲互企旗舰店 (淘宝) | ~5.25                          | https://cc.580ai.net/pricing     | 原始记录保留。淘宝买兑换码后到 `cc.580ai.net` 兑换，`1 人民币 = 1.785` 站内货币，约 `9.375` 站内货币 / 1M token。说明文档曾记录在 https://www.yuque.com/nicaisadasd/fwextu/ekk2q8nrf3ow4k9q |
| LinkAPI      | 4                              | https://linkapi.ai/pricing       | 原始记录保留。从 `relaypulse.top` 监控面板发现。价格有优势，但 hvoy 没有将其列为综合首选。                                                                                           |
| SSSAICode    | 3.2                            | https://www.sssaicode.com/models | 原始记录保留。从 `relaypulse.top` 监控面板发现。目前已记录价格里最低，但 hvoy 没有将其列为综合首选。                                                                                      |
| RightCode    | 7.5                            | https://www.rightcode.co/        | hvoy 当前综合首选。适合编程，价格不是最低，但质量和可用性平衡最好。                                                                                                                |
| PackyCode    | `4 （便宜线，质量一般）`12.5质量更好）        | https://www.packycode.com/       | hvoy 更偏向“稳定和上游质量”的推荐站。                                                                                                                              |
| 柏拉图AI        | 10                             | https://api.platodata.ai/        | 覆盖模型很全，适合企业或一站式需求。                                                                                                                                  |
| 云雾AI         | 6                              | https://yunwu.ai/                | 老牌站，稳定性不错。                                                                                                                                          |
| DawCode      | `7.5`                          | https://dawcode.com/             | 可试用，有赠送额度，但响应速度一般。                                                                                                                                  |
| FoxCode      | `0.5`                          | https://foxcode.top/             | 价格极低，但 hvoy 提到有用户反馈可能掺水，且最低充值 35 元。                                                                                                                 |
| ZeroCode     | `1`                            | https://zeroai.plus/             | 很便宜，但群不活跃，适合少量测试。                                                                                                                                   |

## 选择原则

- 首先看稳定性，再看价格。hvoy 明确把稳定性放在第一位。
- 对 Claude 来说，`¥7.5 / ¥37.5` 这类价格带通常比极低价更可信。
- 价格明显低到离谱的站，默认按“可能掺水、可能不稳定、可能账单不透明”处理。
- 不要大额充值，用多少充多少。

## 推荐动作

- 如果要一个“最好中转站”结论，当前先选 `RightCode`
- 如果你更看重稳定性和上游质量，备用选 `PackyCode`
- 如果你更在意极限低价，`SSSAICode`、`LinkAPI`、淘宝这条 `cc.580ai.net` 都值得继续保留观察
- 超低价站如 `FoxCode`、`ZeroCode` 只建议小额测试，不建议当唯一渠道

## 参考链接

- hvoy 评测页：https://hvoy.ai/APIreview.html