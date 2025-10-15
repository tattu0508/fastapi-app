from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    try:
        # CSVファイルを読み込み
        df = pd.read_csv(file.file)

        # 欠損値の数
        missing = df.isnull().sum().to_dict()

        # 基本統計量（数値列のみ）
        stats = df.describe().T  # 転置して列ベースに
        stats = stats[["mean", "50%", "std", "min", "max"]]
        stats.rename(columns={"50%": "median"}, inplace=True)

        stats_dict = stats.to_dict(orient="index")

        return JSONResponse(content={
            "row_count": len(df),
            "column_count": len(df.columns),
            "missing_values": missing,
            "statistics": stats_dict
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# 実行用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
