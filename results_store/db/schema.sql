CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY,
  app_id TEXT NOT NULL,
  app_type TEXT NOT NULL,
  dataset_version TEXT NOT NULL,
  git_commit TEXT NOT NULL,
  created_at TEXT NOT NULL,
  result_json TEXT NOT NULL
);
