# Elementor 原生 Accordion：结构、设置与 Custom CSS

核对日期：2026-11-04。适用依据为 Elementor **4.3.5** 官方组件及前端交互源码；相同版本和已覆盖字段优先复用，其他版本或新增控件按实际导出或对应版本源码核对。

## 组件与内容对应

- 使用 `widgetType: "nested-accordion"`；标题重复项保存在 `settings.items`，正文保存在直接子容器 `elements` 中。
- `settings.items[i]` 对应 `elements[i]`。数量与顺序必须相同；调整标题顺序时同步调整正文容器。
- 每个重复项使用唯一 `_id`，每个元素使用独立唯一 `id`；两者不需要相等。
- 重复项的 `item_title` 为网页标题；`element_css_id` 为可选 CSS ID，不是正文容器的 Elementor ID。
- 正文容器继续使用原生 text-editor、heading、image 等组件，均设置中文导航器名称。`nested-accordion` 不属于禁止使用的 `e-*` 原子元素。
- 旧版 `accordion` 使用重复项中的 `tab_title`、`tab_content`，与嵌套组件结构不同；按目标站实际能力选用，不混用字段。

## 已核对的设置

| 设置 | 正确写法及用途 |
|---|---|
| `default_state` | `expanded` 表示首项默认展开；`all_collapsed` 表示全部收起 |
| `max_items_expended` | `one` 表示每次展开一项；`multiple` 允许多项展开。字段拼写按源码保留 |
| `n_accordion_animation_duration` | SLIDER 对象；4.3.5 转换参考值为 `{"unit":"ms","size":200,"sizes":[]}`，即 0.2 秒 |
| `title_tag` | 按页面层级选 `h3`、`h4` 或 `div` 等合法标签 |
| `accordion_item_title_position_horizontal` | `start`、`center`、`end`、`stretch`；`stretch` 可让标题与图标分居两端 |
| `accordion_item_title_icon_position` | `start` 或 `end` |
| `accordion_item_title_icon` | 展开图标对象，例如 `{"value":"fas fa-plus","library":"fa-solid"}` |
| `accordion_item_title_icon_active` | 收起图标对象，例如 `{"value":"fas fa-minus","library":"fa-solid"}` |
| `accordion_item_title_space_between` | 条目之间的距离，使用尺寸对象 |
| `accordion_item_title_distance_from_content` | 标题与正文之间的距离，使用尺寸对象 |
| `accordion_padding`、`content_padding` | 标题与正文的原生 DIMENSIONS 控件，包含 unit、四边值及 isLinked |
| `title_typography_*` | 标题排版组；可设置字号、字重、行高，省略字体家族字段以继承网站字体 |
| `faq_schema` | 按内容性质决定；普通产品选项、定制说明设置 `no` |

200ms 是本项目已核对的转换参考配置，不是 Elementor 官方默认值，也不是所有版本的固定要求。源设计要求其他时长或其他默认展开项时，核对目标版本的原生实现再设置。

### 最小结构示例

这是一个 widget 片段，可作为元素数组的一项。实际生成时重新生成唯一 ID；标题与正文按用户已确认内容填写。

```json
{
  "id": "ac000001",
  "elType": "widget",
  "widgetType": "nested-accordion",
  "isInner": false,
  "settings": {
    "_title": "原生手风琴：产品选项",
    "items": [
      {"_id": "ad00001", "item_title": "Materials", "element_css_id": ""},
      {"_id": "ad00002", "item_title": "Sizing", "element_css_id": ""}
    ],
    "default_state": "expanded",
    "max_items_expended": "one",
    "n_accordion_animation_duration": {"unit": "ms", "size": 200, "sizes": []},
    "title_tag": "h4",
    "faq_schema": "no",
    "accordion_item_title_position_horizontal": "stretch",
    "accordion_item_title_icon_position": "end",
    "accordion_item_title_icon": {"value": "fas fa-plus", "library": "fa-solid"},
    "accordion_item_title_icon_active": {"value": "fas fa-minus", "library": "fa-solid"},
    "accordion_item_title_space_between": {"unit": "px", "size": 10, "sizes": []},
    "title_typography_typography": "custom",
    "title_typography_font_size": {"unit": "px", "size": 16, "sizes": []},
    "title_typography_font_weight": "600",
    "custom_css": "selector .e-n-accordion-item { border-radius: 4px; }"
  },
  "elements": [
    {
      "id": "ac000002", "elType": "container", "isInner": true,
      "settings": {"_title": "材质选项正文", "content_width": "full"},
      "elements": [
        {
          "id": "ac000003", "elType": "widget", "widgetType": "text-editor", "isInner": false,
          "settings": {"_title": "材质说明", "editor": "<p>Leather colours and finishes.</p>"},
          "elements": []
        }
      ]
    },
    {
      "id": "ac000004", "elType": "container", "isInner": true,
      "settings": {"_title": "尺寸选项正文", "content_width": "full"},
      "elements": [
        {
          "id": "ac000005", "elType": "widget", "widgetType": "text-editor", "isInner": false,
          "settings": {"_title": "尺寸说明", "editor": "<p>Length and width options.</p>"},
          "elements": []
        }
      ]
    }
  ]
}
```

## Custom CSS

迁移或补充的手风琴 CSS 写入**同一个 Accordion widget 的 `settings.custom_css`**，并用 `selector` 限定作用域。原生控件能表达的样式可继续保留；避免对同一属性作无理由的重复覆盖。

以下示例调整条目边框、选中背景、hover 与焦点，原生控件继续负责间距、排版、图标和正文容器样式：

```css
selector .e-n-accordion-item {
  border: 1px solid #DDDEE0;
  border-radius: 4px;
  background: #FFFFFF;
  transition: background-color .2s, border-color .2s;
}
selector .e-n-accordion-item > .e-n-accordion-item-title,
selector .e-n-accordion-item > .e-con {
  border: 0;
}
selector .e-n-accordion-item[open] {
  background: #F4F2ED;
  border-color: #A8977B;
}
selector .e-n-accordion-item-title:focus-visible {
  outline: 2px solid #7F715C;
  outline-offset: -5px;
}
@media (hover: hover) and (pointer: fine) {
  selector .e-n-accordion-item:hover {
    background: #F4F2ED;
    border-color: #7F715C;
  }
}
@media (prefers-reduced-motion: reduce) {
  selector .e-n-accordion-item {
    transition: none;
  }
}
```

- 标题与图标结构使用 `.e-n-accordion-item-title-header`、`.e-n-accordion-item-title-text`、`.e-n-accordion-item-title-icon`；正文容器为条目的直接 `.e-con` 子元素。
- 保留原生对 `open`、内容显隐、动画高度及键盘操作的控制。嵌套多层 Accordion 时，进一步限定选择器层级，避免外层样式影响内层。
- CSS 的减少动态效果规则只控制 CSS 动效；原生 JavaScript 动画需要按目标版本另外验证。
- 使用元素级 Custom CSS 前确认目标站有相应控件与权限；Pro 前端脚本存在不能单独证明编辑器权限可用。

## 验证范围

检查标题与正文对应、默认展开状态、单项／多项模式、动画尺寸值及单位，并测试展开、收起、逐项切换、重复点击、键盘与手机布局。

本参考的 4.3.5 结构及控件已核对官方源码；200ms、单项展开配置已用同版本前端交互代码在本地验证。只有实际粘贴并操作目标编辑器后，才能声称目标编辑器交互已验证。包装脚本与剪贴板往返校验属于独立检查。

## 官方依据

- [4.3.5 nested-accordion.php](https://github.com/elementor/elementor/blob/4.3.5/modules/nested-accordion/widgets/nested-accordion.php)：组件名称、重复项字段、原生控件、按索引输出正文、默认展开状态及图标。
- [4.3.5 nested-accordion.js](https://github.com/elementor/elementor/blob/4.3.5/modules/nested-accordion/assets/js/frontend/handlers/nested-accordion.js)：点击、展开数量和动画时长单位处理。
- [4.3.5 frontend.scss](https://github.com/elementor/elementor/blob/4.3.5/modules/nested-accordion/assets/scss/frontend.scss)：结构类名、展开状态与内容显隐。
