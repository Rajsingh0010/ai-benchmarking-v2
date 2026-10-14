from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    db_path: Path = Path(os.getenv("BENCHMARK_DB_PATH", "results_store/db/benchmark.sqlite3"))
    hardware_profile: str = os.getenv("HARDWARE_PROFILE", "local-cpu")
    git_commit: str = os.getenv("GIT_COMMIT", "local")


settings = Settings()
