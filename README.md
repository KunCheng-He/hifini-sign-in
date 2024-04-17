## HIFINI 音乐磁场签到脚本

### 青龙面板使用步骤

1. 青龙面板创建订阅，然后复制以下命令到名称中：

```shell
ql repo https://github.com/KunCheng-He/hifini-sign-in.git "hifini.py" "" ""
```

![订阅管理](https://github.com/KunCheng-He/hifini-sign-in/assets/48958733/325aa8ec-68dd-47ed-9ca7-27357a50e4fa)

2. 添加依赖

![添加依赖](https://github.com/KunCheng-He/hifini-sign-in/assets/48958733/e3284d29-6ecd-4224-932b-37b52722339c)

3. 运行订阅

![运行订阅](https://github.com/KunCheng-He/hifini-sign-in/assets/48958733/ac660884-5d81-4dfc-a905-4fc894802dc0)

4. 创建环境变量

按图找到后复制cookie变量

![cookie](https://github.com/KunCheng-He/hifini-sign-in/assets/48958733/ebd0dedd-9f13-46e8-9784-fd799fd83a25)

创建环境变量 `HIFINI_COOKIE`

![创建环境变量](https://github.com/KunCheng-He/hifini-sign-in/assets/48958733/b35671d7-7467-4a10-86de-b695ac8e3efe)

5. 运行定时任务

已经添加完成，等待定时任务自动执行即可

### 致谢

- 源代码参考[fengwenhua/hifini_sign_in](https://github.com/fengwenhua/hifini_sign_in)，仓库很久没更新了，就重新写了一个以解决人机验证的问题
- 技术支持者[Xie Zhongtao](https://github.com/francisol)，感谢🫶
