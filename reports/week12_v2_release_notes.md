# v2.0 Release Notes

v2 turns the v1 evaluation engine into a more usable benchmark service.

## Changes

- Added `GET /apps` for registry visibility.
- Added filtered and bounded result queries by app ID and app type.
- Expanded acceptance reporting with ASR and zero-data-leak gates.
- Added a dashboard summary row and composite-score run history chart.
- Preserved immutable run metadata for dataset version, hardware profile, and commit.

## Compatibility

The v1 `POST /register_app`, `POST /run_eval`, and `GET /results/{run_id}` contracts remain compatible.
