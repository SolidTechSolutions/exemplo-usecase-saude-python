"""
[EN]    Health Documents (Receita Médica e correlatos) use case — single sign+rubric endpoint, KMS custody.
        Start: uvicorn main:app --port 8101 --reload

[PT-BR] Caso de uso Documentos de Saúde — endpoint único de assinatura+rubrica, custódia KMS.
        Iniciar: uvicorn main:app --port 8101 --reload
"""

import logging

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response

import service

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")

app = FastAPI(title="SolidSign — Health Documents Use Case")


@app.post("/api/saude/sign-documento")
async def sign_documento(
    document: UploadFile = File(...),
    kmsCode: str = Form(...),
    documentType: str = Form(...),
    professionalName: str = Form(""),
    professionalRegistro: str = Form(""),
    professionalUf: str = Form(""),
    professionalEspecialidade: str = Form(""),
):
    content = await document.read()
    signed = service.sign(
        content, document.filename, kmsCode, documentType,
        professionalName, professionalRegistro, professionalUf, professionalEspecialidade,
    )
    if signed:
        return Response(
            content=signed, media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{documentType}_signed.pdf"'},
        )
    return Response(content="Signing failed. Check logs.", status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8101)
