from typing import Callable, Optional, Any
import redis
from redis.commands.search.field import VectorField, TextField
import numpy as np
from sentence_transformers import SentenceTransformer
import uuid
import json
import re
import time

class SemanticCache:
    def __init__(
        self,
        redisHost: str = "localhost",
        redisPort: int = 6379,
        indexName: str = "outlineIndex",
        vectorField: str = "embedding",
        topicField: str = "topic",
        outputField: str = "output",
        modelName: str = "sentence-transformers/all-MiniLM-L6-v2",
        dim: int = 384,
        distanceMetric: str = "COSINE"
    ):
        print("init: connecting to redis")
        self.r = redis.Redis(host=redisHost, port=redisPort, decode_responses=False)
        self.indexName = indexName
        self.vectorField = vectorField
        self.topicField = topicField
        self.outputField = outputField
        self.dim = dim
        self.distanceMetric = distanceMetric
        print("init: loading embedding model")
        self.model = SentenceTransformer(modelName)
        print("init: creating index")
        self.initIndex()
        print("init: ready")

    def normalizeTopic(self, text: str) -> str:
        print(f"normalizeTopic: raw={text}")
        t = text.lower().strip()
        t = re.sub(r"[^\w\s]", "", t)
        t = re.sub(r"\s+", " ", t)
        print(f"normalizeTopic: normalized={t}")
        return t

    def embed(self, text: str) -> bytes:
        print(f"embed: encoding text={text}")
        vec = self.model.encode([text], convert_to_numpy=True)[0].astype(np.float32)
        print("embed: embedding generated")
        return vec.tobytes()

    def initIndex(self):
        print("initIndex: attempting index creation")
        try:
            schema = [
                VectorField(
                    self.vectorField,
                    "HNSW",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": self.dim,
                        "DISTANCE_METRIC": self.distanceMetric,
                    }
                ),
                TextField(self.topicField)
            ]
            self.r.ft(self.indexName).create_index(schema)
            print("initIndex: new index created")
        except Exception as e:
            print(f"initIndex: index exists or failed, ignoring. error={e}")

    def semanticLookup(self, query: str, threshold: float = 0.85, k: int = 1) -> Optional[Any]:
        print(f"semanticLookup: query={query}")
        norm = self.normalizeTopic(query)
        qvec = self.embed(norm)

        knnQuery = f"*=>[KNN {k} @{self.vectorField} $vec AS score]"
        params = {"vec": qvec}

        print("semanticLookup: performing vector search")
        try:
            from redis.commands.search.query import Query
            q = Query(knnQuery).return_fields(self.topicField, self.outputField, "score").sort_by("score").dialect(2)
            res = self.r.ft(self.indexName).search(q, query_params=params)

        except Exception as e:
            print(f"semanticLookup: search failed error={e}")
            return None

        if len(res.docs) == 0:
            print("semanticLookup: no docs found")
            return None

        doc = res.docs[0]
        rawScore = float(doc.score)
        similarity = 1 - rawScore
        print(f"semanticLookup: rawScore={rawScore}, similarity={similarity}")

        if similarity >= threshold:
            print("semanticLookup: similarity threshold met, returning cached")
            outBytes = getattr(doc, self.outputField)
            try:
                return json.loads(outBytes)
            except Exception:
                try:
                    return outBytes.decode()
                except Exception:
                    return outBytes

        print("semanticLookup: below threshold, miss")
        return None

    def saveToCache(self, topic: str, output: Any, ttl: Optional[int] = None):
        print(f"saveToCache: saving topic={topic}")
        norm = self.normalizeTopic(topic)
        vec = self.embed(norm)
        key = f"outline:{uuid.uuid4().hex}"
        outputJson = json.dumps(output)

        mapping = {
            self.topicField: norm,
            self.outputField: outputJson,
            self.vectorField: vec
        }

        self.r.hset(key, mapping=mapping)
        print(f"saveToCache: saved with key={key}")

        if ttl:
            self.r.expire(key, ttl)
            print(f"saveToCache: ttl applied {ttl}")

    def getOrGenerate(
        self,
        topic: str,
        generatorFn: Callable[[], Any],
        threshold: float = 0.85,
        ttl: Optional[int] = None,
        k: int = 1
    ) -> Any:
        print(f"getOrGenerate: topic={topic}")
        cached = self.semanticLookup(topic, threshold=threshold, k=k)

        if cached is not None:
            print("getOrGenerate: cache hit")
            return cached

        print("getOrGenerate: cache miss, generating")
        result = generatorFn()

        try:
            json.loads(result)
            out = result
        except Exception:
            out = result

        self.saveToCache(topic, out, ttl=ttl)
        print("getOrGenerate: new result cached")
        return out
