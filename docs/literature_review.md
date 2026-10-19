# Literature review (v1, 16 Oct 2026)

Purpose: separate what is already known from what this project might add. Each entry was checked against its abstract or publisher page on 16 Oct 2026. Findings are paraphrased.

## 1. Drought controls fire in Indonesia (well established)

- **Field, van der Werf & Shen (2009)**, *Nature Geoscience* 2, 185–188. Airport visibility 1960–2006 as a fire proxy: large fire events happen only when seasonal rain falls below a fairly sharp threshold. Kalimantan became fire-prone from the 1980s as land use changed; Sumatra earlier.
- **Field et al. (2016)**, *PNAS*. 2015 was the most severe season in the satellite era. Fire and smoke respond nonlinearly to dry-season rain below about 4 mm/day; sensitivity appears to have grown over Kalimantan. Calls for early-warning triggers tied to rainfall forecasts.
- **Spessa et al. (2015)**, *Natural Hazards and Earth System Sciences* 15, 429. ECMWF seasonal rainfall forecasts predict Kalimantan burnt area months ahead; El Niño years show a consistent positive bias.

**Implication for us:** our rounds 1–4 (El Niño → dry → fires) replicate these results with newer data. Not new.

## 2. The Indian Ocean Dipole and Sumatra

- **Iskandar et al. (2022)**, *Sustainability* 14(22), 15155. The 2019 extreme positive IOD caused a rainfall deficit over Indonesia and favoured peat fires in southern Sumatra; hotspots rose at the IOD peak.
- **Koplitz et al. (2016)**, *Environmental Research Letters* 11, 094023. The 2015 haze was enabled by both El Niño and a positive IOD.

**Implication:** the IOD–Sumatra link for 2019 is published. What we add is the contrast with 2023 (stronger El Niño, weaker Sumatra drought, fewer Sumatra fires, milder Singapore haze), if that contrast is not already in the literature (not yet found).

## 3. Which fires reach Singapore (model-based)

- **Reddington et al. (2014)**, *ERL* 9, 094006. For 2004–2009, southern Sumatra fires gave about 42–62% of fire-related PM2.5 in Singapore, central Sumatra 21–35%, Kalimantan about 14–15%.
- **Aouizerats et al. (2015)**, *Atmospheric Chemistry and Physics* 15, 363–373. In 2013, Sumatran fires were the main cause of raised aerosol in Singapore; fires explained about half the poor-air days modelled.
- **Koplitz et al. (2016)**. Adjoint (sensitivity) modelling links exposure to source grid cells; much of the 2015 excess mortality came from South Sumatra fires.
- **Djamil et al. (2017)**, EGU abstract. Singapore PSI in 2015 varied on 5-, 10- and 20-day cycles tied to large-scale moisture gyres that steer smoke.

**Implication:** the established view is that **Sumatra dominates Singapore's smoke**. Our 2026 observation (Kalimantan about 78% of detections, yet record Singapore PM2.5) sits awkwardly with that and needs a transport explanation. This is a potential contribution, but it rests on near-real-time data for one season.

## 4. Fire activity has fallen for a given drought (key confounder)

- **Sloan, Tacconi & Cattau (2021)**, *Mitigation and Adaptation Strategies for Global Change* 26, 32. In 627 target communities, fire in 2016–2019 averaged about 23% of expected; even dry 2019 reached about 70% of expected, and was delayed 30–50 days. Credits prevention efforts.
- **Sloan, Gaveau et al. (2022)**, "Declining severe fire activity on managed lands in Equatorial Asia", *Communications Earth & Environment*. For a given drought, fires in the late 2010s were less severe than in the early 2000s, mainly on managed lands.
- **Castro et al. (2026)**, *iScience* 29(6), 116041. Canal blocking in West and Central Kalimantan (2017–2022) reduced fires where blocks overlapped; best case spares up to 6.4% of burnt area.

**Implication:** our fire–rain correlations mix weather with a post-2015 policy regime. **Any analysis must control for the period (pre/post 2016) or detrend.** This is the main methodological gap in rounds 1–4.

## 5. Satellite detection issues

- **Sofan, Yulianto & Sakti (2022)**, *ISPRS Int. J. Geo-Information* 11(12), 601. For VIIRS in Indonesia, type-2 "static land sources" are mostly industrial sites, mines and flares, but the static-zone map also removed some real fires on peatland near rivers.

**Implication:** our finding that 13,963 South Sumatra detections in 2015 were type 2 is consistent with that warning, now for MODIS and at large scale. Counting all detections is defensible; we should quantify the effect rather than assert it.

## What this project could add (to be confirmed by further search)

1. An observation-only, fully reproducible check of the whole chain (ocean index → rain → fires → Singapore PM2.5) with independent data at each link, updated to 2026. Mostly replication; value is reproducibility and recency.
2. Controlling for the post-2015 policy regime when estimating the rain → fire and fire → Singapore links.
3. The 2019 versus 2023 contrast and the 2026 Kalimantan-dominated season against the Sumatra-dominates view.
4. Size of the MODIS type-2 issue in peat years.

## Not yet searched

Palm oil prices and fire (paper 2); statistical seasonal forecasts of Singapore PSI specifically; post-2020 MODIS orbit drift effects on detection counts.

## Sources

- Field et al. 2009: https://doi.org/10.1038/NGEO443
- Field et al. 2016: https://pmc.ncbi.nlm.nih.gov/articles/PMC4995960
- Spessa et al. 2015: https://nhess.copernicus.org/articles/15/429/2015/
- Iskandar et al. 2022: https://doi.org/10.3390/su142215155
- Koplitz et al. 2016: https://doi.org/10.1088/1748-9326/11/9/094023
- Reddington et al. 2014: https://dspace.mit.edu/handle/1721.1/92792
- Aouizerats et al. 2015: https://acp.copernicus.org/articles/15/363/2015/
- Djamil et al. 2017: https://meetingorganizer.copernicus.org/EGU2017/EGU2017-14180.pdf
- Sloan, Tacconi & Cattau 2021: https://doi.org/10.1007/s11027-021-09965-2
- Sloan, Gaveau et al. 2022: https://doaj.org/article/95586aee87c34c80bb9d9e93240ff0da
- Castro et al. 2026: https://doi.org/10.1016/j.isci.2026.116041
- Sofan et al. 2022: https://www.mdpi.com/2220-9964/11/12/601
