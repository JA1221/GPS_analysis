# GPS_analysis
 FinalProject - 1092無線感測網路協定與應用

 設備:
 1. 樹莓派 Raspberry Pi 3B+
 2. GPS接收模組(GY-NEO6MV2)

 檔案:
 1. 收集好的GPS原始資料 ./data/*.txt
 2. 預處理完的GPGSV資料 ./Out/*Out.txt
 3. 統計資料 ./Out/out.xlsx
 3. ML資料集 ./Out/out.csv
 4. ML程式碼(train & test) ./ML.py
 5. 訓練好的Model ./model.pkl
 6. FinalProject 主程式 ./project.py

 環境:
 1. Python 3.x
 2. Python套件: sklearn. joblib (pip install xxx)
 3. 指令要在專案路徑下執行

 執行:
 1. Python project.py
 2. 放入檔案:
    1. Menu - '選擇GPS DATA'
    2. 檔案拖曳到視窗裡
 3. 點擊衛星可以顯示資訊
 4. 顯示歷史資訊 : Menu - 'Satellite History'
 5. 顯示/隱藏干擾訊號的建築 : Menu - '顯示/隱藏建築物'