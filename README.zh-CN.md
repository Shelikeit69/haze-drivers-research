# 雾霾成因研究

[English](README.md)

**2016 年以来，同样的降雨下印尼烧得少多了；但厄尔尼诺年的夏天之后，火季照样更干、火更多，新加坡的雾霾也更重。**

论文在这里（英文，12 页，6 张图）：[docs/paper_climate_fire_singapore_haze_2026-10-16.pdf](docs/paper_climate_fire_singapore_haze_2026-10-16.pdf)

## 主要数字

5 项预先定好的检验，经 Holm 多重比较校正后全部显著。

| 环节 | 结果 | 年份 |
|---|---|---|
| 厄尔尼诺（6 至 8 月 ONI）与加里曼丹 8 至 10 月降雨 | r = −0.79 | 1979 至 2025 |
| 印度洋偶极子与苏门答腊降雨（控制厄尔尼诺） | DMI 每高 1 °C，降雨少 1.7 毫米/日 | 1979 至 2025 |
| 降雨与火点数（控制政策时期） | 降雨每少 1 毫米/日，苏门答腊火点约为 1.55 倍，加里曼丹约为 1.44 倍 | 2001 至 2025 |
| 2016 年后、同样降雨下的火点 | 苏门答腊少约 77%，加里曼丹少约 47% | 2001 至 2025 |
| 火点数与新加坡 PM2.5 | Spearman ρ = 0.88 | 2016 至 2025（10 个季节） |

## 局限

- 6 至 8 月的指数要到 9 月才公布。这赶在 9、10 月之前（2001 至 2025 年，8 至 10 月的火点有 67% 出现在这两个月），但那时火季已经开始了。
- 新加坡这一环只有 10 个季节的数据，不含 2015 年。
- 检验用的数据我之前已经探索过，所以这不算预注册研究。
- 结果是逐年相关，不能证明因果，也不预测 2027 年。
- 这是我的个人项目，没有经过同行评审。

本仓库和我的 AI4Climate 参赛项目 `sg-haze-window` 是两回事，这里的结果不会用到那个产品里。

## 目录

| 路径 | 内容 |
|---|---|
| `data/raw/` | 原始 API 返回文件，原样保存，只读不改，清洗全部在代码里做。用 `SHA256SUMS.txt` 可以检查文件有没有被改过（`cd data/raw && sha256sum -c SHA256SUMS.txt`）。 |
| `src/fetch.py` | 下载原始数据（已存在的文件会跳过）。 |
| `src/analyse.py` | 第 1 轮：计算 SOI、季节降雨和新加坡雾霾指标，做相关分析。 |
| `src/analyse_r2.py` | 第 2 轮：用官方 ONI 交叉核对，加入印度洋偶极子。读取第 1 轮结果，需在 `analyse.py` 之后运行。 |
| `src/analyse_r3.py` | 第 3 轮：换成 GPCP 降雨（与 ERA5 相互独立）重新检验。在 `analyse_r2.py` 之后运行，需要 `netCDF4`。 |
| `src/fetch_firms.py` | 下载 NASA FIRMS MODIS 火点。密钥从环境变量 `FIRMS_MAP_KEY` 读取，不保存在任何文件里。 |
| `src/analyse_r4.py` | 第 4 轮：干旱 → 火点 → 新加坡 PM2.5。在 `analyse_r3.py` 之后运行。 |
| `src/plot_r4.py` | 绘制 `results/fires_r4.png`。 |
| `src/confirmatory.py` | 按 `docs/research_plan_v1.md` 做主检验和稳健性检验。在 `analyse_r4.py` 之后运行，需要 `statsmodels`。 |
| `src/fire_months.py` | 计算 8 至 10 月火点在各月的占比（论文里时间点的说法来自这里）。 |
| `src/plot.py` | 绘制 `results/enso_haze.png`。 |
| `results/` | 当前代码的输出。要更新就重跑代码，不要手改。 |
| `docs/` | 论文 PDF、冻结的研究计划、文献综述，以及每轮分析的记录。 |
| `LICENSE` | 本仓库代码和文字采用 MIT 许可证。原始数据沿用各自的许可（见下文）。 |

## 复现

```
python src/analyse.py data/raw results
python src/analyse_r2.py data/raw results
python src/analyse_r3.py data/raw results
python src/analyse_r4.py data/raw results
python src/plot_r4.py results
python src/confirmatory.py results
python src/fire_months.py data/raw results
python src/plot.py results
```

需要 Python 3，以及 pandas、numpy、scipy、matplotlib、netCDF4、statsmodels。只有要补充新数据时才需要重新下载（`python src/fetch.py data/raw`），已有文件不会被覆盖。

## 许可与署名

本仓库的代码、记录和论文采用 MIT 许可证（`LICENSE`），版权归 Zhang Lin Si Cheng。

`data/raw/` 里的文件是第三方数据的副本，不在 MIT 许可范围内，各自沿用下表列出的条款。如果复用，请注明原始来源：

- 新加坡 PSI 和 PM2.5：数据来自 data.gov.sg 的 PSI 数据集，于 2026 年 10 月 16 日获取，依据 Singapore Open Data Licence 1.0 版提供。
- ERA5 降雨和气压：Open-Meteo.com 提供的天气数据（CC BY 4.0），基于哥白尼气候变化服务（C3S）的 ERA5 再分析。
- ONI、DMI 和 GPCP：NOAA 物理科学实验室（PSL）。DMI 背后的 HadISST 是英国气象局数据。GPCP 请引用 Adler et al. (2003)。
- 火点：NASA FIRMS（2001 至 2025 年用 MODIS 标准产品，2026 年用近实时产品）。

## 数据来源（2026 年 10 月 16 日下载）

| 数据 | 来源 | 本仓库覆盖范围 | 许可 |
|---|---|---|---|
| 逐日平均海平面气压、逐日降水（ERA5 再分析） | Open-Meteo 历史天气 API | 1950-01-01 至 2026-10-10，8 个点（见下） | CC BY 4.0；非商业用途免费 |
| ONI（CPC，ERSST v6，3 个月滑动平均；文件注明 "as of 09/7/2026"） | NOAA PSL `psl.noaa.gov/data/correlation/oni.data`，由 Toni 手动下载，保存为 `noaa_psl_oni.data` | 1950 年 1 月至 2026 年 8 月（中心月） | 美国政府数据 |
| 偶极子模态指数 DMI（HadISST1.1；2026 年 7 月 25 日生成，最近几个月为初步值） | NOAA PSL `psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data`，由 Toni 手动下载，保存为 `noaa_psl_dmi_had_long.data` | 1870 年 1 月至 2026 年 5 月 | NOAA PSL；HadISST 为英国气象局数据，需署名 |
| GPCP v2.3 月降水，2.5°（卫星 + 雨量站；2021 年 11 月起为临时版） | NOAA PSL `downloads.psl.noaa.gov/Datasets/gpcp/precip.mon.mean.nc`，由 Toni 手动下载，保存为 `noaa_psl_gpcp_v2.3_precip.mon.mean.nc` | 1979 年 1 月至 2026 年 6 月 | NOAA PSL；引用 Adler et al. 2003（文件内有引文） |
| MODIS 火点（2001 至 2025 年 MODIS_SP；2026 年 MODIS_NRT） | NASA FIRMS 区域 API，范围东经 100 至 116.5 度、南纬 5 度至北纬 2.3 度，2026 年 10 月 16 日用 Toni 的 MAP_KEY 下载 | 2001 至 2025 年每年 8 月 1 日至 10 月 31 日；2026 年 8 月 1 日至 10 月 15 日 | NASA 开放数据；引用 FIRMS |
| 分区 PSI 和 24 小时 PM2.5，逐小时 | NEA，经 data.gov.sg 实时 API（`/v2/real-time/api/psi?date=`） | 2016 至 2025 年每年 8 月 1 日至 10 月 31 日；2026 年 8 月 1 日至 10 月 15 日 | Singapore Open Data Licence；注明来源，不得暗示官方身份 |

ERA5 取点（请求的纬度、经度；Open-Meteo 会对齐到最近的网格，实际网格记录在每个 JSON 里）：

- SOI 站点：达尔文 (-12.46, 130.84)，塔希提 (-17.53, -149.57)
- 苏门答腊：廖内 (0.50, 101.50)，占碑 (-1.60, 103.60)，南苏门答腊 (-3.00, 104.80)
- 加里曼丹：西加 (-0.50, 109.50)，中加 (-2.20, 113.90)，南加 (-3.30, 114.60)

## 方法说明

- 从第 3 轮起，主分析用官方 ONI 配 GPCP 降雨。第 3 轮发现，SOI 之所以看起来比 ONI 好，部分是因为 SOI 和 ERA5 降雨出自同一个数据源。
- 第 1 轮用的是本仓库自己算的 SOI，因为当时工作环境连不上 NOAA 网站，到第 2 轮才加入官方 ONI 做交叉核对。SOI 用 Troup 公式，基于 ERA5 月平均的塔希提减达尔文气压，基准期 1981 至 2010 年。负值表示厄尔尼诺。它不是澳大利亚气象局发布的官方 SOI。
- 新加坡指标每年都用 5 个分区重新计算，因为 2024 年起 API 不再提供 `national` 字段。PSI 取各区最大值（NEA 全国 PSI 的定义）；PM2.5 取该小时有读数的各区平均。
- 季节降雨 = 每个岛 3 个点在 8 至 10 月的平均，单位毫米/日。只要缺一天，该季节就留空。

## 已知数据问题（保留，不填补）

- NEA API 没有 2016 年以前的数据，所以新加坡序列里没有 2015 年雾霾。
- NEA 有 20 天返回"data not found"：2019-08-09、08-15、09-06、09-10、09-11、09-14、09-15、09-21、09-25、09-26、10-02、10-17、10-18；2021-10-01 至 10-04、10-25；2023-10-08、10-31。2019 年有几天缺失正好在雾霾高峰，所以 2019 年的雾霾被低估。另有一些日子不足 24 个小时读数。
- ERA5 最近几个月是初步值，之后可能修订。ERA5 的热带降雨有偏差；Field et al. 基于 TRMM 的 4 毫米/日阈值只作参考。
- 2026 年降雨数据不完整（到 10 月 10 日），所以 2026 年只用于"相同日期窗口"的对比（8 月 1 日至 10 月 10 日）。
