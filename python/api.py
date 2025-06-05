from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import subprocess
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_INPUT = "python/data/produk.xlsx"
EXCEL_OUTPUT = "python/output/hasil.xlsx"
SCRAPER_SCRIPT = "python/main.py"


@app.post("/scrape")
def run_scraper(file: UploadFile = File(...)):
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        with open(EXCEL_INPUT, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = subprocess.run(
            ["python", SCRAPER_SCRIPT], capture_output=True, text=True
        )

        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)

        if result.returncode != 0:
            return JSONResponse(
                content={"error": "Scraper gagal dijalankan", "detail": result.stderr},
                status_code=500,
            )

        if not os.path.exists(EXCEL_OUTPUT):
            return JSONResponse(
                content={"error": "Scraping berhasil tapi file hasil tidak ditemukan"},
                status_code=500,
            )

        return JSONResponse(
            content={"message": "Scraping selesai. Siap diunduh."}, status_code=200
        )

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/download")
def download_result():
    try:
        if not os.path.exists(EXCEL_OUTPUT):
            return JSONResponse(
                content={"error": "File hasil tidak ditemukan."}, status_code=404
            )

        # Simpan path sebelum kirim response
        path_copy = EXCEL_OUTPUT

        # Setelah response dikirim, file akan otomatis dihapus
        return FileResponse(
            path_copy,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="hasilcuy.xlsx",
            background=lambda: os.remove(path_copy),
        )

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
