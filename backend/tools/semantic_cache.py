import hashlib
import json
import os

class SemanticCache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, topic):
        # Simple hash-based cache (replace with embedding for production)
        return hashlib.md5(topic.encode()).hexdigest()
    
    def get(self, topic):
        cache_key = self._get_cache_key(topic)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def set(self, topic, result):
        cache_key = self._get_cache_key(topic)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        with open(cache_file, 'w') as f:
            json.dump(result, f)