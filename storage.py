import os
import json
import requests
import config

_cache = None

# Local fallback file
LOCAL_FILE = config.MAPPING_FILE


def load_mapping():
    """Load mapping from JSONBin or local file."""
    global _cache
    if _cache is not None:
        return _cache

    # 1. Try JSONBin.io
    if config.JSONBIN_API_KEY and config.JSONBIN_BIN_ID:
        try:
            url = f"https://api.jsonbin.io/v3/b/{config.JSONBIN_BIN_ID}/latest"
            headers = {"X-Master-Key": config.JSONBIN_API_KEY}
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json().get("record", {})
                _cache = data
                _save_local(data)
                return data
        except Exception as e:
            print(f"[STORAGE] JSONBin load error: {e}")

    # 2. Fallback to local file
    _cache = _load_local()
    return _cache


def save_mapping(mapping):
    """Save mapping to JSONBin and local file."""
    global _cache
    _cache = mapping
    _save_local(mapping)

    if config.JSONBIN_API_KEY and config.JSONBIN_BIN_ID:
        try:
            url = f"https://api.jsonbin.io/v3/b/{config.JSONBIN_BIN_ID}"
            headers = {
                "X-Master-Key": config.JSONBIN_API_KEY,
                "Content-Type": "application/json"
            }
            requests.put(url, headers=headers, json=mapping, timeout=5)
        except Exception as e:
            print(f"[STORAGE] JSONBin save error: {e}")


def invalidate_cache():
    global _cache
    _cache = None


def _load_local():
    try:
        if os.path.exists(LOCAL_FILE):
            with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"[STORAGE] Local read error: {e}")
    return {}


def _save_local(mapping):
    try:
        with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[STORAGE] Local save error: {e}")


def _make_key(mavzu: int, section: str) -> str:
    return f"m{mavzu}_{section.lower()}"


def add_message(mavzu: int, section: str, msg_id: int, caption: str = None) -> bool:
    """Add a message to mavzu + section. Returns True if added/updated."""
    key = _make_key(mavzu, section)
    mapping = load_mapping()
    if key not in mapping:
        mapping[key] = []

    changed = False
    if msg_id not in mapping[key]:
        mapping[key].append(msg_id)
        changed = True

    if caption is not None:
        if "_captions" not in mapping:
            mapping["_captions"] = {}
        mapping["_captions"][str(msg_id)] = caption
        changed = True

    if changed:
        save_mapping(mapping)
        return True
    return False


def remove_message(mavzu: int, section: str, msg_id: int) -> bool:
    key = _make_key(mavzu, section)
    mapping = load_mapping()
    if key in mapping and msg_id in mapping[key]:
        mapping[key].remove(msg_id)
        if not mapping[key]:
            del mapping[key]
        if "_captions" in mapping and str(msg_id) in mapping["_captions"]:
            del mapping["_captions"][str(msg_id)]
        save_mapping(mapping)
        return True
    return False


def clear_section(mavzu: int, section: str) -> bool:
    key = _make_key(mavzu, section)
    mapping = load_mapping()
    if key in mapping:
        msg_ids = mapping[key]
        del mapping[key]
        if "_captions" in mapping:
            for mid in msg_ids:
                mapping["_captions"].pop(str(mid), None)
        save_mapping(mapping)
        return True
    return False


def get_messages(mavzu: int, section: str) -> list:
    key = _make_key(mavzu, section)
    mapping = load_mapping()
    return mapping.get(key, [])


def get_available_sections(mavzu: int) -> list:
    """Return list of section keys for a topic that have at least 1 message."""
    mapping = load_mapping()
    available = []
    prefix = f"m{mavzu}_"
    for key, msgs in mapping.items():
        if key.startswith(prefix) and msgs:
            sec = key[len(prefix):]
            if sec in config.SECTIONS:
                available.append(sec)
    return available


def get_caption(msg_id: int):
    mapping = load_mapping()
    captions = mapping.get("_captions", {})
    return captions.get(str(msg_id))


def set_caption(msg_id: int, caption: str):
    mapping = load_mapping()
    if "_captions" not in mapping:
        mapping["_captions"] = {}
    mapping["_captions"][str(msg_id)] = caption
    save_mapping(mapping)


def list_all() -> dict:
    """Return dictionary of mavzu -> {section: count}."""
    mapping = load_mapping()
    result = {}
    for key, msgs in mapping.items():
        if key.startswith("m") and "_" in key and msgs:
            try:
                parts = key[1:].split("_", 1)
                mavzu_num = int(parts[0])
                sec = parts[1]
                if mavzu_num not in result:
                    result[mavzu_num] = {}
                result[mavzu_num][sec] = len(msgs)
            except Exception:
                pass
    return result
