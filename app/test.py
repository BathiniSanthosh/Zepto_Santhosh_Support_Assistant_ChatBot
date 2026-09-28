from transformers import AutoTokenizer
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"

AutoTokenizer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Success")