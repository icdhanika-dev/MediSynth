import base64
import uuid
import html
from textwrap import dedent

import fitz
import streamlit as st

from neo4j import GraphDatabase

from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_DATABASE,
)

from workflow.diagnostic_workflow import build_workflow


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MediSynth",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM THEME
# ============================================================

st.markdown(
    dedent(
        """
        <style>

        /* ==============================
           GLOBAL
        ============================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 85% 10%,
                    rgba(255, 105, 70, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 15% 35%,
                    rgba(126, 87, 194, 0.08),
                    transparent 30%
                ),
                #0d0d0f;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        h1, h2, h3 {
            letter-spacing: -0.6px;
        }

        /* ==============================
           SIDEBAR
        ============================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #111113 0%,
                    #151313 100%
                );
            border-right: 1px solid #292522;
        }

        [data-testid="stSidebar"] * {
            color: #f4eee9;
        }

        /* ==============================
           HERO
        ============================== */

        .hero-card {
            padding: 42px;
            border-radius: 28px;
            border: 1px solid #3a302c;
            background:
                linear-gradient(
                    135deg,
                    rgba(39, 31, 28, 0.96),
                    rgba(22, 20, 25, 0.98)
                );
            box-shadow:
                0 20px 70px rgba(0,0,0,0.30);
            margin-bottom: 28px;
            animation: fadeUp 0.7s ease;
        }

        .hero-kicker {
            color: #ff8b67;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .hero-title {
            color: #fff8f2;
            font-size: 52px;
            font-weight: 850;
            line-height: 1.05;
            margin-bottom: 14px;
        }

        .hero-title span {
            color: #ff7657;
        }

        .hero-description {
            color: #bdb3ad;
            font-size: 17px;
            line-height: 1.65;
            max-width: 850px;
        }

        /* ==============================
           SLIDE CARDS
        ============================== */

        .slide-label {
            color: #ff8b67;
            font-size: 12px;
            font-weight: 850;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .slide-title {
            color: #fff8f2;
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .slide-subtitle {
            color: #aaa09a;
            font-size: 15px;
            margin-bottom: 22px;
        }

        .slide-divider {
            height: 1px;
            background: #2c2826;
            margin: 32px 0;
        }

        /* ==============================
           AGENT CARDS
        ============================== */

        .agent-card {
            padding: 22px;
            border-radius: 18px;
            background: #151516;
            border: 1px solid #302c2a;
            min-height: 145px;
            transition: all 0.25s ease;
            animation: fadeUp 0.6s ease;
        }

        .agent-card:hover {
            transform: translateY(-5px);
            border-color: #ff7657;
            box-shadow: 0 12px 35px rgba(255,118,87,0.10);
        }

        .agent-icon {
            font-size: 26px;
            margin-bottom: 12px;
        }

        .agent-name {
            font-size: 17px;
            font-weight: 800;
            color: #fff8f2;
        }

        .agent-description {
            color: #9e9691;
            font-size: 13px;
            line-height: 1.5;
            margin-top: 7px;
        }

        /* ==============================
           METRIC CARDS
        ============================== */

        .metric-card {
            background: #151516;
            border: 1px solid #302c2a;
            border-radius: 18px;
            padding: 22px;
            text-align: center;
            animation: fadeUp 0.6s ease;
        }

        .metric-value {
            color: #ff8969;
            font-size: 35px;
            font-weight: 850;
        }

        .metric-label {
            color: #918983;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.3px;
            margin-top: 5px;
        }

        /* ==============================
           RESULT CARDS
        ============================== */

        .result-card {
            background: #151516;
            border: 1px solid #332e2b;
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 15px;
            animation: fadeUp 0.5s ease;
        }

        .result-heading {
            color: #fff8f2;
            font-size: 19px;
            font-weight: 800;
        }

        .result-text {
            color: #b8afa9;
            line-height: 1.65;
            margin-top: 8px;
        }

        .confidence {
            color: #ff9a78;
            font-weight: 800;
        }

        /* ==============================
           STATUS
        ============================== */

        .status-pill {
            display: inline-block;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(255,118,87,0.10);
            border: 1px solid rgba(255,118,87,0.25);
            color: #ff9475;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.7px;
        }

        /* ==============================
           PIPELINE
        ============================== */

        .pipeline-box {
            background: #141416;
            border: 1px solid #302c2a;
            border-radius: 18px;
            padding: 20px;
            margin: 10px 0 25px 0;
        }

        .pipeline-text {
            color: #bdb4ae;
            text-align: center;
            font-size: 14px;
            line-height: 2;
        }

        .pipeline-text strong {
            color: #ff8b67;
        }

        /* ==============================
           BUTTONS
        ============================== */

        .stButton > button {
            border-radius: 12px;
            min-height: 48px;
            font-weight: 800;
            border: 1px solid #4a3731;
            background: #ff684f;
            color: white;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: #ff7d62;
            border-color: #ff8d72;
            transform: translateY(-2px);
        }

        /* ==============================
           FILE UPLOAD
        ============================== */

        [data-testid="stFileUploader"] {
            background: #151516;
            border-radius: 16px;
        }

        /* ==============================
           INPUTS
        ============================== */

        textarea,
        input {
            border-radius: 12px !important;
        }

        /* ==============================
           ANIMATION
        ============================== */

        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(12px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* ==============================
           FOOTER
        ============================== */

        .footer {
            text-align: center;
            color: #716964;
            font-size: 12px;
            padding: 35px 0 10px 0;
            letter-spacing: 1px;
        }

        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe_text(value):
    if value is None:
        return ""

    return str(value)


def get_value(obj, key, default=None):
    """
    Works with both Pydantic objects and dictionaries.
    """

    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def short_text(value, limit=180):
    value = safe_text(value)

    if len(value) <= limit:
        return value

    return value[:limit] + "..."


def extract_pdf_text(uploaded_file):
    """
    Extract text from uploaded pathology PDF.
    """

    pdf_bytes = uploaded_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page in document:
        pages.append(
            page.get_text()
        )

    document.close()

    return "\n".join(pages)


def image_to_data_url(uploaded_file):
    """
    Convert uploaded image into a base64 data URL.
    """

    image_bytes = uploaded_file.getvalue()

    encoded = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    mime = uploaded_file.type

    return f"data:{mime};base64,{encoded}"


def display_agent_analysis(analysis):

    agent_name = get_value(
        analysis,
        "agent",
        "Specialist Agent"
    )

    findings = get_value(
        analysis,
        "findings",
        []
    )

    possible_conditions = get_value(
        analysis,
        "possible_conditions",
        []
    )

    uncertainties = get_value(
        analysis,
        "uncertainties",
        []
    )

    contradictions = get_value(
        analysis,
        "contradictions",
        []
    )

    st.markdown(
        f"### {agent_name.title()}"
    )

    if findings:

        st.markdown("#### Findings")

        for finding in findings:

            finding_text = get_value(
                finding,
                "finding",
                ""
            )

            evidence = get_value(
                finding,
                "evidence",
                ""
            )

            confidence = get_value(
                finding,
                "confidence",
                0
            )

            try:
                confidence_percent = float(
                    confidence
                ) * 100
            except Exception:
                confidence_percent = 0

            with st.container(border=True):

                st.markdown(
                    f"**{safe_text(finding_text)}**"
                )

                if evidence:

                    st.caption(
                        f"Evidence: {safe_text(evidence)}"
                    )

                st.progress(
                    min(
                        max(
                            confidence_percent / 100,
                            0
                        ),
                        1
                    )
                )

                st.caption(
                    f"Confidence: {confidence_percent:.0f}%"
                )

    if possible_conditions:

        st.markdown(
            "#### Possible Conditions"
        )

        for condition in possible_conditions:

            st.markdown(
                f"- {safe_text(condition)}"
            )

    if uncertainties:

        st.markdown(
            "#### Uncertainties"
        )

        for item in uncertainties:

            st.markdown(
                f"- {safe_text(item)}"
            )

    if contradictions:

        st.markdown(
            "#### Contradictions"
        )

        for item in contradictions:

            st.warning(
                safe_text(item)
            )


def render_metric(value, label):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-label">{html.escape(label)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        # 🩺 MediSynth
        """
    )

    st.caption(
        "MULTI-AGENT CLINICAL DECISION SUPPORT"
    )

    st.divider()

    agents = [
        (
            "☢️",
            "Radiology Agent",
            "Analyzes uploaded radiology images."
        ),
        (
            "🔬",
            "Pathology Agent",
            "Analyzes pathology reports."
        ),
        (
            "📄",
            "Patient History Agent",
            "Analyzes symptoms and clinical history."
        ),
    ]

    for icon, name, description in agents:

        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-icon">{icon}</div>
                <div class="agent-name">{html.escape(name)}</div>
                <div class="agent-description">
                    {html.escape(description)}
                </div>
            </div>
            <div style="height:10px;"></div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### PIPELINE")

    st.caption(
        "Agents → Evidence → Conflict → Debate → "
        "Consensus → Human Review"
    )

    st.divider()

    st.caption(
        "Prototype for hackathon demonstration."
    )

    st.caption(
        "Decision support only. Human clinician review required."
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero-card">
<div class="hero-kicker">AA-25 · AUTONOMOUS MULTI-AGENT DIAGNOSIS ASSISTANT</div>
<div class="hero-title">Medi<span>Synth</span></div>
<div class="hero-description">Evidence-driven multi-agent clinical decision support. Independent specialist agents analyze different evidence sources, identify disagreements, debate conflicting findings, and produce a traceable consolidated differential for human review.</div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PIPELINE VISUAL
# ============================================================

st.markdown(
    '<div class="slide-label">SYSTEM FLOW</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="slide-title">From Evidence to Clinical Review</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="slide-subtitle">Each stage contributes independently before consensus.</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="pipeline-box">
        <div class="pipeline-text">
            <strong>RADIOLOGY</strong>
            &nbsp; → &nbsp;
            <strong>PATHOLOGY</strong>
            &nbsp; → &nbsp;
            <strong>HISTORY</strong>
            &nbsp; → &nbsp;
            <strong>EVIDENCE</strong>
            &nbsp; → &nbsp;
            <strong>CONFLICT</strong>
            &nbsp; → &nbsp;
            <strong>DEBATE</strong>
            &nbsp; → &nbsp;
            <strong>CONSENSUS</strong>
            &nbsp; → &nbsp;
            <strong>HUMAN REVIEW</strong>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CASE INTAKE
# ============================================================

st.markdown(
    '<div class="slide-label">01 · CASE INTAKE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="slide-title">New Clinical Case</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="slide-subtitle">Provide the available evidence. Each specialist receives its own evidence source.</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### ☢️ Radiology")

    radiology_file = st.file_uploader(
        "Upload radiology image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ],
        help="Upload a PNG or JPG/JPEG radiology image.",
        key="radiology_upload",
    )

with col2:

    st.markdown("### 🔬 Pathology")

    pathology_file = st.file_uploader(
        "Upload pathology report",
        type=["pdf"],
        help="Upload the pathology report as a PDF.",
        key="pathology_upload",
    )


st.markdown("### 📄 Patient History")

patient_history = st.text_area(
    "Enter patient symptoms and clinical history",
    placeholder=(
        "Example: Patient has fever for 5 days "
        "with mild chest pain..."
    ),
    height=130,
    key="patient_history",
)


# ============================================================
# INPUT PREVIEW
# ============================================================

if radiology_file or pathology_file or patient_history:

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">EVIDENCE PREVIEW</div>',
        unsafe_allow_html=True
    )

    preview1, preview2, preview3 = st.columns(3)

    with preview1:

        if radiology_file:

            st.success(
                f"Radiology loaded\n\n{radiology_file.name}"
            )

            st.image(
                radiology_file,
                caption="Uploaded radiology image",
                use_container_width=True,
            )

        else:

            st.info(
                "No radiology image uploaded."
            )

    with preview2:

        if pathology_file:

            st.success(
                f"Pathology loaded\n\n{pathology_file.name}"
            )

        else:

            st.info(
                "No pathology report uploaded."
            )

    with preview3:

        if patient_history.strip():

            st.success(
                "Patient history provided."
            )

            st.caption(
                short_text(
                    patient_history,
                    180
                )
            )

        else:

            st.info(
                "No patient history entered."
            )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze_clicked = st.button(
    "🚀 ANALYZE CASE",
    use_container_width=True,
)


# ============================================================
# RUN WORKFLOW
# ============================================================

if analyze_clicked:

    if not radiology_file:
        st.error(
            "Please upload a radiology image."
        )
        st.stop()

    if not pathology_file:
        st.error(
            "Please upload a pathology PDF."
        )
        st.stop()

    if not patient_history.strip():
        st.error(
            "Please enter patient history."
        )
        st.stop()

    case_id = (
        "TEST_CASE_"
        + uuid.uuid4().hex[:6].upper()
    )

    with st.status(
        "Running MediSynth multi-agent pipeline...",
        expanded=True
    ) as status:

        st.write(
            "☢️ Radiology Agent analyzing imaging evidence..."
        )

        radiology_data = image_to_data_url(
            radiology_file
        )

        st.write(
            "🔬 Pathology Agent analyzing pathology evidence..."
        )

        pathology_text = extract_pdf_text(
            pathology_file
        )

        st.write(
            "📄 Patient History Agent analyzing clinical history..."
        )

        workflow = build_workflow()

        initial_state = {
            "case_id": case_id,
            "radiology_report": radiology_data,
            "pathology_report": pathology_text,
            "patient_history": patient_history,
            "analyses": [],
            "conflicts": [],
            "debates": [],
            "consensus": {},
        }

        try:

            result = workflow.invoke(
                initial_state
            )

            # Save MediSynth evidence graph to Neo4j
        driver = GraphDatabase.driver(
             NEO4J_URI,
             auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

        with driver.session(database=NEO4J_DATABASE) as session:

            session.run(
              """
            MERGE (c:Case {id: $case_id})
              """,
            case_id=case_id,
         )

         for analysis in result.get("analyses", []):

             agent_name = get_value(
                analysis,
               "agent",
               "Specialist Agent"
             )

              session.run(
                """
                MERGE (c:Case {id: $case_id})
                MERGE (a:Agent {name: $agent_name})
                MERGE (c)-[:ANALYZED_BY]->(a)
                """,
                case_id=case_id,
                agent_name=str(agent_name),
             )

             for finding in get_value(
                analysis,
                "findings",
                []
             ):

                 finding_text = get_value(
                    finding,
                    "finding",
                     ""
                 )

               evidence_text = get_value(
                  finding,
                  "evidence",
                   ""
               )

               if not finding_text:
                  continue

               session.run(
                  """
                  MERGE (c:Case {id: $case_id})
                  MERGE (a:Agent {name: $agent_name})
                  MERGE (f:Finding {
                    case_id: $case_id,
                    text: $finding_text
                })

                MERGE (c)-[:ANALYZED_BY]->(a)
                MERGE (a)-[:FOUND]->(f)

                WITH f
                FOREACH (_ IN CASE
                    WHEN $evidence_text <> "" THEN [1]
                    ELSE []
                END |
                    MERGE (e:Evidence {text: $evidence_text})
                    MERGE (f)-[:SUPPORTED_BY]->(e)
                )
                """,
                case_id=case_id,
                agent_name=str(agent_name),
                finding_text=str(finding_text),
                evidence_text=str(evidence_text),
            )

            driver.close()

            st.session_state["result"] = result
            st.session_state["case_id"] = case_id

            status.update(
                label="Analysis completed successfully.",
                state="complete",
            )

        except Exception as e:

            status.update(
                label="Pipeline encountered an error.",
                state="error",
            )

            st.exception(e)

            st.stop()


# ============================================================
# RESULTS
# ============================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    analyses = result.get(
        "analyses",
        []
    )

    conflicts = result.get(
        "conflicts",
        []
    )

    debates = result.get(
        "debates",
        []
    )

    consensus = result.get(
        "consensus",
        {}
    )

    case_id = st.session_state.get(
        "case_id",
        "TEST_CASE"
    )


    # ========================================================
    # DASHBOARD
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">ANALYSIS COMPLETE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Clinical Intelligence Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">Independent specialist reasoning followed by conflict detection, debate and consensus.</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        render_metric(
            len(analyses),
            "Specialist Agents"
        )

    total_findings = 0

    for analysis in analyses:

        total_findings += len(
            get_value(
                analysis,
                "findings",
                []
            )
        )

    with m2:
        render_metric(
            total_findings,
            "Findings"
        )

    with m3:
        render_metric(
            len(conflicts),
            "Conflicts"
        )

    with m4:
        render_metric(
            len(debates),
            "Debates"
        )


    # ========================================================
    # SPECIALIST ANALYSIS
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">02 · SPECIALIST REASONING</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Specialist Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">Three independent perspectives are preserved before reconciliation.</div>',
        unsafe_allow_html=True
    )


    if analyses:

        agent_names = []

        for analysis in analyses:

            agent_names.append(
                safe_text(
                    get_value(
                        analysis,
                        "agent",
                        "Agent"
                    )
                ).title()
            )

        tabs = st.tabs(
            agent_names
        )

        for tab, analysis in zip(
            tabs,
            analyses
        ):

            with tab:

                display_agent_analysis(
                    analysis
                )

    else:

        st.info(
            "No specialist analysis available."
        )


    # ========================================================
    # EVIDENCE GRAPH
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">03 · EVIDENCE GRAPH</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Evidence Relationship Map</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">Neo4j stores the traceable relationships connecting the case, agents, findings and evidence.</div>',
        unsafe_allow_html=True
    )


    try:

        from streamlit_agraph import (
            agraph,
            Node,
            Edge,
            Config,
        )

        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(
                NEO4J_USERNAME,
                NEO4J_PASSWORD,
            ),
        )

        graph_rows = []

        with driver.session(
            database=NEO4J_DATABASE
        ) as session:

            query = """
            MATCH (c:Case)-[r*1..3]->(n)
            WHERE c.id = $case_id
            UNWIND r AS rel

            WITH
                startNode(rel) AS source_node,
                rel,
                endNode(rel) AS target_node

            RETURN DISTINCT
                coalesce(
                    source_node.name,
                    source_node.text,
                    source_node.id
                ) AS source,

                labels(source_node) AS source_labels,

                type(rel) AS relationship,

                coalesce(
                    target_node.name,
                    target_node.text,
                    target_node.id
                ) AS target,

                labels(target_node) AS target_labels

            LIMIT 80
            """

            graph_rows = [
                record.data()
                for record in session.run(
                    query,
                    case_id=case_id
                )
            ]


        # fallback if current case graph wasn't found
        if not graph_rows:

            with driver.session(
                database=NEO4J_DATABASE
            ) as session:

                fallback_query = """
                MATCH (a)-[r]->(b)

                RETURN DISTINCT
                    coalesce(
                        a.name,
                        a.text,
                        a.id
                    ) AS source,

                    labels(a) AS source_labels,

                    type(r) AS relationship,

                    coalesce(
                        b.name,
                        b.text,
                        b.id
                    ) AS target,

                    labels(b) AS target_labels

                LIMIT 50
                """

                graph_rows = [
                    record.data()
                    for record in session.run(
                        fallback_query
                    )
                ]


        driver.close()


        if graph_rows:

            nodes = {}
            edges = []
            seen_edges = set()


            def make_short_label(text, limit=28):

                text = safe_text(text)

                if len(text) <= limit:
                    return text

                return text[:limit - 3] + "..."


            for row in graph_rows:

                source = safe_text(
                    row.get("source")
                )

                target = safe_text(
                    row.get("target")
                )

                relationship = safe_text(
                    row.get("relationship")
                )

                source_labels = row.get(
                    "source_labels",
                    []
                )

                target_labels = row.get(
                    "target_labels",
                    []
                )


                if not source or not target:
                    continue


                # -------------------------
                # SOURCE NODE
                # -------------------------

                if source not in nodes:

                    if "Case" in source_labels:

                        nodes[source] = Node(
                            id=source,
                            label=make_short_label(
                                source
                            ),
                            size=42,
                            shape="diamond",
                            color="#ff7657",
                            font={
                                "color": "#ffffff",
                                "size": 16,
                            },
                        )

                    elif "Agent" in source_labels:

                        nodes[source] = Node(
                            id=source,
                            label=make_short_label(
                                source
                            ),
                            size=34,
                            shape="box",
                            color="#7e57c2",
                            font={
                                "color": "#ffffff",
                                "size": 14,
                            },
                        )

                    else:

                        nodes[source] = Node(
                            id=source,
                            label=make_short_label(
                                source
                            ),
                            size=27,
                            shape="dot",
                            color="#f0a05a",
                            font={
                                "color": "#ffffff",
                                "size": 12,
                            },
                        )


                # -------------------------
                # TARGET NODE
                # -------------------------

                if target not in nodes:

                    if "Case" in target_labels:

                        nodes[target] = Node(
                            id=target,
                            label=make_short_label(
                                target
                            ),
                            size=42,
                            shape="diamond",
                            color="#ff7657",
                            font={
                                "color": "#ffffff",
                                "size": 16,
                            },
                        )

                    elif "Agent" in target_labels:

                        nodes[target] = Node(
                            id=target,
                            label=make_short_label(
                                target
                            ),
                            size=34,
                            shape="box",
                            color="#7e57c2",
                            font={
                                "color": "#ffffff",
                                "size": 14,
                            },
                        )

                    else:

                        nodes[target] = Node(
                            id=target,
                            label=make_short_label(
                                target
                            ),
                            size=27,
                            shape="dot",
                            color="#f0a05a",
                            font={
                                "color": "#ffffff",
                                "size": 12,
                            },
                        )


                # -------------------------
                # DEDUPLICATE EDGE
                # -------------------------

                edge_key = (
                    source,
                    relationship,
                    target
                )

                if edge_key in seen_edges:
                    continue

                seen_edges.add(
                    edge_key
                )

                edges.append(
                    Edge(
                        source=source,
                        target=target,
                        label="",
                    )
                )


            config = Config(
                width=1150,
                height=650,
                directed=True,
                physics=False,
                hierarchical=True,
                direction="LR",
                sortMethod="directed",
                nodeHighlightBehavior=True,
                highlightColor="#ff7657",
                collapsible=False,
                staticGraphWithDragAndDrop=True,
            )


            agraph(
                nodes=list(
                    nodes.values()
                ),
                edges=edges,
                config=config,
            )


            st.caption(
                "Case → Specialist Agents → Findings → Evidence / Conditions"
            )


        else:

            st.info(
                "No graph data available for this case yet."
            )


    except Exception as e:

        st.warning(
            "Evidence graph could not be displayed."
        )

        st.caption(
            "Make sure Neo4j is running."
        )


    # ========================================================
    # CONFLICT DETECTION
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">04 · CONFLICT DETECTION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Where Do Specialists Disagree?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">Conflicting evidence is isolated before the debate stage.</div>',
        unsafe_allow_html=True
    )


    if conflicts:

        for index, conflict in enumerate(
            conflicts,
            start=1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### Conflict {index}"
                )

                if isinstance(
                    conflict,
                    dict
                ):

                    for key, value in conflict.items():

                        if key in {
                            "topic",
                            "description",
                            "conflict",
                            "reason",
                        }:

                            st.write(
                                f"**{key.replace('_', ' ').title()}:** "
                                f"{safe_text(value)}"
                            )

                else:

                    st.write(
                        safe_text(conflict)
                    )

    else:

        st.success(
            "No significant conflicts were detected."
        )


    # ========================================================
    # DEBATE
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">05 · STRUCTURED DEBATE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Agent Debate</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">Agents defend their positions using evidence before revising their conclusions.</div>',
        unsafe_allow_html=True
    )


    if debates:

        for index, debate in enumerate(
            debates,
            start=1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### Debate {index}"
                )

                topic = get_value(
                    debate,
                    "topic",
                    "Clinical disagreement"
                )

                st.markdown(
                    f"**Topic:** {safe_text(topic)}"
                )


                positions = get_value(
                    debate,
                    "positions",
                    {}
                )

                if positions:

                    st.markdown(
                        "#### Initial Positions"
                    )

                    if isinstance(
                        positions,
                        dict
                    ):

                        for agent, position in positions.items():

                            st.write(
                                f"**{agent}:** {position}"
                            )


                evidence = get_value(
                    debate,
                    "evidence",
                    []
                )

                if evidence:

                    st.markdown(
                        "#### Evidence"
                    )

                    for item in evidence:

                        st.write(
                            f"- {safe_text(item)}"
                        )


                responses = get_value(
                    debate,
                    "responses",
                    []
                )

                if responses:

                    st.markdown(
                        "#### Responses"
                    )

                    for item in responses:

                        st.write(
                            f"- {safe_text(item)}"
                        )


                revised_positions = get_value(
                    debate,
                    "revised_positions",
                    {}
                )

                if revised_positions:

                    st.markdown(
                        "#### Revised Positions"
                    )

                    if isinstance(
                        revised_positions,
                        dict
                    ):

                        for agent, position in revised_positions.items():

                            st.write(
                                f"**{agent}:** {position}"
                            )

    else:

        st.info(
            "No debate was required because no meaningful conflict was detected."
        )


    # ========================================================
    # CONSENSUS
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">06 · CONSENSUS ENGINE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Consolidated Differential</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">Evidence from all specialists is consolidated for clinician review.</div>',
        unsafe_allow_html=True
    )


    if consensus:

        differential = consensus.get(
            "differential",
            consensus.get(
                "possible_conditions",
                []
            )
        )

        if differential:

            st.markdown(
                "### Possible Conditions"
            )

            if isinstance(
                differential,
                list
            ):

                for index, item in enumerate(
                    differential,
                    start=1
                ):

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{index}. {safe_text(item)}**"
                        )

            else:

                st.write(
                    safe_text(differential)
                )


        supporting_evidence = consensus.get(
            "supporting_evidence",
            []
        )

        if supporting_evidence:

            st.markdown(
                "### Supporting Evidence"
            )

            for item in supporting_evidence:

                st.write(
                    f"- {safe_text(item)}"
                )


        unresolved = consensus.get(
            "unresolved_conflicts",
            []
        )

        if unresolved:

            st.markdown(
                "### Unresolved Conflicts"
            )

            for item in unresolved:

                st.warning(
                    safe_text(item)
                )


        evidence_gaps = consensus.get(
            "evidence_gaps",
            []
        )

        if evidence_gaps:

            st.markdown(
                "### Evidence Gaps"
            )

            for item in evidence_gaps:

                st.info(
                    safe_text(item)
                )


        overall_confidence = consensus.get(
            "confidence",
            None
        )

        if overall_confidence is not None:

            try:

                confidence_value = float(
                    overall_confidence
                )

                if confidence_value > 1:
                    confidence_value /= 100

                confidence_value = min(
                    max(
                        confidence_value,
                        0
                    ),
                    1
                )

                st.markdown(
                    "### Overall Confidence"
                )

                st.progress(
                    confidence_value
                )

                st.caption(
                    f"{confidence_value * 100:.0f}%"
                )

            except Exception:
                pass

    else:

        st.info(
            "Consensus result unavailable."
        )


    # ========================================================
    # HUMAN REVIEW
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">07 · HUMAN-IN-THE-LOOP</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Clinician Review Checkpoint</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-subtitle">The AI output is decision support. A human clinician remains responsible for the final decision.</div>',
        unsafe_allow_html=True
    )


    with st.container(
        border=True
    ):

        st.markdown(
            "### 👨‍⚕️ Human Sign-Off"
        )

        review_notes = st.text_area(
            "Clinician review notes",
            placeholder=(
                "Enter comments, modifications, "
                "or additional evidence requested..."
            ),
            height=140,
            key="review_notes",
        )

        review_col1, review_col2 = st.columns(2)

        with review_col1:

            if st.button(
                "✅ APPROVE FOR REVIEW",
                use_container_width=True
            ):

                st.success(
                    "Human review checkpoint recorded."
                )

        with review_col2:

            if st.button(
                "🔄 REQUEST RE-ANALYSIS",
                use_container_width=True
            ):

                st.info(
                    "Re-analysis requested. "
                    "Additional evidence should be provided."
                )


    # ========================================================
    # AUDIT TRAIL
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="slide-label">AUDIT TRAIL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slide-title">Traceable Decision Chain</div>',
        unsafe_allow_html=True
    )

    audit_steps = [
        "Evidence submitted",
        "Specialist agents analyzed independently",
        "Evidence relationships extracted",
        "Conflicts detected",
        "Structured debate performed",
        "Consensus generated",
        "Human review checkpoint",
    ]

    for index, step in enumerate(
        audit_steps,
        start=1
    ):

        st.markdown(
            f"**{index:02d}**  {step}"
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.markdown("---")

    st.warning(
        "MediSynth is a prototype for clinical decision support. "
        "It does not provide an autonomous final diagnosis. "
        "Synthetic/demo data should be used for demonstration."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        MEDISYNTH · AA-25 · MULTI-AGENT CLINICAL DECISION SUPPORT
    </div>
    """,
    unsafe_allow_html=True
)
