"""
Streamlit UI for Patent Partners Assistant.

Provides a user-friendly interface for patent search, memo generation, and export.
"""

import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import time
from typing import Dict, Any, Optional

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Patent Partners Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
    .success-box {
        padding: 20px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
    .error-box {
        padding: 20px;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🔬 Patent Partners")
        st.caption("Team 4 Capstone Project")
        
        selected = option_menu(
            menu_title="Navigation",
            options=["Invention Memo", "Patent Draft", "Prior Art Search", "About"],
            icons=["file-text", "file-earmark-text", "search", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )
        
        # Show API status in sidebar
        st.divider()
        api_status = check_api_health()
        if api_status["healthy"]:
            st.success("✅ API: Online")
            if api_status.get("ollama_available"):
                st.success("✅ LLM: Ready")
            else:
                st.warning("⚠️ LLM: Unavailable")
        else:
            st.error("❌ API: Offline")
    
    # Main content area
    st.title("Patent Partners Assistant")
    st.caption("Offline AI-powered patent analysis and document generation")
    
    # Check API health
    if not api_status["healthy"]:
        st.error("⚠️ API server is not running. Please start it with `make start` or `./start_servers.sh`")
        st.stop()
    
    # Route to appropriate page
    if selected == "Invention Memo":
        memo_page()
    elif selected == "Patent Draft":
        draft_page()
    elif selected == "Prior Art Search":
        search_page()
    elif selected == "About":
        about_page()


def check_api_health() -> Dict[str, Any]:
    """Check if the API server is running and get status."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "healthy": True,
                "ollama_available": data.get("status") == "healthy",
                "version": data.get("version"),
            }
        return {"healthy": False}
    except requests.exceptions.RequestException:
        return {"healthy": False}


def memo_page():
    """Invention memo generation page."""
    st.header("📝 Invention Disclosure Memo")
    
    st.markdown("""
    Generate a comprehensive invention disclosure memo that analyzes your invention
    and compares it to prior art. The memo includes:
    - Invention summary and technical field
    - Prior art analysis
    - Novelty assessment
    - Patentability recommendation
    - Suggested claims strategy
    """)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Input")
        
        # Invention description
        invention_description = st.text_area(
            "Invention Description:",
            placeholder="Describe your invention in detail:\n\n- What problem does it solve?\n- How does it work?\n- What makes it novel?\n- Key features and benefits?\n\nExample: A smart delivery drone system that uses advanced computer vision and machine learning to navigate obstacles in urban environments...",
            height=300,
            key="memo_invention"
        )
        
        # Generation options
        with st.expander("⚙️ Generation Options"):
            temperature = st.slider(
                "Creativity (Temperature):",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values = more creative but less focused"
            )
            
            max_tokens = st.slider(
                "Maximum Length:",
                min_value=1000,
                max_value=4000,
                value=2000,
                step=500,
                help="Maximum length of generated memo"
            )
        
        # Generate button
        generate_clicked = st.button(
            "🚀 Generate Invention Memo",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📤 Generated Memo")
        
        if generate_clicked:
            if not invention_description or len(invention_description) < 50:
                st.warning("⚠️ Please enter a detailed invention description (at least 50 characters).")
            else:
                # Generate memo
                with st.spinner("🤖 Generating invention memo... This may take 60-90 seconds..."):
                    result = generate_memo(
                        invention_description=invention_description,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                
                if result["success"]:
                    # Display success
                    st.success(f"✅ Memo generated in {result['time_seconds']:.1f} seconds!")
                    
                    # Show memo
                    st.markdown("---")
                    st.markdown(result["memo"])
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Text",
                        data=result["memo"],
                        file_name="invention_memo.txt",
                        mime="text/plain",
                    )
                    
                    # Show metadata
                    with st.expander("ℹ️ Generation Details"):
                        st.write(f"**Model Used:** {result['model']}")
                        st.write(f"**Generation Time:** {result['time_ms']:.0f}ms")
                        st.write(f"**Citations Found:** {len(result['citations'])}")
                        st.write(f"**Memo Length:** {len(result['memo'])} characters")
                
                else:
                    st.error(f"❌ Error generating memo: {result['error']}")
                    st.info("💡 **Troubleshooting:**\n- Check if Ollama is running\n- Verify Mistral model is installed: `ollama list`\n- Check API logs for details")


def draft_page():
    """Patent draft generation page."""
    st.header("⚖️ Patent Application Draft")
    
    st.markdown("""
    Generate a USPTO-compliant patent application draft including:
    - Title and Abstract
    - Background and Prior Art
    - Summary of Invention
    - Detailed Description
    - Claims (independent and dependent)
    """)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Input")
        
        # Invention description
        invention_description = st.text_area(
            "Invention Description:",
            placeholder="Provide a comprehensive description of your invention:\n\n- Technical field and problem\n- Detailed solution\n- Key components/steps\n- Advantages over prior art\n- Specific examples\n\nExample: An autonomous delivery drone system featuring multi-sensor obstacle avoidance, AI-powered navigation, secure package delivery...",
            height=300,
            key="draft_invention"
        )
        
        # Generation options
        with st.expander("⚙️ Generation Options"):
            temperature = st.slider(
                "Creativity (Temperature):",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key="draft_temp"
            )
            
            max_tokens = st.slider(
                "Maximum Length:",
                min_value=2000,
                max_value=5000,
                value=3500,
                step=500,
                key="draft_tokens"
            )
        
        # Generate button
        generate_clicked = st.button(
            "🚀 Generate Patent Draft",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📤 Generated Draft")
        
        if generate_clicked:
            if not invention_description or len(invention_description) < 50:
                st.warning("⚠️ Please enter a detailed invention description (at least 50 characters).")
            else:
                # Generate draft
                with st.spinner("🤖 Generating patent draft... This may take 90-120 seconds..."):
                    result = generate_draft(
                        invention_description=invention_description,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                
                if result["success"]:
                    # Display success
                    st.success(f"✅ Draft generated in {result['time_seconds']:.1f} seconds!")
                    
                    # Show draft sections
                    st.markdown("---")
                    
                    # Create tabs for sections
                    if result["sections"]:
                        tabs = st.tabs(["Full Draft"] + result["sections"][:5])  # Limit to 6 tabs
                        
                        with tabs[0]:
                            st.markdown(result["draft"])
                        
                        # Show individual sections
                        draft_sections = parse_sections_from_draft(result["draft"])
                        for i, section_name in enumerate(result["sections"][:5], 1):
                            with tabs[i]:
                                section_text = draft_sections.get(section_name, "Section not found")
                                st.markdown(f"## {section_name.replace('_', ' ').title()}")
                                st.markdown(section_text)
                    else:
                        st.markdown(result["draft"])
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Text",
                        data=result["draft"],
                        file_name="patent_draft.txt",
                        mime="text/plain",
                    )
                    
                    # Show metadata
                    with st.expander("ℹ️ Generation Details"):
                        st.write(f"**Model Used:** {result['model']}")
                        st.write(f"**Generation Time:** {result['time_ms']:.0f}ms")
                        st.write(f"**Sections Generated:** {len(result['sections'])}")
                        st.write(f"**Draft Length:** {len(result['draft'])} characters")
                        st.write(f"**Citations Found:** {len(result['citations'])}")
                
                else:
                    st.error(f"❌ Error generating draft: {result['error']}")
                    st.info("💡 **Troubleshooting:**\n- Check if Ollama is running\n- Verify Mistral model is installed: `ollama list`\n- Check API logs for details")


def search_page():
    """Prior art search page."""
    st.header("🔍 Prior Art Search")
    
    st.markdown("""
    Search for existing patents related to your invention.
    
    **🚧 Coming Soon:** This feature will be implemented in the next sprint with:
    - BM25 keyword search
    - FAISS semantic search
    - Hybrid ranking with reranking
    - Citation extraction
    """)
    
    # Search input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search query:",
            placeholder="Enter keywords, concepts, or technical terms...",
        )
    
    with col2:
        top_k = st.number_input("Results:", min_value=1, max_value=50, value=10)
    
    if st.button("Search Patents", type="primary"):
        if search_query:
            st.info("🚧 Search functionality will be implemented in Sprint 2. For now, you can generate memos and drafts without prior art context.")
        else:
            st.warning("Please enter a search query.")


def about_page():
    """About page with project information."""
    st.header("ℹ️ About Patent Partners Assistant")
    
    st.markdown("""
    ## 🎯 Project Overview
    
    An offline, AI-powered patent assistant that helps lawyers and inventors with:
    - **Prior-Art Search**: Natural language search with citations
    - **Invention Memo**: Automated summary of inventions vs. prior art
    - **Patent Drafting**: Skeleton patent documents (abstract, summary, claims)
    - **Offline Operation**: Complete privacy with local processing
    
    ## 🏗️ Technical Architecture
    
    - **Backend**: FastAPI with SQLite database
    - **Frontend**: Streamlit for lawyer-friendly interface
    - **LLM**: Mistral-7B via Ollama (local inference)
    - **Search**: Hybrid BM25 + FAISS (planned)
    - **Privacy**: All data stays on local machine
    
    ## 👥 Team
    
    - **Team Lead**: Arya Koirala
    - **Data Engineer**: Devika Amalkar
    - **Backend Engineer**: Nandan P
    - **Frontend Engineer**: Rachel Mathew
    - **DevOps/QA**: Nicholas Joseph
    
    ## 📊 Current Status
    
    ### ✅ Completed (Sprint 1)
    - Project setup and architecture
    - FastAPI backend with all endpoints
    - Streamlit UI
    - LLM integration (Mistral-7B)
    - Memo generation (working)
    - Draft generation (working)
    - DOCX export
    
    ### 🔄 In Progress (Sprint 2)
    - USPTO data ingestion
    - Search implementation
    - UI enhancements
    
    ### 📅 Planned (Sprint 3)
    - Advanced search with reranking
    - Citation validation
    - Performance optimization
    - Deployment packaging
    
    ## 🔗 Links
    
    - **Repository**: [GitHub](https://github.com/nandanpabolu/Capstone-Project-Team-4)
    - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Issues**: [GitHub Issues](https://github.com/nandanpabolu/Capstone-Project-Team-4/issues)
    
    ## ⚠️ Disclaimer
    
    This tool is for educational and research purposes only. It is not a replacement 
    for professional legal counsel.
    """)


def generate_memo(invention_description: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call API to generate invention memo."""
    try:
        payload = {
            "invention_description": invention_description,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/generate/memo",
            json=payload,
            timeout=180  # 3 minutes
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "memo": data["draft"],
                "citations": data.get("citations", []),
                "time_ms": data.get("generation_time_ms", 0),
                "time_seconds": elapsed,
                "model": data.get("model_used", "unknown"),
            }
        else:
            return {
                "success": False,
                "error": f"API returned status {response.status_code}: {response.text}"
            }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out after 3 minutes. The model may be processing a very long response."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_draft(invention_description: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call API to generate patent draft."""
    try:
        payload = {
            "invention_description": invention_description,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/generate/draft",
            json=payload,
            timeout=180  # 3 minutes
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "draft": data["draft"],
                "sections": data.get("sections", []),
                "citations": data.get("citations", []),
                "time_ms": data.get("generation_time_ms", 0),
                "time_seconds": elapsed,
                "model": data.get("model_used", "unknown"),
            }
        else:
            return {
                "success": False,
                "error": f"API returned status {response.status_code}: {response.text}"
            }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out after 3 minutes. The model may be processing a very long response."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def parse_sections_from_draft(draft_text: str) -> Dict[str, str]:
    """Parse draft text into sections."""
    sections = {}
    current_section = "preamble"
    current_content = []
    
    for line in draft_text.split("\n"):
        if line.strip().startswith("##"):
            # Save previous section
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            
            # Start new section
            section_name = line.strip("#").strip().lower().replace(" ", "_")
            current_section = section_name
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections


if __name__ == "__main__":
    main()
