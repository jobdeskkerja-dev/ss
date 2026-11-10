import io
import os
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="SIPRES Smart School API", version="1.0.0")

REQUIRED_COLS = ["NIS", "Nama", "Kelas", "Alpa", "Menit_Terlambat", "Jumlah_Sanksi"]
ACCESS_CODE = os.getenv("SIPRES_ACCESS_CODE", "").strip()


DASHBOARD_HTML = '<!doctype html>\n<html lang="id">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <meta name="theme-color" content="#101a35">\n  <title>SIPRES | Smart School</title>\n  <link rel="preconnect" href="https://fonts.googleapis.com">\n  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>\n  <style>\n    :root{--navy:#101a35;--navy2:#1c2d59;--primary:#4f46e5;--muted:#64748b;--line:#e7ebf3;--bg:#f5f7fb;--green:#10b981;--yellow:#f59e0b;--red:#ef4444}\n    *{box-sizing:border-box}body{margin:0;background:var(--bg);font-family:Inter,system-ui,sans-serif;color:#172033}\n    .shell{max-width:1440px;margin:auto;padding:24px}\n    .hero{background:linear-gradient(120deg,#0f172a,#1e293b 55%,#312e81);border-radius:24px;padding:30px 34px;color:#fff;display:flex;gap:22px;align-items:center;box-shadow:0 18px 45px #17255420}\n    .logo{width:76px;height:76px;object-fit:contain;border-radius:15px;display:none}.logo-placeholder{width:76px;height:76px;border:1px dashed #ffffff66;border-radius:15px;display:grid;place-items:center;font-size:12px;color:#cbd5e1;text-align:center}\n    .tag{display:inline-block;color:#c7d2fe;background:#6366f166;border:1px solid #a5b4fc66;border-radius:30px;padding:6px 12px;font-size:10px;font-weight:800;letter-spacing:1px}\n    h1{font-size:clamp(25px,3vw,36px);margin:10px 0 7px;letter-spacing:-1px}.hero p{color:#cbd5e1;line-height:1.7;margin:0;max-width:850px;font-size:13px}\n    .hero-actions{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.btn{border:0;border-radius:11px;padding:11px 15px;font-weight:700;cursor:pointer;font-family:inherit}.btn-light{background:#fff;color:#172033}.btn-primary{background:linear-gradient(135deg,#4f46e5,#4338ca);color:#fff;box-shadow:0 5px 15px #4f46e544}.btn-ghost{background:#eef2ff;color:#4338ca}\n    .tabs{display:flex;gap:8px;overflow:auto;padding:18px 0 12px}.tab{white-space:nowrap;border:1px solid var(--line);background:#fff;color:#64748b;padding:11px 16px;border-radius:12px;font-weight:700;cursor:pointer}.tab.active{background:#eef2ff;color:#4338ca;border-color:#c7d2fe}\n    .panel{display:none}.panel.active{display:block}.section-title{font-size:19px;font-weight:800;margin:18px 0 5px}.sub{font-size:12px;color:var(--muted);margin:0 0 17px;line-height:1.6}\n    .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:19px;box-shadow:0 5px 18px #0f172a08}\n    .kpi-label{font-size:11px;color:#64748b;font-weight:800;text-transform:uppercase;letter-spacing:.5px}.kpi-icon{float:right;background:#f1f5f9;padding:8px;border-radius:10px}.kpi-value{font-size:30px;font-weight:800;letter-spacing:-1px;margin:13px 0 4px}.kpi-note{font-size:11px;color:#94a3b8}.accent{height:4px;width:40px;border-radius:5px;margin-top:14px}\n    .two-col{display:grid;grid-template-columns:minmax(300px, .9fr) minmax(0,1.6fr);gap:14px;margin-top:15px}.upload-box{border:1px dashed #cbd5e1;border-radius:14px;padding:17px;background:#fafbff}.upload-box input{width:100%;margin:12px 0}.hint{font-size:11px;color:#64748b;line-height:1.7}.status-msg{font-size:13px;line-height:1.6;white-space:pre-line;color:#334155;margin-top:12px}.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.chart{min-height:350px}\n    .table-wrap{overflow:auto;border:1px solid var(--line);border-radius:14px;background:#fff}table{border-collapse:collapse;width:100%;font-size:12px;white-space:nowrap}th{background:#f8fafc;color:#64748b;text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.5px}th,td{padding:12px 14px;border-bottom:1px solid #eef1f6}tbody tr{cursor:pointer}tbody tr:hover{background:#f5f7ff}.pill{display:inline-block;padding:5px 9px;border-radius:30px;font-weight:700;font-size:10px}.safe{background:#dcfce7;color:#166534}.sp1{background:#fef3c7;color:#92400e}.sp2{background:#fee2e2;color:#991b1b}\n    .detail{min-height:240px;white-space:pre-line;line-height:1.9;color:#475569;font-size:13px}.empty{padding:30px;text-align:center;color:#94a3b8;font-size:13px}.rules{line-height:1.9;font-size:13px;color:#475569}.rule{padding:15px;border:1px solid var(--line);border-radius:13px;margin:10px 0;background:#fff}.footer{text-align:center;padding:25px;color:#94a3b8;font-size:11px;border-top:1px solid var(--line);margin-top:25px}\n    .overlay{position:fixed;inset:0;background:#0f172acc;display:none;place-items:center;z-index:10;padding:20px}.overlay.show{display:grid}.modal{background:white;padding:25px;border-radius:18px;max-width:380px;width:100%}.modal input{width:100%;padding:12px;border:1px solid var(--line);border-radius:10px;margin:12px 0}\n    @media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}.two-col,.chart-grid{grid-template-columns:1fr}.hero{align-items:flex-start;flex-wrap:wrap}.hero-actions{margin-left:0;justify-content:flex-start}}\n    @media(max-width:560px){.shell{padding:14px}.hero{padding:22px}.logo,.logo-placeholder{width:58px;height:58px}.grid{gap:9px}.card{padding:14px}.kpi-value{font-size:24px}.hero p{font-size:12px}}\n  </style>\n</head>\n<body>\n<div class="shell">\n  <header class="hero">\n    <div>\n      <img id="logoPreview" class="logo" alt="Logo sekolah">\n      <div id="logoPlaceholder" class="logo-placeholder">LOGO<br>SEKOLAH</div>\n    </div>\n    <div style="flex:1;min-width:230px">\n      <span class="tag">SIPRES • SMART SCHOOL</span>\n      <h1>Dashboard Kehadiran Siswa</h1>\n      <p>Sistem Informasi Kehadiran & Kedisiplinan Siswa khusus Guru BK dan Wali Kelas. Pantau analitik kehadiran, deteksi dini siswa bermasalah, dan ambil tindakan preventif secara cepat dan terukur.</p>\n    </div>\n    <div class="hero-actions">\n      <label class="btn btn-light" for="logoFile">Unggah Logo</label><input id="logoFile" type="file" accept="image/png,image/jpeg" hidden>\n    </div>\n  </header>\n\n  <nav class="tabs">\n    <button class="tab active" data-tab="dashboard">📊 Dashboard & Analitik</button>\n    <button class="tab" data-tab="warning">⚠️ Pusat Peringatan BK</button>\n    <button class="tab" data-tab="database">🗂️ Database Seluruh Siswa</button>\n    <button class="tab" data-tab="guide">📖 Panduan & Aturan SP</button>\n  </nav>\n\n  <main>\n    <section id="dashboard" class="panel active">\n      <div class="section-title">Ringkasan Kinerja Sekolah</div>\n      <p class="sub">Indikator utama kedisiplinan berdasarkan data absensi yang diunggah.</p>\n      <div class="grid">\n        <div class="card"><span class="kpi-icon">👥</span><div class="kpi-label">Total Siswa</div><div class="kpi-value" id="kTotal">0</div><div class="kpi-note">Siswa terdata di sistem</div><div class="accent" style="background:#4f46e5"></div></div>\n        <div class="card"><span class="kpi-icon">📋</span><div class="kpi-label">Total Alpa</div><div class="kpi-value" id="kAlpa">0</div><div class="kpi-note">Akumulasi tanpa keterangan</div><div class="accent" style="background:#ef4444"></div></div>\n        <div class="card"><span class="kpi-icon">⏱️</span><div class="kpi-label">Menit Terlambat</div><div class="kpi-value" id="kMenit">0</div><div class="kpi-note">Akumulasi waktu terlambat</div><div class="accent" style="background:#f97316"></div></div>\n        <div class="card"><span class="kpi-icon">⚠️</span><div class="kpi-label">Total Pelanggaran</div><div class="kpi-value" id="kSanksi">0</div><div class="kpi-note">Akumulasi sanksi disiplin</div><div class="accent" style="background:#10b981"></div></div>\n      </div>\n      <div class="two-col">\n        <div class="card">\n          <div class="section-title" style="margin-top:0">📂 Import Data Absensi</div><p class="sub">Unggah laporan absensi format .xlsx</p>\n          <div class="upload-box">\n            <b>Pilih file Excel (.xlsx)</b><input id="excelFile" type="file" accept=".xlsx">\n            <button class="btn btn-primary" id="processBtn">🚀 Proses & Perbarui Dashboard</button>\n            <button class="btn btn-ghost" id="resetBtn">↺ Reset Tampilan</button>\n            <p class="hint">Kolom wajib: <b>NIS, Nama, Kelas, Alpa, Menit_Terlambat, Jumlah_Sanksi</b><br>Ukuran file maksimal 4 MB untuk deployment serverless.</p>\n          </div>\n          <div class="status-msg" id="statusMsg">Menunggu file Excel diunggah...</div>\n        </div>\n        <div class="card">\n          <div class="section-title" style="margin-top:0">📌 Hasil Evaluasi BK</div><p class="sub">Ringkasan rekomendasi penanganan siswa</p>\n          <div id="summary" class="status-msg">Belum ada data yang diproses.</div>\n        </div>\n      </div>\n      <div class="section-title">📈 Analitik & Statistik Visual</div><p class="sub">Grafik interaktif untuk membaca pola kehadiran dan kedisiplinan siswa.</p>\n      <div class="chart-grid">\n        <div class="card chart" id="statusChart"></div><div class="card chart" id="violationChart"></div>\n      </div>\n    </section>\n\n    <section id="warning" class="panel">\n      <div class="section-title">Pusat Peringatan Dini (Early Warning System)</div>\n      <p class="sub">Daftar siswa yang memerlukan perhatian khusus atau rekomendasi Surat Peringatan berdasarkan ambang batas pelanggaran.</p>\n      <div class="table-wrap" id="warningTable"><div class="empty">Unggah data absensi terlebih dahulu.</div></div>\n    </section>\n\n    <section id="database" class="panel">\n      <div class="section-title">Database Seluruh Siswa</div>\n      <p class="sub">Klik baris siswa pada tabel untuk melihat rincian kedisiplinan.</p>\n      <div class="two-col">\n        <div class="table-wrap" id="studentTable"><div class="empty">Belum ada data siswa.</div></div>\n        <div class="card"><div class="section-title" style="margin-top:0">🔎 Rincian Siswa Terpilih</div><div class="detail" id="studentDetail">Klik baris/nama siswa pada tabel sebelah kiri.</div></div>\n      </div>\n    </section>\n\n    <section id="guide" class="panel">\n      <div class="section-title">📘 Panduan Sistem Rekomendasi Surat Peringatan</div>\n      <p class="sub">Sistem menghitung rekomendasi status kedisiplinan secara otomatis berdasarkan parameter berikut.</p>\n      <div class="rule"><span class="pill safe">🟢 AMAN</span><p class="rules">Siswa belum melewati ambang batas kedisiplinan.</p></div>\n      <div class="rule"><span class="pill sp1">🟡 PERLU SP 1</span><ul class="rules"><li>Jumlah Alpa ≥ 3 hari</li><li>Akumulasi Menit Terlambat ≥ 40 menit</li><li>Jumlah Sanksi/Pelanggaran ≥ 2 kali</li></ul></div>\n      <div class="rule"><span class="pill sp2">🔴 PERLU SP 2</span><ul class="rules"><li>Jumlah Alpa ≥ 5 hari</li><li>Akumulasi Menit Terlambat ≥ 120 menit</li><li>Jumlah Sanksi/Pelanggaran ≥ 3 kali</li></ul></div>\n      <p class="hint">Catatan: status merupakan rekomendasi berbasis aturan pada sistem, bukan keputusan otomatis penerbitan surat peringatan. Guru BK/Wali Kelas tetap melakukan verifikasi.</p>\n    </section>\n  </main>\n  <footer class="footer"><b>SIPRES • Smart School</b> — Dashboard Analitik Kehadiran Siswa & Kedisiplinan Sekolah<br>Dibuat khusus untuk Guru Bimbingan Konseling dan Wali Kelas</footer>\n</div>\n\n<div class="overlay" id="accessOverlay"><div class="modal"><h3>🔐 Akses SIPRES</h3><p class="hint">Masukkan kode akses yang diberikan pengelola aplikasi.</p><input id="accessInput" type="password" placeholder="Kode akses"><button class="btn btn-primary" id="accessBtn" style="width:100%">Masuk</button><p class="hint" id="accessError"></p></div></div>\n\n<script>\nlet accessCode = "";\nlet currentData = null;\nconst $ = id => document.getElementById(id);\nconst fmt = n => Number(n || 0).toLocaleString("id-ID");\nconst esc = v => String(v ?? "").replace(/[&<>"\']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",\'"\':"&quot;","\'":"&#39;"}[c]));\nconst statusClass = s => s.includes("SP 2") ? "sp2" : s.includes("SP 1") ? "sp1" : "safe";\n\ndocument.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => {\n  document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));\n  document.querySelectorAll(".panel").forEach(x => x.classList.remove("active"));\n  btn.classList.add("active"); $(btn.dataset.tab).classList.add("active");\n  setTimeout(() => { if(currentData){ Plotly.Plots.resize("statusChart"); Plotly.Plots.resize("violationChart"); } }, 80);\n}));\n\n$("logoFile").addEventListener("change", e => {\n  const file=e.target.files[0]; if(!file)return;\n  const url=URL.createObjectURL(file); $("logoPreview").src=url;\n  $("logoPreview").style.display="block"; $("logoPlaceholder").style.display="none";\n});\n\nasync function checkConfig(){\n  try{\n    const r=await fetch("/api/health"); const d=await r.json();\n    if(d.access_protected) $("accessOverlay").classList.add("show");\n  }catch(e){ $("statusMsg").textContent="Tidak dapat terhubung ke API. Pastikan deployment Vercel selesai."; }\n}\n$("accessBtn").addEventListener("click",()=>{accessCode=$("accessInput").value.trim(); $("accessOverlay").classList.remove("show"); $("accessError").textContent="";});\n$("accessInput").addEventListener("keydown",e=>{if(e.key==="Enter")$("accessBtn").click();});\n\nfunction renderTable(rows, target, clickable=false){\n  if(!rows || !rows.length){$(target).innerHTML=\'<div class="empty">Tidak ada data.</div>\';return;}\n  const cols=["NIS","Nama","Kelas","Alpa","Menit_Terlambat","Jumlah_Sanksi","Status_SP"];\n  let out=\'<table><thead><tr>\'+cols.map(c=>`<th>${c.replaceAll("_"," ")}</th>`).join("")+\'</tr></thead><tbody>\';\n  rows.forEach((r,i)=>{\n    out+=`<tr ${clickable?`data-row="${i}"`:""}>`+cols.map(c=>`<td>${c==="Status_SP"?`<span class="pill ${statusClass(r[c])}">${esc(r[c])}</span>`:esc(r[c])}</td>`).join("")+\'</tr>\';\n  });\n  $(target).innerHTML=out+\'</tbody></table>\';\n  if(clickable) $(target).querySelectorAll("tbody tr").forEach(tr=>tr.addEventListener("click",()=>{\n    const r=rows[Number(tr.dataset.row)];\n    $("studentDetail").textContent=\n`🔍 DETAIL DATA SISWA TERPILIH\n----------------------------------------\n📌 Nama Lengkap  : ${r.Nama}\n🆔 NIS           : ${r.NIS}\n🏫 Kelas         : ${r.Kelas}\n📋 Total Alpa    : ${r.Alpa} hari\n⏱️ Keterlambatan : ${r.Menit_Terlambat} menit\n⚠️ Jumlah Sanksi : ${r.Jumlah_Sanksi} kali\n📊 Status        : ${r.Status_SP}`;\n  }));\n}\n\nfunction render(data){\n  currentData=data; const s=data.summary;\n  $("kTotal").textContent=fmt(s.total_siswa); $("kAlpa").textContent=fmt(s.total_alpa);\n  $("kMenit").textContent=fmt(s.total_menit); $("kSanksi").textContent=fmt(s.total_sanksi);\n  $("summary").textContent=`📊 RINGKASAN EVALUASI KEDISIPLINAN SEKOLAH\n\n👥 Total Siswa Terdata : ${s.total_siswa}\n🟢 Status Aman        : ${s.aman} siswa\n🟡 Rekomendasi SP 1    : ${s.sp1} siswa\n🔴 Rekomendasi SP 2    : ${s.sp2} siswa\n\n💡 Status dihitung otomatis berdasarkan ambang batas pelanggaran.`;\n  renderTable(data.warning,"warningTable",false);\n  renderTable(data.students,"studentTable",true);\n  const common={paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",font:{family:"Inter",color:"#64748b"},margin:{t:55,b:45,l:35,r:25},height:330};\n  Plotly.newPlot("statusChart",[{type:"pie",labels:data.charts.status_labels,values:data.charts.status_values,hole:.7,sort:false,\n    marker:{colors:["#10b981","#f59e0b","#ef4444"],line:{color:"#fff",width:3}},textinfo:"percent",textposition:"outside",\n    hovertemplate:"<b>%{label}</b><br>Jumlah: %{value} siswa<extra></extra>"}],\n    {...common,title:{text:"Distribusi Status Kedisiplinan Siswa"},annotations:[{text:`<b>${s.total_siswa}</b><br><span style="font-size:11px;color:#64748b">Total Siswa</span>`,x:.5,y:.5,showarrow:false,font:{size:20,color:"#1e293b"}}]},\n    {responsive:true,displayModeBar:false});\n  Plotly.newPlot("violationChart",[{type:"bar",x:data.charts.violation_labels,y:data.charts.violation_values,\n    marker:{color:["#ef4444","#f59e0b","#4f46e5"],cornerradius:8},text:data.charts.violation_values,textposition:"outside"}],\n    {...common,title:{text:"Statistik Jenis Pelanggaran"},yaxis:{title:"Jumlah Siswa",rangemode:"tozero",gridcolor:"#e2e8f0"}},\n    {responsive:true,displayModeBar:false});\n}\n\n$("processBtn").addEventListener("click",async()=>{\n  const file=$("excelFile").files[0];\n  if(!file){$("statusMsg").textContent="Pilih file Excel terlebih dahulu.";return;}\n  const btn=$("processBtn");btn.disabled=true;btn.textContent="Memproses...";\n  $("statusMsg").textContent="Sedang membaca dan menganalisis data...";\n  try{\n    const form=new FormData();form.append("file",file);\n    const r=await fetch("/api/analyze",{method:"POST",headers:accessCode?{"X-Access-Code":accessCode}:{},body:form});\n    const d=await r.json();if(!r.ok){if(r.status===401){$("accessOverlay").classList.add("show");$("accessInput").value="";}throw new Error(d.detail||"Gagal memproses file.");}\n    render(d);$("statusMsg").textContent="✅ Data berhasil dimuat. Dashboard telah diperbarui.";\n  }catch(e){$("statusMsg").textContent="❌ "+e.message;}\n  finally{btn.disabled=false;btn.textContent="🚀 Proses & Perbarui Dashboard";}\n});\n\n$("resetBtn").addEventListener("click",()=>{\n  currentData=null;$("excelFile").value="";$("statusMsg").textContent="Tampilan direset. Silakan unggah file baru.";\n  $("summary").textContent="Belum ada data yang diproses.";\n  ["kTotal","kAlpa","kMenit","kSanksi"].forEach(id=>$(id).textContent="0");\n  ["warningTable","studentTable"].forEach(id=>$(id).innerHTML=\'<div class="empty">Belum ada data.</div>\');\n  $("studentDetail").textContent="Klik baris/nama siswa pada tabel sebelah kiri.";\n  Plotly.purge("statusChart");Plotly.purge("violationChart");\n  $("statusChart").innerHTML="";$("violationChart").innerHTML="";\n});\ncheckConfig();\n</script>\n</body>\n</html>\n'

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/health")
@app.get("/api/health")
def health():
    return {"ok": True, "app": "SIPRES Smart School", "access_protected": bool(ACCESS_CODE)}


@app.post("/analyze")
@app.post("/api/analyze")
async def analyze_excel(
    file: UploadFile = File(...),
    x_access_code: str | None = Header(default=None),
):
    check_access(x_access_code)

    filename = (file.filename or "").lower()
    if not filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Format file harus .xlsx.")

    content = await file.read()
    # Batas lunak untuk menghindari upload besar pada fungsi serverless.
    if len(content) > 4 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Ukuran file melebihi 4 MB. Pecah atau kecilkan file Excel, lalu unggah kembali."
        )

    try:
        df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"File Excel tidak dapat dibaca: {exc}")

    df.columns = df.columns.astype(str).str.strip()
    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail="Kolom wajib belum ditemukan: " + ", ".join(missing)
        )
    if df.empty:
        raise HTTPException(status_code=400, detail="File Excel tidak berisi data siswa.")

    df["NIS"] = df["NIS"].fillna("").astype(str).str.strip()
    for col in ["Nama", "Kelas"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    for col in ["Alpa", "Menit_Terlambat", "Jumlah_Sanksi"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise HTTPException(
                status_code=400,
                detail=f"Kolom {col} memiliki data kosong atau bukan angka yang valid."
            )
        if (df[col] < 0).any():
            raise HTTPException(status_code=400, detail=f"Nilai pada kolom {col} tidak boleh negatif.")
        df[col] = df[col].astype(int)

    df["Status_SP"] = [
        evaluasi_status_sp(int(a), int(m), int(s))
        for a, m, s in zip(df["Alpa"], df["Menit_Terlambat"], df["Jumlah_Sanksi"])
    ]

    total_siswa = int(len(df))
    aman = int((df["Status_SP"] == "🟢 Aman").sum())
    sp1 = int((df["Status_SP"] == "🟡 Perlu SP 1").sum())
    sp2 = int((df["Status_SP"] == "🔴 Perlu SP 2").sum())

    warning = df[df["Status_SP"].isin(["🟡 Perlu SP 1", "🔴 Perlu SP 2"])].copy()
    if warning.empty:
        warning_rows: list[dict[str, Any]] = [{
            "NIS": "-", "Nama": "Luar biasa! Tidak ada siswa melewati ambang batas SP",
            "Kelas": "-", "Alpa": 0, "Menit_Terlambat": 0,
            "Jumlah_Sanksi": 0, "Status_SP": "🟢 Aman"
        }]
    else:
        warning_rows = warning[REQUIRED_COLS + ["Status_SP"]].to_dict(orient="records")

    students = df[REQUIRED_COLS + ["Status_SP"]].to_dict(orient="records")

    # Convert numpy/int-like values to JSON-safe Python values.
    for row in students + warning_rows:
        for key, value in list(row.items()):
            if pd.isna(value):
                row[key] = ""
            elif hasattr(value, "item"):
                row[key] = value.item()

    return JSONResponse({
        "summary": {
            "total_siswa": total_siswa,
            "total_alpa": int(df["Alpa"].sum()),
            "total_menit": int(df["Menit_Terlambat"].sum()),
            "total_sanksi": int(df["Jumlah_Sanksi"].sum()),
            "aman": aman,
            "sp1": sp1,
            "sp2": sp2,
        },
        "warning": warning_rows,
        "students": students,
        "charts": {
            "status_labels": ["Aman", "Perlu SP 1", "Perlu SP 2"],
            "status_values": [aman, sp1, sp2],
            "violation_labels": ["Alpa", "Terlambat", "Pelanggaran"],
            "violation_values": [
                int((df["Alpa"] > 0).sum()),
                int((df["Menit_Terlambat"] > 0).sum()),
                int((df["Jumlah_Sanksi"] > 0).sum()),
            ],
        },
    })
