"""
Streamlit UI for Patent Partners Assistant.

Provides a user-friendly interface for patent search, memo generation, and export.
"""

import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Simple settings for demo - no complex imports needed
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Patent Partners Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL is already defined above


def main():
    """Main Streamlit application."""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🔬 Patent Partners")
        st.caption("Team 4 Capstone Project")
        
        selected = option_menu(
            menu_title="Navigation",
            options=["Idea Input", "Prior Art Search", "Invention Memo", "Export Draft"],
            icons=["lightbulb", "search", "file-text", "download"],
            menu_icon="cast",
            default_index=0,
        )
    
    # Main content area
    st.title("Patent Partners Assistant")
    st.caption("Offline AI-powered patent analysis and document generation")
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ API server is not running. Please start it with `make api`")
        st.stop()
    
    # Route to appropriate page
    if selected == "Idea Input":
        idea_input_page()
    elif selected == "Prior Art Search":
        search_page()
    elif selected == "Invention Memo":
        memo_page()
    elif selected == "Export Draft":
        export_page()


def check_api_health() -> bool:
    """Check if the API server is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def idea_input_page():
    """Idea input and auto-draft page."""
    st.header("💡 Idea Input & Auto-Draft")
    
    st.markdown("""
    Enter your invention idea below and the system will help you:
    - Search for relevant prior art
    - Generate an invention memo
    - Create a patent draft
    """)
    
    # Idea input
    invention_idea = st.text_area(
        "Describe your invention:",
        placeholder="Enter a detailed description of your invention, including its purpose, how it works, and what makes it novel...",
        height=200,
    )
    
    if st.button("Generate Patent Draft", type="primary"):
        if invention_idea:
            with st.spinner("Generating patent draft..."):
                # TODO: Implement actual generation
                st.success("✅ Patent draft generated!")
                st.info("🚧 Generation functionality will be implemented in Sprint 2")
        else:
            st.warning("Please enter your invention idea first.")


def search_page():
    """Prior art search page."""
    st.header("🔍 Prior Art Search")
    
    st.markdown("""
    Search for existing patents related to your invention to understand the prior art landscape.
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
            with st.spinner("Searching patents..."):
                # TODO: Implement actual search
                st.success("✅ Search completed!")
                st.info("🚧 Search functionality will be implemented in Sprint 1")
                
                # Placeholder results
                st.subheader("Search Results")
                st.info("No results yet - search functionality coming soon!")
        else:
            st.warning("Please enter a search query.")


def memo_page():
    """Invention memo generation page."""
    st.header("📝 Invention Memo")
    
    st.markdown("""
    Generate a comprehensive memo that compares your invention to existing prior art,
    highlighting novelty and potential patentability.
    """)
    
    # Memo input
    invention_description = st.text_area(
        "Invention Description:",
        placeholder="Provide a detailed description of your invention...",
        height=150,
    )
    
    if st.button("Generate Invention Memo", type="primary"):
        if invention_description:
            with st.spinner("Generating invention memo..."):
                # TODO: Implement actual memo generation
                st.success("✅ Invention memo generated!")
                st.info("🚧 Memo generation functionality will be implemented in Sprint 2")
        else:
            st.warning("Please enter your invention description first.")


def export_page():
    """Document export page."""
    st.header("📄 Export Draft")
    
    st.markdown("""
    Export your generated patent documents in various formats for further editing and submission.
    """)
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Options")
        export_format = st.selectbox(
            "Format:",
            ["DOCX", "PDF", "Markdown"],
            index=0,
        )
        
        include_sections = st.multiselect(
            "Include Sections:",
            ["Abstract", "Summary", "Claims", "Description"],
            default=["Abstract", "Summary", "Claims"],
        )
    
    with col2:
        st.subheader("Preview")
        st.info("🚧 Export functionality will be implemented in Sprint 3")
    
    if st.button("Export Document", type="primary"):
        if include_sections:
            with st.spinner("Exporting document..."):
                # TODO: Implement actual export
                st.success("✅ Document exported!")
                st.info("🚧 Export functionality will be implemented in Sprint 3")
        else:
            st.warning("Please select at least one section to export.")


if __name__ == "__main__":
    main()
