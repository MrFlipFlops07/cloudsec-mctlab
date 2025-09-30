 HEAD
#!/usr/bin/env python3
import os, requests, json, logging, boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ES_ENDPOINT = os.environ.get("ES_ENDPOINT", "http://localhost:9200")
ES_INDEX = os.environ.get("ES_INDEX", "cloudtrail-events")
PLAYBOOK_LAMBDA = os.environ.get("PLAYBOOK_LAMBDA", "mctlab-playbook")

lambda_client = boto3.client('lambda', region_name=os.environ.get("AWS_REGION", "us-east-1"))

def es_search(query):
    url = f"{ES_ENDPOINT}/{ES_INDEX}/_search"
    try:
        r = requests.get(url, json=query, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.exception("ES search failed: %s", e)
        return {"hits":{"hits":[]}}

def build_console_login_query():
    return {
      "query": {
        "bool": {
          "must": [
            {"match": {"eventName": "ConsoleLogin"}},
            {"match": {"responseElements.ConsoleLogin": "Success"}}
          ]
        }
      },
      "size": 50,
      "sort": [{"@timestamp": {"order": "desc"}}]
    }

def call_playbook(payload):
    try:
        lambda_client.invoke(FunctionName=PLAYBOOK_LAMBDA, InvocationType='Event', Payload=json.dumps(payload))
        logger.info("Invoked playbook with payload: %s", payload)
    except Exception as e:
        logger.exception("Failed to invoke playbook: %s", e)

def lambda_handler(event, context):
    q = build_console_login_query()
    res = es_search(q)
    hits = res.get('hits', {}).get('hits', [])
    logger.info("Found %d hits", len(hits))
    for h in hits:
        source = h.get('_source', {})
        src_ip = source.get('sourceIPAddress')
        user = source.get('userIdentity', {}).get('arn')
        # Simple whitelist: change to your trusted IPs / ranges
        if src_ip and not src_ip.startswith("203.0.113."):  # example reserved test net
            payload = {
                "action": "isolate",
                "source_ip": src_ip,
                "user": user,
                "evidence": source
            }
            call_playbook(payload)
    return {"checked": len(hits)}
 3185941 (Add full infra, lambdas, and docker-compose for multi-cloud threat detection lab)
