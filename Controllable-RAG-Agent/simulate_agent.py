

import tempfile
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components
from functions_for_pipeline import create_agent, PlanExecute

def create_network_graph(current_state: str):
    """
    Create a network graph visualization of the agent's current state.
    """
    net = Network(directed=True, notebook=True, height="300px", width="100%")
    net.toggle_physics(False)
    
    nodes = [
        {"id": "anonymize_question", "label": "匿名化問題", "x": 0, "y": 0},
        {"id": "planner", "label": "規劃步驟", "x": 175*1.75, "y": -100},
        {"id": "de_anonymize_plan", "label": "計畫去匿名化", "x": 350*1.75, "y": -100},
        {"id": "break_down_plan", "label": "分解計畫", "x": 525*1.75, "y": -100},
        {"id": "task_handler", "label": "任務決策", "x": 700*1.75, "y": 0},
        {"id": "retrieve_chunks", "label": "檢索 Chunks", "x": 875*1.75, "y": 200},
        {"id": "retrieve_summaries", "label": "檢索 Summaries", "x": 875*1.75, "y": 100},
        {"id": "retrieve_book_quotes", "label": "檢索 Quotes", "x": 875*1.75, "y": 0},
        {"id": "answer", "label": "根據上下文回答", "x": 875*1.75, "y": -100},
        {"id": "replan", "label": "重新規劃", "x": 1050*1.75, "y": 0},
        {"id": "can_be_answered_already", "label": "檢查是否可回答", "x": 1225*1.75, "y": 0},
        {"id": "get_final_answer", "label": "生成最終答案", "x": 1400*1.75, "y": 0}
    ]

    edges = [
        ("anonymize_question", "planner"),
        ("planner", "de_anonymize_plan"),
        ("de_anonymize_plan", "break_down_plan"),
        ("break_down_plan", "task_handler"),
        ("task_handler", "retrieve_chunks"),
        ("task_handler", "retrieve_summaries"),
        ("task_handler", "retrieve_book_quotes"),
        ("task_handler", "answer"),
        ("retrieve_chunks", "replan"),
        ("retrieve_summaries", "replan"),
        ("retrieve_book_quotes", "replan"),
        ("answer", "replan"),
        ("replan", "can_be_answered_already"),
        ("replan", "break_down_plan"),
        ("can_be_answered_already", "get_final_answer")
    ]
    
    for node in nodes:
        color = "#00FF00" if node["id"] == current_state else "#FFB6C1"
        net.add_node(node["id"], label=node["label"], x=node["x"], y=node["y"], color=color, physics=False, font={'size': 22})
    
    for edge in edges:
        net.add_edge(edge[0], edge[1], color="#808080")
    
    net.options.edges.smooth.type = "straight"
    net.options.edges.width = 1.5
    
    return net

def save_and_display_graph(net):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as tmp_file:
        net.write_html(tmp_file.name, notebook=True)
        tmp_file.flush()
        with open(tmp_file.name, "r", encoding="utf-8") as f:
            return f.read()

def update_placeholders_and_graph(agent_state_value, placeholders, graph_placeholder, previous_values, previous_state):
    current_state = agent_state_value.get("curr_state")

    if current_state:
        net = create_network_graph(current_state)
        graph_html = save_and_display_graph(net)
        graph_placeholder.empty()
        with graph_placeholder.container():
            components.html(graph_html, height=400, scrolling=True)

    if current_state != previous_state and previous_state is not None:
        for key, placeholder in placeholders.items():
            if key in previous_values and previous_values[key] is not None:
                if isinstance(previous_values[key], list):
                    formatted_value = "\n".join([f"{i+1}. {item}" for i, item in enumerate(previous_values[key])])
                else:
                    formatted_value = previous_values[key]
                placeholder.markdown(f"{formatted_value}")

    for key in placeholders:
        if key in agent_state_value:
            previous_values[key] = agent_state_value[key]

    return previous_values, current_state

def execute_plan_and_print_steps(inputs, plan_and_execute_app, placeholders, graph_placeholder, recursion_limit=25):
    config = {"recursion_limit": recursion_limit}
    agent_state_value = None
    progress_bar = st.progress(0)
    step = 0
    previous_state = None
    previous_values = {key: None for key in placeholders}

    try:
        for plan_output in plan_and_execute_app.stream(inputs, config=config):
            step += 1
            for _, agent_state_value in plan_output.items():
                previous_values, previous_state = update_placeholders_and_graph(
                    agent_state_value, placeholders, graph_placeholder, previous_values, previous_state
                )

                progress_bar.progress(step / recursion_limit)
                if step >= recursion_limit:
                    break

        for key, placeholder in placeholders.items():
            if key in previous_values and previous_values[key] is not None:
                if isinstance(previous_values[key], list):
                    formatted_value = "\n".join([f"{i+1}. {item}" for i, item in enumerate(previous_values[key])])
                else:
                    formatted_value = previous_values[key]
                placeholder.markdown(f"{formatted_value}")

        response = agent_state_value.get('response', "No response found.") if agent_state_value else "No response found."
    except Exception as e:
        response = f"An error occurred: {str(e)}"
        st.error(f"Error: {e}")

    return response

def main():
    st.set_page_config(layout="wide")
    
    st.title("ESG 報告分析代理 (FAISS 版本)")
    st.write("此代理使用原專案架構，透過三個獨立的 FAISS 資料庫來回答問題。")

    try:
        plan_and_execute_app = create_agent()
    except Exception as e:
        st.error(f"初始化代理時出錯: {e}")
        st.error("請確保您已成功執行 `vectorize_esg_faiss.py` 腳本，並且 FAISS 資料庫已存在。")
        return

    question = st.text_input("請輸入您關於 ESG 報告的問題:", "報告中揭露的溫室氣體排放量是多少？主要的減排措施有哪些？")

    if st.button("執行代理"):
        if not question:
            st.warning("請輸入一個問題。")
            return

        inputs = {"question": question, "aggregated_context": "", "past_steps": [], "tool": ""}
        
        st.markdown("---下面是代理的執行過程---")
        graph_placeholder = st.empty()

        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            st.markdown("**📜 計畫**")
        with col2:
            st.markdown("**✅ 過去步驟**")
        with col3:
            st.markdown("**🧠 累積上下文**")

        placeholders = {
            "plan": col1.empty(),
            "past_steps": col2.empty(),
            "aggregated_context": col3.empty(),
        }

        with st.spinner("代理正在思考中，請稍候..."):
            response = execute_plan_and_print_steps(inputs, plan_and_execute_app, placeholders, graph_placeholder, recursion_limit=45)
        
        st.markdown("---最終答案---")
        st.success(response)

if __name__ == "__main__":
    main()
