# 全球衛星即時位置 Satellite Tracker

在 3D 地球上即時顯示一萬五千多顆現役衛星的位置，單純的靜態網頁，下載後不需安裝、不需伺服器，離線也能用。
線上網頁觀看 https://chichawang.github.io/satellite-tracker/
A static, offline-capable web page that shows 15,000+ active satellites moving around a 3D Earth in real time, with the Sun, Moon, Milky Way, day/night shading and country borders. The interface is in Traditional Chinese.

## 功能

**衛星**

- 顯示 CelesTrak 全部現役衛星（約 15,900 顆），位置以 SGP4 模型即時推算
- 兩種分類方式，可切換並個別開關
  - 依軌道：太空站、低軌（Starlink／其他）、中軌、GPS、其他導航、地球同步、高橢圓
  - 依用途：太空站、GPS、其他導航、氣象、軍用／情報、網路通訊星系、科學／技術試驗、地球觀測、通訊／廣播、業餘無線電／立方衛星、未分類
- 點選衛星（或從清單點選）顯示詳細資訊：即時經緯度、高度、速度、NORAD 編號、國際編號、軌道週期、傾角、離心率、近／遠地點、TLE 原始資料，並畫出軌道線
- 外部連結：N2YO、Heavens-Above、CelesTrak、Google、維基百科
- 以名稱或 NORAD 編號搜尋
- 國際太空站與天宮太空站有專屬標示
- 可把所有衛星投影到地表（星下點）

**地球與天空**

- 地球日夜分界，夜側顯示城市燈光
- 國界與海岸線、經緯線
- 真實星空與銀河背景，亮星標示中文名稱
- 太陽、月球（位置依時間計算，月相正確）
- 黃道面、月球軌道、地球到太陽與月球的連接線
- 太陽直射點與月下點在地表前後各 12 小時的軌跡

**操作**

- 滑鼠拖曳旋轉、滾輪縮放，支援觸控
- 時間可暫停或以 1×、10×、60×、600× 加速
- 選單在右側，可整個收合，也可分區塊收合

## 使用方式

1. 下載整個資料夾（GitHub 頁面上按 **Code → Download ZIP** 後解壓縮）
2. 用瀏覽器開啟 `index.html`

`index.html` 需要旁邊的 `lib/` 和 `data/` 資料夾，請整個資料夾一起搬移。

如果直接開啟後畫面空白，可以改用本機伺服器開啟：

```bash
python -m http.server 8000
```

然後在瀏覽器開啟 `http://localhost:8000`。

因為是純靜態網頁，也可以直接用 GitHub Pages 發布。

## 軌道資料更新

衛星位置是由軌道資料（TLE）推算的，資料越舊誤差越大，低軌衛星超過約兩週就會明顯偏離。

**自動更新（建議）**
網頁開啟時，如果手上的資料超過一天而且有網路，會自動從 CelesTrak 下載最新資料並存在瀏覽器裡。也可以按選單頂端的「⟳ 線上更新」手動更新。沒有網路時會使用資料夾內建的資料。

**更新資料夾內建的資料**
要把資料夾複製到不能連網的電腦之前，可以先更新內建資料：

```bash
python update-data.py
```

| 指令 | 作用 |
|---|---|
| `python update-data.py` | 下載最新軌道資料到 `data/tle.js` |
| `python update-data.py --file a.tle` | 改用已下載好的 TLE 檔 |
| `python update-data.py --groups` | 同時更新用途群組清單 `data/groups.js` |
| `python update-data.py --groups-only` | 只更新用途群組清單 |

只需要 Python 3 標準函式庫。Windows 也可以用 `update-data.ps1`（只更新軌道資料，不含用途群組）。

CelesTrak 限制同一份資料兩小時內不可重複下載，太頻繁會被暫時拒絕。

## 檔案結構

```
index.html          網頁本體（介面與全部程式）
update-data.py      更新資料的 Python 程式
update-data.ps1     更新軌道資料的 PowerShell 程式
lib/
  three.min.js      3D 繪圖函式庫
  satellite.min.js  SGP4 軌道推算函式庫
data/
  tle.js            衛星軌道資料
  groups.js         CelesTrak 用途群組的衛星編號
  earth.js          地球白天貼圖
  sky.js            星空、太陽、月球、夜間燈光貼圖
  world.js          國界與海岸線
```

圖片和資料都包成 `.js` 檔，是為了讓網頁直接用瀏覽器開啟（`file://`）時也能載入。

## 已知限制

- **只含現役衛星**：不包含已失效的衛星、火箭殘骸與太空碎片。
- **用途分類不是完全準確**：以 CelesTrak 官方群組為主，沒被收錄的衛星依名稱推定，約九百多顆無法判斷。「軍用／情報」大多是依 USA、COSMOS、遙感等命名慣例判斷。
- **太陽與月球放大顯示**：太陽放大 6 倍、月球放大 3 倍；太陽的方向正確但距離未按比例，月球的距離按比例。
- **太陽與月球位置為簡化公式**：太陽誤差約 0.01°，月球約 0.3°。
- **外部連結需要網路**。

## 資料來源與授權

| 內容 | 來源 | 授權 |
|---|---|---|
| 衛星軌道資料、用途群組 | [CelesTrak](https://celestrak.org/) | 見 CelesTrak 網站說明 |
| 3D 繪圖 | [three.js](https://threejs.org/) r149 | MIT |
| 軌道推算 | [satellite.js](https://github.com/shashwatak/satellite-js) 5.0.0 | MIT |
| 星空、太陽、月球、夜間燈光貼圖 | [Solar System Scope](https://www.solarsystemscope.com/textures/) | CC BY 4.0 |
| 國界與海岸線 | [Natural Earth](https://www.naturalearthdata.com/)，經 [world-atlas](https://github.com/topojson/world-atlas) | 公有領域／ISC |
| 地球白天貼圖 | three.js 範例 `earth_atmos_2048.jpg` | 隨 three.js 範例散布，原始來源請見 three.js 專案 |

### 本專案的授權

著作權人：王志嘉

本專案自己的程式碼（`index.html`、`update-data.py`、`update-data.ps1`）採用 [MIT 授權附加商業使用限制條款](LICENSE)：

- 個人、教學、研究等非商業用途可自由使用、修改與散布，只需保留著作權與授權聲明。
- **商業用途必須事先取得著作權人的書面同意**。請在本專案的 GitHub 儲存庫開立 issue 提出申請，說明使用者與用途；未獲回覆不視為同意。

`lib/` 與 `data/` 內的第三方函式庫與圖資，各自依上表的授權條款。
