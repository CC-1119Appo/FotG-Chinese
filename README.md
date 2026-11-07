# FotG简体中文包

《命运银河》（Fate of the Galaxy, FotG）的简体中文汉化包，适用于 FreeSpace Open。

## 内容

- `contents/data/tables/`
  - `tstrings.tbl`：任务简报、战役剧情、事件叙述、科技描述等全部中文文本
  - `strings.tbl` / `str_fotg_1-lcl.tbm`：引擎界面、选项、提示等
  - `zz_fotg_zh-tlc.tbm` / `zz_fotg_zh-lcl.tbm`：模块化覆盖表，避免加载顺序影响
  - `zz_fotg_zh-shp.tbm` / `zz_fotg_zh-wep.tbm`：舰船、武器显示名（按星战中文术语表）
  - `help.tbl`、`mainhall.tbl`、`rank.tbl`、`tips.tbl`、`medals.tbl`
  - `lua/0_GCW-sct.lua`：GCW 动态战役脚本中文版
- `contents/data/missions/`
  - GCW 战役名中文覆盖文件
  - Assault 模式单人任务副本（移除 Red Alert 标记以便在任务列表显示）

## 安装

1. 将本仓库的 `contents` 目录放到 FotG 的 SideMod 目录中（或作为 Knossos 的独立 mod 安装）。
2. 确保 `mod.json` 的 `parent` 指向 `FotG`。
3. 通过 Knossos 启动「FotG简体中文包」，不要直接启动本体。

字体文件因授权与体积原因未包含；如缺少中文字体，请从游戏本体或系统字体补充 `data/fonts`。

## 术语

舰船、武器、人物、地点等专有名词参照星战中文术语表（namelist）统一翻译。

## 说明

- 内部 `$Name` 保持英文，仅覆盖显示名，避免任务/脚本引用失效。
- 文本已适配 FSO 26.2.0 的 token 长度限制（技术标题 31 字节、帮助文本 128 字节）。
