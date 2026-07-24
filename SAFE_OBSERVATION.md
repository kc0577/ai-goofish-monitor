# 安全观察模式

目标是先观察 7 天的供给、价格分布和疑似低价机会，不自动购买、不联系卖家、不自动发布商品。

## 默认边界

- 单账号；不使用代理池或账号轮换。
- 每个任务最多读取 1 页，仅查看 1 天内新发布。
- 不配置 Cron；由人工触发，每天最多两轮。
- 只用关键词规则，不调用 AI、不下载商品图片。
- 首次失败后暂停 24 小时，避免登录状态失效时反复请求。
- 结果只是候选线索，不代表商品真实、无故障或一定能转卖。

## 首批观察品类

1. Kindle Paperwhite 5：体积小、型号相对标准化，重点排除锁机、屏幕问题和电池衰减。
2. Redmi AX6000：型号标准化、运输简单，重点核对电源、刷机和维修情况。
3. Switch《塞尔达传说：王国之泪》卡带：单价较低、版本容易识别，重点核对卡带可读、封面语言和运费。

这些品类和价格只是观察假设。7 天后根据真实上架量、价格离散程度和风险信号决定保留或替换。

## 启动前

1. 将 `.env.safe-observation.example` 复制为 `.env`，替换 Web 密码。
2. 将 `config.safe-observation.example.json` 复制为 `config.json`。
3. 运行下方登录采集器，在可见的 Edge 窗口中由本人扫码或使用本人手机号登录。脚本检测成功后只在本机保存 `state/acc_1.json`，不会打印 Cookie。
4. 首轮只运行一个任务，并设置 `--debug-limit 3`。

示例：

```powershell
.venv\Scripts\python.exe scripts\capture_xianyu_login.py --output state\acc_1.json

.venv\Scripts\python.exe spider_v2.py --config config.json --task-name "Kindle Paperwhite 5 观察" --debug-limit 3
```

## 买入门槛

观察期结束前不买入。后续候选至少满足：可核验型号与状态、扣除运费后预计毛利率不低于 20%、预计毛利不低于 80 元、卖家行为无明显异常，并由用户本人最终确认付款。
