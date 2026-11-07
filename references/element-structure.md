# Elementor 普通元素结构与样式数据

核对日期：2026-10-19。以下是 Elementor 官方文档的要点整理，不是原文副本。文档示例说明数据形状；具体控件键名和值仍以目标站同版本导出或对应版本源码为准。

## 页面模板与剪贴板元素

- 官方完整页面／模板 JSON 包含 `title`、`type`、`version`、`page_settings`、`content`。本 skill 的一键复制文件传递的是元素数组，不使用完整页面／模板外壳。
- 普通容器至少有 `id`、`elType: "container"`、`isInner`、`settings`、`elements`。`elements` 是子元素数组，可递归嵌套。
- 普通 widget 同样有 `id`、`elType: "widget"`、`isInner`、`settings`、`elements`，另有 `widgetType`。`settings` 的键来自该 widget 的控件 ID；不要由 CSS 属性名直接猜测。
- 未设置时，官方例子允许 `settings: []`；有设置时使用对象。复制生成器的当前校验可能更严格，实际构造时同时满足脚本要求。
- `id` 为唯一字符串。7–8 位十六进制只是本 skill 的生成约定，不是官方唯一格式。

## 表格 HTML 元素

核对日期：2026-11-03。Elementor 自带 HTML 元素的 `widgetType` 为 `"html"`，代码控件 ID 为 `html`，因此表格结构及必要包裹层写入 `settings.html`。其他内容继续使用普通组件。

项目生成约定：表格 CSS 写入该 HTML 元素“高级 → Custom CSS”的 `settings.custom_css`，使用 `selector` 限定当前元素作用域；`settings.html` 不放 `<style>` 或内联 `style`。例如 HTML 为 `<div class="jw-table-wrap"><table>...</table></div>`，Custom CSS 可为 `selector .jw-table-wrap { overflow-x: auto; }`。`custom_css` 字段与 `selector` 写法已有项目生成数据先例，目标站仍须支持元素级 Custom CSS；不能将本地包装成功视为目标站样式已生效。

字段依据：[Elementor HTML 元素源码](https://github.com/elementor/elementor/blob/main/includes/widgets/html.php)中的 `get_name()`、`register_controls()` 和 `render()`。本次核对的是 `main` 分支，目标站版本或权限影响元素可用性时仍须另行核实。

## 原生 Tabs 组件

核对日期：2026-11-04。新版嵌套 Tabs 的 `widgetType` 为 `"nested-tabs"`，标签内容使用子容器；旧版 Tabs 的 `widgetType` 为 `"tabs"`，通过重复项中的 `tab_title`、`tab_content` 保存标签及富文本。两种结构不能互换。

Elementor 4.3.5 的标签重复项、内容容器索引、方向与样式字段、默认激活项和同组件 Custom CSS，已整理在 [原生 Tabs 参考](native-tabs.md)。转换 Tab 时读取该文件，不在这里重复维护字段清单。`nested-tabs` 是普通内置嵌套 widget，不是本 skill 禁止的 `e-*` 原子元素；包装脚本已有的递归结构校验可处理其子容器，不证明标签关联或切换行为正确。

## 原生 Accordion 组件

核对日期：2026-11-04。嵌套手风琴的 `widgetType` 为 `"nested-accordion"`，标题放在 `settings.items`，正文放在按数组索引对应的普通子容器中。控件键名、可复用的展开与动画配置、同组件 Custom CSS 和结构示例集中维护在 [原生 Accordion 参考](native-accordion.md)。它属于普通内置嵌套 widget。

## 响应式与全局样式

- 官方响应式数据将默认值放在基本控件键，平板和手机分别使用 `_tablet`、`_mobile` 后缀。额外断点遵循相同后缀模式；仅目标站实际支持的断点才可使用。
- 例如 `align`、`align_tablet`、`align_mobile` 可存不同设备的对齐值。尺寸控件通常使用包含 `unit`、`size`、`sizes` 的对象，不应一律写成 CSS 字符串。
- 全局颜色和字体引用存放在 `settings.__globals__`，值形式为 `globals/<type>?id=<global-id>`。这些 ID 属于站点 Kit；跨站生成时优先使用独立值，除非目标站的全局 ID 已核实。

## 控件字段的核对顺序

1. 先查这份本地参考中已记录的结构、字段及限制。
2. 需要确认具体控件键名和值时，以目标站实际导出的同类型普通容器或 widget 为准；没有导出时，查项目内其他已验证的同版本设置。
3. 本地资料和目标站导出仍不足，或出现陌生字段、复杂交互及版本差异时，再查对应版本源码或在线官方资料。不要仅凭 CSS 名称或这份笔记猜测控件键名。

既有项目中的普通容器 hover 字段参考：`background_hover_background`、`background_hover_color`、`background_hover_transition`、`border_hover_border`、`border_hover_color`、`box_shadow_hover_box_shadow_type`、`box_shadow_hover_box_shadow`、`border_hover_transition`。这是项目参考，未核定为所有版本通用字段；需要时与目标站导出或对应版本源码比对。

## 官方来源

- [General Structure](https://developers.elementor.com/docs/data-structure/general-structure/)
- [Container Element](https://developers.elementor.com/docs/data-structure/container-element/)
- [Widget Element](https://developers.elementor.com/docs/data-structure/widget-element/)
- [Responsive Data](https://developers.elementor.com/docs/data-structure/responsive-data/)
- [Global Styles](https://developers.elementor.com/docs/data-structure/global-styles/)
- [Elementor 容器源码](https://github.com/elementor/elementor/blob/main/includes/elements/container.php)（`main` 分支会变化，版本相关问题应查对应版本）
