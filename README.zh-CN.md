# 雾霾成因研究

[English](README.md)

**2016 年以来，同样的降雨下印尼烧得少多了；但厄尔尼诺年的夏天之后，火季照样更干、火更多，新加坡的雾霾也更重。**

论文在这里（英文，13 页，6 张图；2026 年 10 月 19 日修订）：[docs/paper_climate_fire_singapore_haze_2026-10-16.pdf](docs/paper_climate_fire_singapore_haze_2026-10-16.pdf)

## v2（2026 年 11 月）

v2 的起因是 2026 年 10 月 28 日 Dr Sean Sloan（温哥华岛大学）的来信。Sloan 本人的工作（Sloan et al. 2022, *Communications Earth & Environment* 3:207, doi 10.1038/s43247-022-00522-6）按"火灾事件"（fire events）度量火的严重程度，用火季降雨作控制变量。他给了两条建议：(1) 用"火辐射功率总和"（FRP sum）代替火点计数来衡量火势；(2) 降雨不只取火季，往前推 1 到 2 个月累加，因为降雨的作用是非线性的而且跨越更长窗口。v2 同时复现了 Sloan 的事件方法在我们两个岛上的趋势分析。

主要数字全部来自冻结的结论报告，没有额外估计或手算：

- **Step 0，Sloan 事件方法的复现。** 用他写死的事件定义，我们在自己的岛框里构造出的"严重事件"年序列，和他 Dryad 上发表的事件对应——苏门答腊 Pearson r = 0.9995，加里曼丹 r = 0.99998；18 个季节的总数相差不到 1.5%。
- **Q1，2002–2019 复现 Sloan 的趋势。** 两个岛的严重事件占比都在下降（苏门答腊 −11.7%，加里曼丹 −17.7%），方向上和 Sloan 四个区域的范围（−19 到 −27%）一致。非常严重事件的占比在加里曼丹下降了 −30.1%（落在他的范围内），但苏门答腊是 +2.3%（bootstrap 区间很宽）。
- **Q2，延长到 2025 年。** 控制 Jul–Dec 降雨后，每年严重事件占比的系数苏门答腊为 −0.0038（p = 0.0028，17 年下降 −22.5%），加里曼丹为 −0.0041（p = 0.00004，下降 −21.5%）。T1–T6 共 6 项确认性检验在 Holm 校正后全部显著。
- **Q3，用 Sloan 的两条建议重跑 v1 的雨火关系。** 不管用 FRP 总和还是检测数，不管降雨取火季还是从 6 月累加，结果都成立。Aug–Oct FRP 总和在降雨每少 1 毫米/日时是原来的 1.59 倍（苏门答腊）和 1.47 倍（加里曼丹）；按 Jun–Oct 总降雨算，每少 100 毫米时是 1.51 倍和 1.36 倍。两岛的 Aug–Oct FRP 总和和新加坡 Aug–Oct 平均 PM2.5 的 Spearman 相关系数是 0.93（2016–2025 年，10 个季节）。

完整报告：[docs/2026-11-02_v2_conclusions.md](docs/2026-11-02_v2_conclusions.md)。冻结计划：[docs/research_plan_v2.md](docs/research_plan_v2.md)。

## 主要数字（v1）

5 项预先定好的检验，经 Holm 多重比较校正后全部显著。

| 环节 | 结果 | 年份 |
|---|---|---|
| 厄尔尼诺（6 至 8 月 ONI）与加里曼丹 8 至 10 月降雨 | r = −0.79 | 1979 至 2025 |
| 印度洋偶极子与苏门答腊降雨（控制厄尔尼诺） | DMI 每高 1 °C，降雨少 1.7 毫米/日 | 1979 至 2025 |
| 降雨与火点数（控制政策时期） | 降雨每少 1 毫米/日，苏门答腊火点约为 1.55 倍，加里曼丹约为 1.44 倍 | 2001 至 2025 |
| 2016 年后、同样降雨下的火点（断点设在 2016 年） | 苏门答腊少约 77%，加里曼丹少约 47%（断点放在 2008 至 2021 年之间时，分别少 49% 至 79% 和 18% 至 47%） | 2001 至 2025 |
| 火点数与新加坡 PM2.5 | Spearman ρ = 0.88 | 2016 至 2025（10 个季节） |

## 局限

v1：

- 6 至 8 月的指数要到 9 月才公布。这赶在 9、10 月之前（2001 至 2025 年，8 至 10 月的火点有 67% 出现在这两个月），但那时火季已经开始了。
- 2016 年后火点降幅的大小取决于断点放在哪一年，降雨效应则基本不变。
- 新加坡这一环只有 10 个季节的数据，不含 2015 年。
- 检验用的数据我之前已经探索过，所以这不算预注册研究。
- 结果是逐年相关，不能证明因果，也不预测 2027 年。
- 这是我的个人项目，没有经过同行评审。

v2：

- 证据来自相关性，24 个季节（新加坡那一环只有 10 个）。
- 研究计划是在看过 Aug–Oct 火点数和 FRP 总和之后才写的，所以不算预注册研究（见计划里的诚实声明）。
- 降雨用的是 2.5° GPCP 数据，每个岛只有 3 个格点。CHIRPS 和 VIIRS 的检验在计划里写了但没有跑。
- 降雨在模型里是线性的。LOWESS 曲线显示火能量随 Jul–Dec 降雨逐渐下降、高降雨段略有平缓，看不出明显阈值，但没有专门做阈值检验。
- 苏门答腊的"非常严重事件占比"复现结果是唯一和 Sloan 方向相反的一项。

本仓库和我的 AI4Climate 参赛项目 `sg-haze-window` 是两回事，这里的结果不会用到那个产品里。

## 目录

| 路径 | 内容 |
|---|---|
| `data/raw/` | 原始 API 返回文件，原样保存，只读不改，清洗全部在代码里做。用 `SHA256SUMS.txt` 可以检查文件有没有被改过（`cd data/raw && sha256sum -c SHA256SUMS.txt`）。 |
| `data/external/sloan_dryad/` | 手动下载的 Sloan Dryad 事件表（doi 10.5061/dryad.msbcc2g1t）。zip 包 202 MB，超过 GitHub 上限，所以不进 git。 |
| `src/fetch.py` | 下载原始数据（已存在的文件会跳过）。 |
| `src/analyse.py` | 第 1 轮：计算 SOI、季节降雨和新加坡雾霾指标，做相关分析。 |
| `src/analyse_r2.py` | 第 2 轮：用官方 ONI 交叉核对，加入印度洋偶极子。读取第 1 轮结果，需在 `analyse.py` 之后运行。 |
| `src/analyse_r3.py` | 第 3 轮：换成 GPCP 降雨（与 ERA5 相互独立）重新检验。在 `analyse_r2.py` 之后运行，需要 `netCDF4`。 |
| `src/fetch_firms.py` | 下载 NASA FIRMS MODIS 火点，Aug–Oct 窗口（v1）。密钥从 `FIRMS_MAP_KEY` 读取，不保存在任何文件里。 |
| `src/fetch_firms_v2.py` | 下载 NASA FIRMS MODIS 火点，1 Jun–31 Jan 窗口、2002–2025（v2 事件构建需要边缘月份）。同样从 `FIRMS_MAP_KEY` 读密钥。 |
| `src/analyse_r4.py` | 第 4 轮：干旱 → 火点 → 新加坡 PM2.5。在 `analyse_r3.py` 之后运行。 |
| `src/plot_r4.py` | 绘制 `results/fires_r4.png`。 |
| `src/confirmatory.py` | 按 `docs/research_plan_v1.md` 做主检验和稳健性检验。在 `analyse_r4.py` 之后运行，需要 `statsmodels`。 |
| `src/fire_months.py` | 计算 8 至 10 月火点在各月的占比（论文里时间点的说法来自这里）。 |
| `src/posthoc_checks.py` | 收到评审意见后补做的检验（负二项模型、一阶差分、平稳性），不在冻结的研究计划内。 |
| `src/plot.py` | 绘制 `results/enso_haze.png`。 |
| `src/v2_step0.py` | 用 Sloan 定义从 FIRMS 检测构建事件，并和 Dryad 表核对。**需要** Sloan 的 Dryad 数据放在 `data/external/sloan_dryad/`。 |
| `src/v2_q3.py` | 用 Sloan 的两条建议重跑 v1 的雨火关系（FRP 总和 + 累加降雨）。直接用仓库里已有的数据，不需要 Dryad。 |
| `src/v2_stage2.py` | v2 Step 1 复现、T1–T2 确认性检验、Holm 校正、稳健性检验和探索性分析。通过 `v2_step0` 的事件构建用到 Dryad 数据。 |
| `src/v2_figures.py` | 画 Step 0 复现图，供 `docs/2026-11-02_v2_conclusions.md` 配图使用。只读 `results/` 目录里的 CSV，不重跑任何模型。 |
| `results/` | 当前代码的输出。要更新就重跑代码，不要手改。 |
| `docs/` | 论文 PDF、冻结的研究计划（v1 和 v2）、文献综述、v2 的结论和结果说明，以及每轮 v1 分析的记录。 |
| `LICENSE` | 本仓库代码和文字采用 MIT 许可证。原始数据沿用各自的许可（见下文）。 |

## 复现

v1：

```
python src/analyse.py data/raw results
python src/analyse_r2.py data/raw results
python src/analyse_r3.py data/raw results
python src/analyse_r4.py data/raw results
python src/plot_r4.py results
python src/confirmatory.py results
python src/fire_months.py data/raw results
python src/plot.py results
python src/posthoc_checks.py results
```

v2，在 v1 之后跑（v2 的事件构建复用 v1 的 FIRMS 火点文件）：

1. **Dryad 数据（手动下载，202 MB，超过 GitHub 上限）。** 从 Sloan 的 Dryad 仓库（doi 10.5061/dryad.msbcc2g1t）下载 `doi_10_5061_dryad_msbcc2g1t__v20220828.zip`，核对 SHA256，解压到 `data/external/sloan_dryad/`：

   ```
   curl -LO https://datadryad.org/api/v2/files/.../download
   sha256sum doi_10_5061_dryad_msbcc2g1t__v20220828.zip
   # 应为: 0b76226376a13cc8212df0f07041597cd169fba9c7cbdcd8cb6541e80a789e3b
   mkdir -p data/external/sloan_dryad
   unzip doi_10_5061_dryad_msbcc2g1t__v20220828.zip -d data/external/sloan_dryad
   ```

2. **FIRMS 密钥（从环境变量读取，绝不写入任何文件）。** 在 shell 里设置 `FIRMS_MAP_KEY`。`src/fetch_firms_v2.py` 需要它。`src/v2_step0.py` 和 `src/v2_stage2.py` 读 v2 火点文件但不调用 FIRMS API。

3. **脚本运行顺序：**

   ```
   python src/fetch_firms_v2.py data/raw/firms_v2
   python src/v2_step0.py data/raw data/external/sloan_dryad results
   python src/v2_q3.py data/raw results
   python src/v2_stage2.py data/raw results data/external/sloan_dryad
   python src/v2_figures.py results
   ```

   `v2_q3.py` 不依赖 Dryad 数据，只要 v1 火点到位就可以提前跑。`v2_step0.py` 和 `v2_stage2.py` 都需要 Dryad 表；`v2_stage2.py` 还需要 `fetch_firms_v2.py` 下载的 v2 火点。`v2_figures.py` 只需要前面脚本产出的 `results/` 文件。

需要 Python 3，以及 pandas、numpy、scipy、matplotlib、netCDF4、statsmodels。

## 许可与署名

本仓库的代码、记录和论文采用 MIT 许可证（`LICENSE`），版权归 Zhang Lin Si Cheng。

`data/raw/` 里的文件是第三方数据的副本，不在 MIT 许可范围内，各自沿用下表列出的条款。如果复用，请注明原始来源：

- 新加坡 PSI 和 PM2.5：数据来自 data.gov.sg 的 PSI 数据集，于 2026 年 10 月 16 日获取，依据 Singapore Open Data Licence 1.0 版提供。
- ERA5 降雨和气压：Open-Meteo.com 提供的天气数据（CC BY 4.0），基于哥白尼气候变化服务（C3S）的 ERA5 再分析。
- ONI、DMI 和 GPCP：NOAA 物理科学实验室（PSL）。DMI 背后的 HadISST 是英国气象局数据。GPCP 请引用 Adler et al. (2003)。
- 火点：NASA FIRMS（2001 至 2025 年用 MODIS 标准产品，2026 年用近实时产品）。
- Sloan 事件数据：许可请去 Dryad 页面核实（doi 10.5061/dryad.msbcc2g1t）。

## 数据来源

| 数据 | 来源 | 本仓库覆盖范围 | 许可 |
|---|---|---|---|
| 逐日平均海平面气压、逐日降水（ERA5 再分析） | Open-Meteo 历史天气 API | 1950-01-01 至 2026-10-10，8 个点（见下） | CC BY 4.0；非商业用途免费 |
| ONI（CPC，ERSST v6，3 个月滑动平均；文件注明 "as of 09/7/2026"） | NOAA PSL `psl.noaa.gov/data/correlation/oni.data`，由 Toni 手动下载，保存为 `noaa_psl_oni.data` | 1950 年 1 月至 2026 年 8 月（中心月） | 美国政府数据 |
| 偶极子模态指数 DMI（HadISST1.1；2026 年 7 月 25 日生成，最近几个月为初步值） | NOAA PSL `psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data`，由 Toni 手动下载，保存为 `noaa_psl_dmi_had_long.data` | 1870 年 1 月至 2026 年 5 月 | NOAA PSL；HadISST 为英国气象局数据，需署名 |
| GPCP v2.3 月降水，2.5°（卫星 + 雨量站；2021 年 11 月起为临时版） | NOAA PSL `downloads.psl.noaa.gov/Datasets/gpcp/precip.mon.mean.nc`，由 Toni 手动下载，保存为 `noaa_psl_gpcp_v2.3_precip.mon.mean.nc` | 1979 年 1 月至 2026 年 6 月 | NOAA PSL；引用 Adler et al. 2003（文件内有引文） |
| MODIS 火点，Aug–Oct 2001–2025 和近实时 2026（v1） | NASA FIRMS 区域 API，范围东经 100 至 116.5 度、南纬 5 度至北纬 2.3 度，2026 年 10 月 16 日用 Toni 的 MAP_KEY 下载，存放在 `data/raw/firms/` | 2001 至 2025 年每年 8 月 1 日至 10 月 31 日；2026 年 8 月 1 日至 10 月 15 日 | NASA 开放数据；引用 FIRMS |
| MODIS 火点，1 Jun–31 Jan 2002–2025（v2 事件构建） | NASA FIRMS 区域 API，范围同上，2026 年 11 月 2 日下载，存放在 `data/raw/firms_v2/` | 2002 年 6 月 1 日至 2026 年 1 月 31 日 | NASA 开放数据；引用 FIRMS |
| Sloan 事件表，2002–2019 | Dryad doi 10.5061/dryad.msbcc2g1t，版本 2022 年 8 月 28 日，手动下载 | Sloan 省份级事件和检测点，本地按我们的岛框筛选 | 去 Dryad 页面查 |
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
- v2 事件构建用 MODIS 正弦投影、1 公里等面积格、8 近邻连接，所有 MODIS 检测类型都纳入。只保留 Jul–Dec 引燃的事件；事件可以跨到 1 月（这一点和 Sloan 的"事件不跨年"不同）。

## 已知数据问题（保留，不填补）

- NEA API 没有 2016 年以前的数据，所以新加坡序列里没有 2015 年雾霾。
- NEA 有 20 天返回"data not found"：2019-08-09、08-15、09-06、09-10、09-11、09-14、09-15、09-21、09-25、09-26、10-02、10-17、10-18；2021-10-01 至 10-04、10-25；2023-10-08、10-31。2019 年有几天缺失正好在雾霾高峰，所以 2019 年的雾霾被低估。另有一些日子不足 24 个小时读数。
- ERA5 最近几个月是初步值，之后可能修订。ERA5 的热带降雨有偏差；Field et al. 基于 TRMM 的 4 毫米/日阈值只作参考。
- 2026 年降雨数据不完整（到 10 月 10 日），所以 2026 年只用于"相同日期窗口"的对比（8 月 1 日至 10 月 10 日）。
- 2026 年 11 月 2 日下载的 v2 FIRMS 文件里有 9 个空文件（0 行数据），都出现在雨季窗口。详见 `results/v2_step0_empty_firms_v2.csv`。
