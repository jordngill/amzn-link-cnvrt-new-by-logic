# (c) @AmznUsers | Jordan Gill

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6580477946:AAEo69sgCMbUid4Hi5UGcVphiwAbzaLr2fU")
API_ID = int(os.environ.get("API_ID", "12936189"))
API_HASH = os.environ.get("API_HASH", "7e24008e8ec33a397155b6a9d618497b")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001877793174"))
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1166670205").split())
DB_URL = os.environ.get("DB_URL", "mongodb+srv://gill1322:gill1322@amazondb.rqg93er.mongodb.net/?retryWrites=true&w=majority&appName=AmazonDB")
DB_NAME = os.environ.get("DB_NAME", "AmazonDB")
AMAZON_TLD = os.environ.get("AMAZON_TLD", "in")
AMAZON_TAG = os.getenv("AMAZON_TAG", "gillharyana0e-21")
FORWARD_CHANNEL_NUMBER = os.getenv("FORWARD_CHANNEL_NUMBER", -1002043723833)
BOT_TYPE_PUBLIC = os.getenv("BOT_TYPE_PUBLIC", "False").lower() == "True"
COOKIES = os.environ.get("COOKIES", 'ubid-acbin=260-2754458-7012255;x-acbin="8ZtF2K2r7?p?UQUgbSuQMu??lAkXupXz4gSwS@EuQbwyI8SJ?SWPH5h@2nKF3IkT";at-acbin=Atza|IwEBICnZ2qFj4l495oZSgjAeIt82hUBWDVadfSFeUnv7JjBxpwbqkccQj1zHc6HITg7r_783NsHI_iZXsd8xZflXnXZ-9FVtTjRYPvoqYVAoLlf4OqHvC5EJdoD1ZSUIRXO4u9KIolbKoiEahbWYpmIpw4zah88MwpkLtJt6sB3zLO5eubVFsCNWbtU9uQBVyUDnkJNF69bZYjUSetp27OgggsT2WfMZ-3rsP8qH-wauPzpJlg;lc-acbin=en_IN;sess-at-acbin="bXZvMD3QLCiKsTiD518DZyj4bqpIvEYCCdZXOqctOUU=";sst-acbin=Sst1|PQFPQZyK-PfdZkOj6rzHmMcoCWbaW5fz_sb61CDlRvMJHWoE4Z1vessVtn_Jmfn7jnaGr2Cwcj0f6Ri6P-qugvgSoQJagZLXQr38NuZi1EyvlXYcS4CJeIPpjEz9rVbHkDgMaZbmuKDIGDPZS1ghl7CLo-ZIkLtpGdBx80Ci9f5IvENUxSgsr0Y_r-HhZcnVu79PAWk0FDdeYHdKtvdXcm7k_7d-4Qucf6De5WFE_lsit545o5uFQ0bvwiWQShgaEVBxdU7yxQVrSxZiLq1xF3JJvMBR6WEANUqLmUI6Pzve71U')
BROADCAST_AS_COPY = os.getenv("BROADCAST_AS_COPY", "True").lower() == "true"
