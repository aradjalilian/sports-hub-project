from dotenv import load_dotenv
load_dotenv()

import os

api_key = os.environ.get("RESEND_API_KEY")

print("API key loaded:", bool(api_key))
print("Starts with re_:", api_key.startswith("re_") if api_key else False)