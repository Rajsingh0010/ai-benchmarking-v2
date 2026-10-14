import streamlit as st
from orchestrator.config import settings
from orchestrator.storage import RunStore

st.set_page_config(page_title="AI Benchmarking Suite", page_icon="📊", layout="wide")
st.title("AI Benchmarking Suite")
st.caption("Offline-first v2 results dashboard")
runs = RunStore(settings.db_path).list()
if not runs:
    st.info("No benchmark runs yet. Start the API and run scripts/run_benchmark.py, or POST /run_eval.")
else:
    passed = sum(run["gates"]["passed"] for run in runs)
    a, b, c = st.columns(3)
    a.metric("Runs", len(runs))
    b.metric("Gate pass rate", f"{passed / len(runs):.0%}")
    c.metric("Latest composite", f"{runs[0]['composite_score']:.1%}")
    st.subheader("Run history")
    st.line_chart({"composite score": [run["composite_score"] for run in reversed(runs)]})
    for run in runs:
        with st.container(border=True):
            left, middle, right = st.columns(3)
            left.write(f"**{run['app_id']}** · `{run['app_type']}`")
            middle.metric("Composite score", f"{run['composite_score']:.1%}")
            right.metric("Gate", "PASS" if run["gates"]["passed"] else "FAIL")
            st.json({"metrics": run["metrics"], "security": run["security"]}, expanded=False)
