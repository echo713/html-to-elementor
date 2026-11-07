# Elementor 跨站复制与兼容性

核对日期：2026-10-19。以下整理自 Elementor 官方帮助文档和官方仓库的复制／粘贴源码。源码链接指向 `main` 分支，目标网站可能运行不同版本。

## 一键复制数据

当前官方复制源码创建的对象包含 `type: "elementor"`、`siteurl` 和 `elements`；其中 `siteurl` 来自来源编辑器的 `elementorCommon.config.urls.rest`，`elements` 是所选元素的数据数组。它不是页面 URL，也不是完整模板导入 JSON。

当前粘贴源码先检查 `type` 和非空 `elements`；随后比较剪贴板 `siteurl` 与目标站 REST 根地址。两者不同时，调用 `import_from_json` 处理元素。因此已有外站复制数据应保留实际来源地址，不能伪装为目标站以跳过导入。为目标站从零重建且不含外站资源 ID 的数据，可按本 skill 的生成约定使用目标站实际 REST 根地址；这不是官方提供的 HTML 自动转换接口。

## 官方操作与适用条件

- 编辑器中复制元素后，在目标站的容器区域右键选择 “Paste from other site”，再按 Ctrl+V 或 Cmd+V 完成粘贴。
- Elementor 帮助文档写明：来源站与目标站至少使用 Elementor 3.11，且启用相同相关功能；不能将容器粘到只使用旧式 Section 的站点。
- 官方帮助文档明确此流程只适用于 Elementor Editor 元素，不适用于第三方插件组件。
- 以上是跨站复制条件，不保证本 skill 从 HTML 重建的任意元素在目标版本、目标主题和插件组合中无损显示。

## 实施和验证边界

- 默认使用普通 Elementor 容器与内置 widget；媒体 ID、全局 Kit 引用、模板引用及第三方组件不能直接跨站照搬。
- 图片来源与询问交互按主文件“图片来源与留空”执行：缺少图片地址时弹出对话输入框，收到用户填写的地址则使用，选择“否，留空”或明确要求留空则留空；不通过 MCP 或其他方式查询 WordPress 来查找图片或匹配附件 ID。
- 本地包装脚本能检查 JSON 结构和嵌入数据的往返一致性；复制按钮本身需要在浏览器中操作验证。这些本地检查不能证明目标编辑器已成功粘贴或实际渲染一致。若用户授权或提供目标编辑器环境，实际粘贴并查看后才能报告该项已验证。
- 目标站版本、功能状态或某控件行为不明时，先查看目标站实际配置／导出；仍有缺口再访问对应版本的官方资料或源码。不要把 `main` 分支行为直接当成旧版本行为。

## 官方来源

- [How do I copy elements from one site to another?](https://elementor.com/help/how-do-i-copy-elements-from-one-site-to-another/)（页面显示最后更新为 2026-09-15）
- [Copy command 源码](https://github.com/elementor/elementor/blob/main/assets/dev/js/editor/document/elements/commands/copy.js)
- [Paste command 源码](https://github.com/elementor/elementor/blob/main/assets/dev/js/editor/document/elements/commands/paste.js)
