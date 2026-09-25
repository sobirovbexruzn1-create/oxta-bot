import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "8786504369:AAHrKNXz6hKeYfGRiPK68Llw3_TWd502StQ")

# Admin IDs (comma-separated, e.g. ADMIN_IDS=123456789,987654321)
_admin_raw = os.getenv("ADMIN_IDS", "7859182866")
ADMIN_IDS = [int(x.strip()) for x in _admin_raw.split(",") if x.strip().isdigit()]

# Sources (materials) channel ID (where teacher's videos/slides are uploaded)
SOURCES_CHANNEL_ID = int(os.getenv("SOURCES_CHANNEL_ID", "-1004340745564"))

# Public channel where posts with buttons will be published
PUBLIC_CHANNEL = os.getenv("PUBLIC_CHANNEL", "@RavonRivojlanish")

# JSONBin.io persistent storage
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY", "")
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID", "")

# Local fallback mapping file
MAPPING_FILE = os.path.join(os.path.dirname(__file__), "mapping.json")

# ══════════════════════════════════════════
# OXTA: 15 ta mavzu ro'yxati
# ══════════════════════════════════════════
OXTA_TOPICS = {
    1: "Kirish va jarrohlik asboblari",
    2: "Qo'l topografik anatomiyasi",
    3: "Oyoq topografik anatomiyasi",
    4: "Qo'l va oyoq operativ xirurgiyasi",
    5: "Amputatsiya va ekzartikulyatsiya",
    6: "Bosh (miya qismi) xirurgiyasi",
    7: "Bosh (yuz qismi) xirurgiyasi",
    8: "Bo'yin sohasi xirurgiyasi",
    9: "Ko'krak qafasi xirurgiyasi",
    10: "Ko'krak bo'shlig'i a'zolari",
    11: "Qorin sohasi xirurgiyasi",
    12: "Qorin bo'shlig'i a'zolari",
    13: "Ichaklar operativ xirurgiyasi",
    14: "Bel va qorin parda orti sohasi",
    15: "Tos sohasi anatomiyasi"
}

# ══════════════════════════════════════════
# Bo'limlar (Subsections)
# ══════════════════════════════════════════
SECTIONS = {
    "video": {
        "title": "📹 Video darslar",
        "btn": "📹 Video",
        "aliases": ["video", "v", "vid", "videolar"]
    },
    "praktika": {
        "title": "🔬 Praktika / Amaliyot",
        "btn": "🔬 Praktika",
        "aliases": ["praktika", "practice", "p", "amaliyot", "pr"]
    },
    "slayd": {
        "title": "📊 Taqdimot / Slaydlar",
        "btn": "📊 Slayd",
        "aliases": ["slayd", "slide", "s", "slaydlar", "prezentatsiya"]
    },
    "post": {
        "title": "📝 Postlar mundarijasi",
        "btn": "📝 Post",
        "aliases": ["post", "postlar"]
    },
    "konspekt": {
        "title": "📋 Konspektlar",
        "btn": "📋 Konspekt",
        "aliases": ["konspekt", "k", "konspektlar"]
    },
    "savollar": {
        "title": "❓ Savollar",
        "btn": "❓ Savollar",
        "aliases": ["savollar", "savol", "q"]
    },
    "test": {
        "title": "🎯 Testlar",
        "btn": "🎯 Test",
        "aliases": ["test", "testlar", "t"]
    }
}

# Mapping alias to canonical section key
SECTION_ALIASES = {}
for sec_key, info in SECTIONS.items():
    for alias in info["aliases"]:
        SECTION_ALIASES[alias.lower()] = sec_key
