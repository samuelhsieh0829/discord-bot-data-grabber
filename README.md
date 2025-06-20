# Discord bot data grabber
輸入你的dc bot token來取得機器人所在的伺服器及資訊
## 可用指令
- `help` 查看所有可用的指令
- `guilds` 取得機器人所在的所有伺服器(包含id、人數)
- `channels <guild_id>` 取得某伺服器的所有頻道
- `members <guild_id>` 取得某在伺服器內的所有使用者 (需要guild user intents)
- `messages <guild_id> <channel_id> (<limit>)` 取得在某伺服器某頻道內的最近訊息(預設為10則)
- `exit` 結束程式