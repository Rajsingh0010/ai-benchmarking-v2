import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from metrics_engine.cv_metrics.detection import evaluate_detection_records
from metrics_engine.llm_metrics.generation import evaluate_llm_records

cv = [{"predictions":[{"box":[0,0,10,10],"label":"vehicle","score":.95}],
       "truth":[{"box":[0,0,10,10],"label":"vehicle"}], "slices":["daylight"]}]
llm = [{"question":"What color is the sky?","answer":"blue","ground_truth":"blue",
        "context":["The sky appears blue during the day."], "category":"factual",
        "faithfulness":.95, "answer_relevance":.9, "latency_ms":120}]
print(json.dumps({"cv": evaluate_detection_records(cv), "llm": evaluate_llm_records(llm)}, indent=2))
