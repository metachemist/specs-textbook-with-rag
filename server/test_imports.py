# server/test_imports.py
import sys

print(f"Testing imports on Python {sys.version}")

try:
    import qdrant_client
    print("✅ Qdrant Client loaded successfully")
except ImportError as e:
    print(f"❌ Qdrant Failed: {e}")

try:
    import openai
    print("✅ OpenAI loaded successfully")
except ImportError as e:
    print(f"❌ OpenAI Failed: {e}")

try:
    import psycopg2
    print("✅ Psycopg2 (Neon) loaded successfully")
except ImportError as e:
    print(f"❌ Psycopg2 Failed: {e}")