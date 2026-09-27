# 🇧🇷 SolidSign API - Caso de Uso: Documentos de Saúde (Receita Médica e correlatos) — Python

Este projeto demonstra a integração com a **SolidSign API** para assinar documentos de saúde (receita, atestado, exame, laudo): uma assinatura PDF única que embute o OID ICP-Brasil do tipo de documento + OID do profissional, mais rubrica visual — via KMS SolidSign.

## Endpoint

`POST /api/saude/sign-documento` — recebe `document` (PDF), `kmsCode`, `documentType` (`prescricao`/`atestado`/`exame`/`laudo`) e os dados do profissional (`professionalName`, `professionalRegistro`, `professionalUf`, `professionalEspecialidade`), retorna o PDF assinado.

## OIDs de tipo de documento (ICP-Brasil)

`prescricao`=`2.16.76.1.12.1.1`, `atestado`=`2.16.76.1.12.1.2`, `exame`=`2.16.76.1.12.1.3`, `laudo`=`2.16.76.1.12.1.4`.

## OIDs de categoria profissional

Padrão: médico (`2.16.76.1.4.2.2.*`, configurável em `.env`). Outras: farmacêutico `.3.*`, enfermeiro `.4.*`, nutricionista `.5.*`, fisioterapeuta `.7.*`, psicólogo `.8.*`, dentista `.12.*`.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn

## Como Executar

```bash
python -m venv venv && source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
cp .env.example .env   # edite com seu token
uvicorn main:app --port 8098 --reload
```

```
curl -X POST http://localhost:8098/api/saude/sign-documento \
  -F "document=@receita.pdf" -F "kmsCode=$KMS_CODE" -F "documentType=prescricao" \
  -F "professionalName=Fulano de Tal" -F "professionalRegistro=123456" \
  -F "professionalUf=SP" -F "professionalEspecialidade=Cardiologia" \
  -o receita-assinada.pdf
```

## Outros métodos de certificação

Para HSM em nuvem ou navegador (PKCS#1), use os mesmos parâmetros nos exemplos genéricos [`exemplo-python-integracao-pdf-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-pdf-cloud) e [`exemplo-python-integracao-pdf-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-pdf-pkcs1).

## Tratamento de Erros
O sistema loga o JSON detalhado de erro da SolidSign.

---

# 🇬🇧 SolidSign API - Use Case: Health Documents (Medical Prescription and related) — Python

This project demonstrates integrating with the **SolidSign API** to sign health documents (prescription, medical certificate, exam request, report): a single PDF signature embedding the ICP-Brasil document-type OID + professional OID, plus a visible rubric — via SolidSign's KMS.

## Endpoint

`POST /api/saude/sign-documento` — takes `document` (PDF), `kmsCode`, `documentType` and the professional's data, returns the signed PDF.

## Document-type OIDs (ICP-Brasil)

`prescricao`=`2.16.76.1.12.1.1`, `atestado`=`2.16.76.1.12.1.2`, `exame`=`2.16.76.1.12.1.3`, `laudo`=`2.16.76.1.12.1.4`.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn

## How to Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --port 8098 --reload
```

## Other certification methods

For cloud HSM or browser (PKCS#1) signing, apply the same parameters to [`exemplo-python-integracao-pdf-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-pdf-cloud) and [`exemplo-python-integracao-pdf-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-pdf-pkcs1).

## Error Handling
The system logs SolidSign's detailed error JSON.

---

# 🇪🇸 SolidSign API - Caso de Uso: Documentos de Salud (Receta Médica y afines) — Python

Este proyecto demuestra la integración con la **SolidSign API** para firmar documentos de salud: una única firma PDF que embute el OID del tipo de documento + OID del profesional, más rúbrica visual — vía KMS.

## Endpoint

`POST /api/saude/sign-documento` — recibe `document` (PDF), `kmsCode`, `documentType` y los datos del profesional, devuelve el PDF firmado.

## OIDs de tipo de documento (ICP-Brasil)

`prescricao`=`2.16.76.1.12.1.1`, `atestado`=`2.16.76.1.12.1.2`, `exame`=`2.16.76.1.12.1.3`, `laudo`=`2.16.76.1.12.1.4`.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn

## Cómo Ejecutar

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --port 8098 --reload
```

## Otros métodos de certificación

Para HSM en la nube o navegador (PKCS#1), aplique los mismos parámetros a [`exemplo-python-integracao-pdf-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-pdf-cloud) y [`exemplo-python-integracao-pdf-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-pdf-pkcs1).

## Gestión de Errores
El sistema registra el JSON detallado de errores de SolidSign.
