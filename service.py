"""
[EN]    Signs a health document (prescription, medical certificate, exam request or report)
        with an ICP-Brasil health-sector document-type OID plus the professional's OID
        (registration/UF/specialty), and stamps a visible rubric — using a SolidSign
        KMS-custodied certificate (POST /solidsign/dsig/pdf/sign-kms).

[PT-BR] Assina um documento de saúde (receita, atestado, pedido de exame ou laudo) com o OID
        de tipo de documento de saúde ICP-Brasil mais o OID do profissional
        (registro/UF/especialidade), e estampa uma rubrica visível.
"""

import json
import logging
import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

DOCUMENT_TYPE_OID = {
    "prescricao": "2.16.76.1.12.1.1",
    "atestado": "2.16.76.1.12.1.2",
    "exame": "2.16.76.1.12.1.3",
    "laudo": "2.16.76.1.12.1.4",
}


def sign(
    content: bytes, filename: str, kms_code: str, document_type: str,
    professional_name: str, professional_registro: str, professional_uf: str, professional_especialidade: str,
) -> Optional[bytes]:
    document_type_oid = DOCUMENT_TYPE_OID.get(document_type)
    if document_type_oid is None:
        logger.error("Unknown documentType '%s'.", document_type)
        return None

    base_url = os.getenv("SOLIDSIGN_API_BASE_URL", "").rstrip("/")
    authorization = os.getenv("SOLIDSIGN_API_AUTHORIZATION", "")
    profile = os.getenv("SOLIDSIGN_SAUDE_PROFILE", "ADRB")
    hash_algorithm = os.getenv("SOLIDSIGN_SAUDE_HASH_ALGORITHM", "SHA256")
    prof_oid_registro = os.getenv("SOLIDSIGN_SAUDE_PROF_OID_REGISTRO", "")
    prof_oid_uf = os.getenv("SOLIDSIGN_SAUDE_PROF_OID_UF", "")
    prof_oid_especialidade = os.getenv("SOLIDSIGN_SAUDE_PROF_OID_ESPECIALIDADE", "")

    document_info_metadata = json.dumps({
        document_type_oid: "",
        prof_oid_registro: professional_registro,
        prof_oid_uf: professional_uf,
        prof_oid_especialidade: professional_especialidade,
    })
    signature_field_config = json.dumps({
        "pageNumber": int(os.getenv("SOLIDSIGN_SAUDE_RUBRIC_PAGE", "1")),
        "coordinateX": int(os.getenv("SOLIDSIGN_SAUDE_RUBRIC_X", "60")),
        "coordinateY": int(os.getenv("SOLIDSIGN_SAUDE_RUBRIC_Y", "60")),
        "width": int(os.getenv("SOLIDSIGN_SAUDE_RUBRIC_WIDTH", "200")),
        "height": int(os.getenv("SOLIDSIGN_SAUDE_RUBRIC_HEIGHT", "70")),
    })
    signature_text_config = json.dumps({
        "text": f"Dr(a). {professional_name} — CRM {professional_registro}/{professional_uf}",
        "fontSize": int(os.getenv("SOLIDSIGN_SAUDE_RUBRIC_FONT_SIZE", "9")),
    })

    sign_url = base_url + "/solidsign/dsig/pdf/sign-kms"
    headers = {"Authorization": authorization}
    files = {"document[0]": (filename, content, "application/pdf")}
    data = {
        "kmsCode": kms_code,
        "profile": profile,
        "hashAlgorithm": hash_algorithm,
        "documentInfoMetadata": document_info_metadata,
        "signatureFieldConfig[0]": signature_field_config,
        "signatureTextConfig[0]": signature_text_config,
    }

    try:
        resp = requests.post(sign_url, headers=headers, files=files, data=data, timeout=120)
        resp.raise_for_status()
        sign_resp = resp.json()

        documents = sign_resp.get("documents", [])
        if not documents:
            logger.error("SolidSign response had no documents.")
            return None

        doc = documents[0]
        links_obj = doc.get("_links") or {}
        download_url = (links_obj.get("self") or {}).get("href")
        if not download_url:
            download_url = next(
                (lnk["href"] for lnk in doc.get("links", []) if lnk.get("rel") == "self"), None,
            )
        if not download_url:
            logger.error("SolidSign response had no download link.")
            return None

        dl = requests.get(download_url, headers=headers, timeout=120)
        return dl.content if dl.status_code == 200 else None

    except requests.HTTPError as e:
        logger.error("SolidSign API error %s: %s", e.response.status_code, e.response.text)
    except Exception as e:
        logger.error("Unexpected error during health document signing: %s", e)

    return None
