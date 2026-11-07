# Elementor 原生 Tabs：结构、字段与 Custom CSS

核对日期：2026-11-04。字段来源为 Elementor **4.3.5** 官方源码；目标站当日运行该版本、启用了普通容器及嵌套元素，现有页面结构中发现 `nested-tabs`。这些事实用于复用数据结构，不等于新生成模块已经在编辑器中粘贴、渲染或操作验证。

## 读取与复用范围

- 主文件规定使用原生 Tabs；此参考补充具体数据结构和已核对字段，仅在转换 Tabs 时读取。
- 相同版本、相同结构和下列已覆盖字段可直接复用，无需重复搜索官方源码。目标版本变化、需要本文件未覆盖的控件，或实际导出与本记录冲突时，再查对应版本资料并更新相关记录。
- 这里的 220px 标签列、300px 内容区和 767px 手机断点均为示例。实际值按源设计及目标站断点设置，不把某次产品模块的尺寸或七项内容数量变成通用要求。
- MCP 的 widget schema 工具可能只覆盖它允许编辑的组件。返回 `Unknown widget type: nested-tabs` 不能单独证明网站没有该组件；应结合目标站配置、实际元素树或同版本源码判断。元素树没有 settings 时，只能证明组件出现过，不能据此声称拿到了完整导出设置。

## 数据结构与标签对应关系

使用 `widgetType: "nested-tabs"`；标签重复项在 `settings.tabs`，每项的 `tab_title` 为网页上显示的标签名称。

| 数据 | 含义及规则 |
|---|---|
| `settings.tabs[i]` | 第 i 个标签重复项；`_id` 是重复项自己的唯一 ID |
| `settings.tabs[i].tab_title` | 标签文字，保留用户确认内容与顺序 |
| `settings.tabs[i].tab_icon`、`tab_icon_active` | 图标对象；不使用图标时可设为 `{"value":"","library":""}` |
| `settings.tabs[i].element_id` | 可选的标签 CSS ID，不是内容容器的 Elementor ID |
| `elements[i]` | 第 i 个标签对应的普通内容容器，顺序与重复项一致 |
| 内容容器的 `elements` | 原生 heading、text-editor、image 等子组件 |

`tabs` 和直接内容容器的数量必须一致。4.3.5 通过数组索引打印对应内容，不通过重复项 `_id` 与容器 ID 相等来关联；因此不要为了“绑定”而复用这两个 ID，也不要在改标签顺序后遗漏内容容器排序。

4.3.5 的 `render_tab_titles_html()` 默认将第一项设为选中，`add_attributes_to_container()` 默认给第一项内容添加 `e-active`。默认首项可沿用此行为；不能虚构 `active_index` 等未经核对的设置来改变默认项。若源设计要求其他默认项，先核对目标版本可用的原生方法，且不能悄悄改动标签顺序。

### 最小结构示例

这是 widget 数据片段，可作为元素数组中的一项。示例 ID 仅用于展示，实际生成时重新生成唯一 ID；中文 `_title` 只用于导航器，网页文字保持用户确认内容。

```json
{
  "id": "ab000001",
  "elType": "widget",
  "widgetType": "nested-tabs",
  "isInner": false,
  "settings": {
    "_title": "原生竖向选项卡",
    "tabs": [
      {"_id": "bb00001", "tab_title": "Materials", "tab_icon": {"value": "", "library": ""}, "tab_icon_active": {"value": "", "library": ""}},
      {"_id": "bb00002", "tab_title": "Construction", "tab_icon": {"value": "", "library": ""}, "tab_icon_active": {"value": "", "library": ""}}
    ],
    "tabs_direction": "inline-start",
    "tabs_direction_mobile": "block-start",
    "tabs_width": {"unit": "px", "size": 220, "sizes": []},
    "tabs_title_space_between": {"unit": "px", "size": 6, "sizes": []},
    "tabs_title_spacing": {"unit": "px", "size": 16, "sizes": []},
    "title_alignment": "start",
    "breakpoint_selector": "none",
    "custom_css": "selector .e-n-tabs-content { min-width: 0; }"
  },
  "elements": [
    {
      "id": "ab000002", "elType": "container", "isInner": true,
      "settings": {"_title": "材质标签内容", "content_width": "full"},
      "elements": [
        {
          "id": "ab000003", "elType": "widget", "widgetType": "heading", "isInner": false,
          "settings": {"_title": "材质标题", "title": "Materials", "header_size": "h4"}, "elements": []
        },
        {
          "id": "ab000004", "elType": "widget", "widgetType": "text-editor", "isInner": false,
          "settings": {"_title": "材质正文", "editor": "<p>Material details.</p>"}, "elements": []
        }
      ]
    },
    {
      "id": "ab000005", "elType": "container", "isInner": true,
      "settings": {"_title": "结构标签内容", "content_width": "full"},
      "elements": [
        {
          "id": "ab000006", "elType": "widget", "widgetType": "heading", "isInner": false,
          "settings": {"_title": "结构标题", "title": "Construction", "header_size": "h4"}, "elements": []
        },
        {
          "id": "ab000007", "elType": "widget", "widgetType": "text-editor", "isInner": false,
          "settings": {"_title": "结构正文", "editor": "<p>Construction details.</p>"}, "elements": []
        }
      ]
    }
  ]
}
```

## 4.3.5 已核对的原生控件

尺寸示例使用 `{"unit":"px","size":220,"sizes":[]}`；边距类 DIMENSIONS 使用 `unit`、`top/right/bottom/left` 和 `isLinked` 对象。响应式值用 `_tablet`、`_mobile` 后缀，不能把 CSS 字符串直接作为尺寸值。

| 控件 | 用途及已核对值 |
|---|---|
| `tabs_direction` | `inline-start`：标签在内容前方，英文站通常为左侧；`inline-end`：右侧；`block-start`：上方；`block-end`：下方 |
| `tabs_width` | 左右布局时的标签列宽度，尺寸对象；它不是内容区宽度 |
| `tabs_justify_vertical` | 左右布局的标签排列：`start`、`center`、`end`、`stretch` |
| `tabs_justify_horizontal` | 上下布局的标签排列，同上；控件存在方向条件，不能假设桌面条件不成立时手机样式一定生成 |
| `title_alignment` | 标签文字对齐：`start`、`center`、`end` |
| `tabs_title_space_between` | 标签之间的间距，尺寸对象 |
| `tabs_title_spacing` | 标签列与内容区的间距，尺寸对象 |
| `padding` | 标签按钮内边距，DIMENSIONS；不是整个 widget 的高级 `_padding` |
| `tabs_title_border_radius` | 标签按钮圆角，DIMENSIONS |
| `horizontal_scroll` | `disable` 或 `enable`；不需要横向滚动时使用 `disable` |
| `breakpoint_selector` | `mobile` 等站点可用断点会触发原生 accordion 布局；`none` 禁用自动 accordion。按源交互选择，不默认把所有手机 Tab 改为 accordion |
| `title_typography_typography` | 自定义文字排版用 `custom`；字号、字重、行高等使用 `title_typography_` 前缀，省略字体家族字段 |
| `title_text_color` / `_hover` / `_active` | 普通、悬停、选中时的标签文字颜色，例如 `title_text_color_active` |
| `tabs_title_transition_duration` | 标签样式过渡时间，SLIDER；`size` 以秒表达，如 0.2 |
| `box_padding`、`box_border_radius` | 内容区内边距和圆角，DIMENSIONS，作用于直接子内容容器；应与容器自身设置保持一致 |

### 样式分组字段前缀

下列前缀来自该版本源码的 group control 名称，后缀遵守 Elementor 分组控件规则：

- 标签背景普通状态：`tabs_title_background_color_background: "classic"`、`tabs_title_background_color_color: "#FFFFFF"`。
- 悬停背景：`tabs_title_background_color_hover_background`、`tabs_title_background_color_hover_color`。
- 选中背景：`tabs_title_background_color_active_background`、`tabs_title_background_color_active_color`。
- 标签边框：`tabs_title_border_border: "solid"`、`tabs_title_border_width`、`tabs_title_border_color`；悬停和选中状态分别用 `tabs_title_border_hover_`、`tabs_title_border_active_` 前缀。
- 内容背景：`box_background_color_background`、`box_background_color_color`；内容边框使用 `box_border_` 前缀。

不要设置 `title_typography_font_family`，也不要通过 `__globals__` 或手写 CSS 强制字体。字号等设置保留，字体继承目标网站。

## CSS 写入同一 Tabs 元素的 Custom CSS

原生控件负责标签、内容容器和切换行为，也可保留它们能直接表达的样式。从源 HTML 迁移或为还原设计编写的 CSS，**全部放在该 Tabs widget 的 `settings.custom_css`**；不写 `<style>`、不写进标签或正文，也不另建 HTML 元素、全局样式或隐藏按钮来实现 Tab。

使用 `selector` 作为组件作用域。4.3.5 相关结构选择器：

| 选择器 | 对应结构 |
|---|---|
| `selector .e-n-tabs` | Tabs 内部布局总容器 |
| `selector .e-n-tabs-heading` | 标签列表 |
| `selector .e-n-tabs-heading > .e-n-tab-title` | 原生标签按钮 |
| `selector .e-n-tab-title[aria-selected="true"]` | 当前选中标签 |
| `selector .e-n-tab-title-text` | 标签文字 |
| `selector .e-n-tabs-content` | 内容区 |
| `selector .e-n-tabs-content > .e-con` | 每个原生内容容器 |

该版本开启优化标记后可能没有 `.elementor-widget-container` 包裹层。上面的局部后代选择器避开对这个可选包裹层的依赖；嵌套其他 Tabs 时需进一步限定当前层级，避免影响内部 Tabs。

以下是竖向标签、300px 内容区、手机端标签竖排在内容上方的补充 CSS 示例，写入同一 Tabs 的 `settings.custom_css`。原生方向分别设置为桌面 `inline-start`、手机 `block-start`，并将 `breakpoint_selector` 设为 `none`，以保留 Tab 交互：

```css
selector .e-n-tabs {
  min-width: 0;
}
selector .e-n-tabs-heading > .e-n-tab-title {
  width: 100%;
  min-height: 44px;
  overflow-wrap: anywhere;
  cursor: pointer;
}
selector .e-n-tabs-content {
  min-width: 0;
  max-width: 300px;
}
@media (max-width: 767px) {
  selector .e-n-tabs {
    flex-direction: column;
  }
  selector .e-n-tabs-heading {
    width: 100%;
    flex-basis: auto;
    flex-direction: column;
    align-items: stretch;
  }
  selector .e-n-tabs-content {
    width: 100%;
    max-width: 100%;
  }
}
selector .e-n-tab-title:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: -4px;
}
@media (prefers-reduced-motion: reduce) {
  selector .e-n-tab-title {
    transition: none !important;
  }
}
```

CSS 只调整布局与视觉，不接管原生切换、`aria-selected`、键盘操作或内容显隐。不用手写 JavaScript 重建这些行为。内容里的表格仍由其自己的独立 HTML 元素及该元素的 Custom CSS 管理。

## 兼容与核验边界

- 元素级 Custom CSS 是目标站能力要求。Pro 前端脚本加载只能证明插件前端功能在运行，不能单独证明编辑器有相应控件和权限；无法确认或不可用时说明限制，不能移到别处绕过主文件规定。
- 2026-11-04 的本地生成案例已检查：79 个元素的包装和复制回读、一个原生 nested-tabs、七个标签与七个内容容器、文案对应、默认字体、图片地址及表格 Custom CSS 作用域。
- 上述记录**尚未在目标 Elementor 编辑器实际粘贴和操作验证**。参考字段可复用，但不能称为已经验证兼容的模板；下次实际粘贴成功或发现问题时，再更新相应结论。
- 交付前核对数量和索引、重复项及元素 ID 唯一、中文导航器名称、已确认标签与正文、方向及手机行为、CSS 所属元素与作用域。实际环境可验证时再检查点击、键盘和渲染。

## 官方源码依据

- [4.3.5 nested-tabs.php](https://github.com/elementor/elementor/blob/4.3.5/modules/nested-tabs/widgets/nested-tabs.php)：`tab_content_container()`、`register_controls()`、`render_tab_titles_html()`、`render_tab_containers_html()`、`add_attributes_to_container()`、`render()`。
- [4.3.5 widget-nested-base.php](https://github.com/elementor/elementor/blob/4.3.5/modules/nested-elements/base/widget-nested-base.php)：`get_initial_config()`、`get_raw_data()`、子容器序列化。
- [4.3.5 frontend.scss](https://github.com/elementor/elementor/blob/4.3.5/modules/nested-tabs/assets/scss/frontend.scss)：原生结构类名、布局变量及内容显隐。
- [Elementor Custom CSS 官方说明](https://elementor.com/help/how-to-add-custom-css/)：元素级 Custom CSS 的使用入口。

上面是固定版本链接，不用 `main` 分支替代版本依据。旧版 `tabs` 的富文本结构不在此示例范围内，需要时单独核对目标版本。
