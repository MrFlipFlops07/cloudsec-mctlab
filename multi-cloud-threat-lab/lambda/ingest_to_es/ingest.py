#!/usr/bin/env python3
# ingest.py
import json, gzip, base64, os, requests, logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ES_ENDPOINT = os.environ.get("ES_ENDPOINT", "http://localhost:9200")
ES_INDEX = os.environ.get("ES_INDEX", "cloudtrail-events")

def decode_awslogs(data_b64_gz):
    compressed_payload = base64.b64decode(data_b64_gz)
    decompressed = gzip.decompress(compressed_payload)
    return json.loads(decompressed)

def index_doc(doc, index=ES_INDEX):
    url = f"{ES_ENDPOINT}/{index}/_doc"
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=doc, headers=headers, timeout=10)
        r.raise_for_status()
        return r.status_code
    except Exception as e:
        logger.exception("Failed to index doc: %s", e)
        return None

def lambda_handler(event, context):
    # event is the CloudWatch Logs subscription payload
    try:
        payload = event['awslogs']['data']
    except Exception:
        logger.error("Unexpected event format")
        return {"error":"bad event"}
    decoded = decode_awslogs(payload)
    # logEvents contain messages (CloudTrail JSON usually as message)
    for rec in decoded.get('logEvents', []):
        try:
            msg = rec.get('message')
            # attempt parse
            try:
                doc = json.loads(msg)
            except Exception:
                # fallback: store raw message
                doc = {"raw_message": msg}
            index_doc(doc)
        except Exception as e:
            logger.exception("error processing log event: %s", e)
    return {"status":"ok"}
