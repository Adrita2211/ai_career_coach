import streamlit as st
import requests
import json
from typing import List, Dict, Any

st.cache_data.clear()
st.cache_resource.clear()
# --- Enhanced Custom CSS with Professional Background ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --text-primary: #2c3e50;
        --text-secondary: #5a6c7d;
        --border-color: rgba(102, 126, 234, 0.2);
        --glow-color: rgba(102, 126, 234, 0.3);
        --glass-bg: rgba(255, 255, 255, 0.95);
        --card-bg: rgba(248, 250, 252, 0.95);
        --light-bg: #f8fafc;
        --off-white: #fefefe;
    }
    
    /* Global App Styling with Light Professional Background */
    .stApp {
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.95), rgba(241, 245, 249, 0.95)), 
                    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:%23667eea;stop-opacity:0.05" /><stop offset="100%" style="stop-color:%23764ba2;stop-opacity:0.05" /></linearGradient></defs><rect width="1200" height="800" fill="url(%23grad1)"/><circle cx="200" cy="150" r="3" fill="%23667eea" opacity="0.3"><animate attributeName="opacity" values="0.3;0.6;0.3" dur="2s" repeatCount="indefinite"/></circle><circle cx="800" cy="200" r="2" fill="%234facfe" opacity="0.4"><animate attributeName="opacity" values="0.4;0.7;0.4" dur="3s" repeatCount="indefinite"/></circle><circle cx="1000" cy="400" r="4" fill="%2343e97b" opacity="0.3"><animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.5s" repeatCount="indefinite"/></circle><circle cx="300" cy="600" r="3" fill="%23f093fb" opacity="0.4"><animate attributeName="opacity" values="0.4;0.7;0.4" dur="4s" repeatCount="indefinite"/></circle><g transform="translate(100,100)"><rect x="0" y="0" width="60" height="4" fill="%23667eea" opacity="0.15" rx="2"><animateTransform attributeName="transform" type="translate" values="0,0;20,10;0,0" dur="6s" repeatCount="indefinite"/></rect><rect x="0" y="15" width="40" height="4" fill="%234facfe" opacity="0.2" rx="2"><animateTransform attributeName="transform" type="translate" values="0,0;15,8;0,0" dur="5s" repeatCount="indefinite"/></rect></g><g transform="translate(900,500)"><polygon points="0,0 20,10 40,0 30,25 10,25" fill="%2343e97b" opacity="0.1"><animateTransform attributeName="transform" type="rotate" values="0 20 12.5;360 20 12.5" dur="8s" repeatCount="indefinite"/></polygon></g><path d="M 50 300 Q 200 250 350 300 T 650 300" stroke="%23667eea" stroke-width="2" fill="none" opacity="0.15"><animate attributeName="stroke-dasharray" values="0,1000;1000,0;0,1000" dur="10s" repeatCount="indefinite"/></path></svg>'),
                    var(--off-white);
        background-size: cover, cover, 100% 100%;
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        min-height: 100vh;
    }
    
    /* Main container with glassmorphism */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid var(--border-color);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
        margin: 2rem auto;
    }
    
    /* Header Styling */
    h1 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        text-shadow: 0 0 30px var(--glow-color);
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1544g2n {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 2px solid var(--border-color) !important;
    }
    
    .css-17eq0hr {
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Form Container */
    .stForm {
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px) !important;
        padding: 2.5rem !important;
        border-radius: 25px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.1) !important;
        margin: 2rem 0 !important;
    }
    
    /* Input Fields */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px var(--glow-color) !important;
        transform: translateY(-2px) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 18px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        font-family: 'Poppins', sans-serif !important;
        resize: vertical !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px var(--glow-color) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Select Box */
    .stSelectbox select {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px var(--glow-color) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Number Input */
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Labels */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }
    
    /* Buttons - Always Visible with Strong Styling */
    .stButton button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 18px 36px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
        margin-top: 25px !important;
        position: relative !important;
        overflow: hidden !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #7c4dff 0%, #536dfe 100%) !important;
    }
    
    .stButton button:active {
        transform: translateY(-2px) !important;
    }
    
    /* Output Container - Enhanced for Better Readability */
    .output-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.95));
        backdrop-filter: blur(15px);
        border: 2px solid var(--border-color);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.15);
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        line-height: 1.8;
        white-space: pre-wrap;
        position: relative;
        overflow: hidden;
        font-size: 16px;
    }
    
    .output-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: var(--accent-gradient);
        border-radius: 20px 20px 0 0;
    }
    
    /* Enhanced Markdown styling in output */
    .output-container h1 {
        color: #2c3e50 !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        border-bottom: 3px solid #4facfe !important;
        padding-bottom: 1rem !important;
        text-align: left !important;
        background: linear-gradient(135deg, #4facfe, #00c9ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .output-container h2 {
        color: #2c3e50 !important;
        font-size: 1.9rem !important;
        font-weight: 600 !important;
        margin: 2rem 0 1rem 0 !important;
        padding-left: 1rem !important;
        border-left: 4px solid #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    .output-container h3 {
        color: #34495e !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 0.8rem 0 !important;
        padding-left: 0.8rem !important;
        border-left: 3px solid #43e97b !important;
    }
    
    .output-container h4 {
        color: #2c3e50 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin: 1.2rem 0 0.6rem 0 !important;
        color: #667eea !important;
    }
    
    .output-container h5, .output-container h6 {
        color: #34495e !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    /* Enhanced Lists */
    .output-container ul, .output-container ol {
        margin: 1.5rem 0 !important;
        padding-left: 2.5rem !important;
        line-height: 1.8 !important;
    }
    
    .output-container li {
        margin: 1rem 0 !important;
        color: #2c3e50 !important;
        font-size: 16px !important;
        line-height: 1.7 !important;
        position: relative !important;
    }
    
    .output-container ul li::marker {
        color: #667eea !important;
        font-weight: bold !important;
    }
    
    .output-container ol li::marker {
        color: #43e97b !important;
        font-weight: bold !important;
    }
    
    /* Enhanced Text Formatting */
    .output-container p {
        margin: 1.2rem 0 !important;
        color: #2c3e50 !important;
        font-size: 16px !important;
        line-height: 1.7 !important;
    }
    
    .output-container strong, .output-container b {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.1), rgba(67, 233, 123, 0.05)) !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        border-left: 3px solid #43e97b !important;
        padding-left: 0.6rem !important;
    }
    
    .output-container em, .output-container i {
        color: #5a6c7d !important;
        font-style: italic !important;
        background: rgba(102, 126, 234, 0.05) !important;
        padding: 0.1rem 0.3rem !important;
        border-radius: 3px !important;
    }
    
    /* Enhanced Code Styling */
    .output-container code {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        color: #2c3e50 !important;
        padding: 0.3rem 0.6rem !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        font-weight: 500 !important;
    }
    
    .output-container pre {
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.9), rgba(241, 245, 249, 0.9)) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 1.5rem !important;
        margin: 1.5rem 0 !important;
        overflow-x: auto !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Enhanced Blockquotes */
    .output-container blockquote {
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.05), rgba(56, 249, 215, 0.05)) !important;
        border-left: 5px solid #43e97b !important;
        margin: 1.5rem 0 !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 0 10px 10px 0 !important;
        font-style: italic !important;
        color: #34495e !important;
        box-shadow: 0 4px 12px rgba(67, 233, 123, 0.1) !important;
    }
    
    /* Enhanced Tables */
    .output-container table {
        width: 100% !important;
        border-collapse: collapse !important;
        margin: 2rem 0 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.1) !important;
    }
    
    .output-container th {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        padding: 1rem !important;
        text-align: left !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    
    .output-container td {
        padding: 0.8rem 1rem !important;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1) !important;
        color: #2c3e50 !important;
        font-size: 15px !important;
    }
    
    .output-container tr:nth-child(even) {
        background: rgba(102, 126, 234, 0.02) !important;
    }
    
    .output-container tr:hover {
        background: rgba(102, 126, 234, 0.05) !important;
        transition: background 0.3s ease !important;
    }
    
    /* Enhanced Links */
    .output-container a {
        color: #667eea !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(102, 126, 234, 0.05)) !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 5px !important;
        border-bottom: 2px solid #667eea !important;
        transition: all 0.3s ease !important;
        display: inline-block !important;
        margin: 0.1rem 0 !important;
    }
    
    .output-container a:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(102, 126, 234, 0.1)) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        border-bottom-color: #4facfe !important;
    }
    
    /* Horizontal Rules */
    .output-container hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(135deg, #667eea, #4facfe) !important;
        margin: 2.5rem 0 !important;
        border-radius: 2px !important;
    }
    
    /* Special Callout Boxes */
    .output-container .callout, .output-container .note, .output-container .tip {
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.08), rgba(56, 249, 215, 0.05)) !important;
        border: 1px solid rgba(67, 233, 123, 0.3) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #43e97b !important;
        box-shadow: 0 6px 18px rgba(67, 233, 123, 0.1) !important;
    }
    
    /* Numbered Steps Enhancement */
    .output-container ol.steps {
        counter-reset: step-counter !important;
        list-style: none !important;
        padding-left: 0 !important;
    }
    
    .output-container ol.steps li {
        counter-increment: step-counter !important;
        position: relative !important;
        padding: 1.5rem 1.5rem 1.5rem 4rem !important;
        margin: 1rem 0 !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9)) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.08) !important;
    }
    
    .output-container ol.steps li::before {
        content: counter(step-counter) !important;
        position: absolute !important;
        left: 1rem !important;
        top: 1.5rem !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        width: 2rem !important;
        height: 2rem !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }
    
    /* Responsive Typography */
    @media (max-width: 768px) {
        .output-container {
            padding: 2rem 1.5rem !important;
            font-size: 15px !important;
        }
        
        .output-container h1 {
            font-size: 2rem !important;
        }
        
        .output-container h2 {
            font-size: 1.6rem !important;
        }
        
        .output-container h3 {
            font-size: 1.3rem !important;
        }
    }
    
    /* Loading Spinner */
    .stSpinner {
        color: #667eea !important;
    }
    
    /* Error Messages */
    .stAlert {
        background: rgba(244, 67, 54, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid #f44336 !important;
        border-radius: 15px !important;
        color: #ff6b6b !important;
    }
    
    /* Success Messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid #4caf50 !important;
        border-radius: 15px !important;
        color: #43e97b !important;
    }
    
    /* Info Messages */
    .stInfo {
        background: rgba(33, 150, 243, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid #2196f3 !important;
        border-radius: 15px !important;
        color: #4facfe !important;
    }
    
    /* Sidebar Title */
    .css-1544g2n h1 {
        background: var(--success-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-size: 1.5rem !important;
        text-align: center !important;
        padding: 1rem 0 !important;
    }
    
    /* Professional floating elements */
    .floating-element {
        position: fixed;
        pointer-events: none;
        z-index: -1;
        opacity: 0.1;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(248, 250, 252, 0.8);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c4dff 0%, #536dfe 100%);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
            margin: 1rem !important;
        }
        
        h1 {
            font-size: 2.2rem !important;
        }
        
        .stForm {
            padding: 1.5rem !important;
        }
    }
    
    /* Animation keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .stForm, .output-container {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Brand colors for different sections */
    .learning-theme { border-left: 4px solid #4facfe; }
    .resume-theme { border-left: 4px solid #f093fb; }
    .interview-theme { border-left: 4px solid #43e97b; }
    .career-theme { border-left: 4px solid #ff6b6b; }
    .skill-theme { border-left: 4px solid #ffd93d; }
</style>
""", unsafe_allow_html=True)

# Add professional header with brand name
st.markdown("""
<div style="text-align: center; padding: 3rem 0; margin-bottom: 2rem;">
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%); 
                padding: 3rem 2rem; 
                border-radius: 25px; 
                border: 1px solid rgba(255, 255, 255, 0.1); 
                box-shadow: 0 25px 50px rgba(0,0,0,0.6);
                backdrop-filter: blur(15px);
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; 
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                    animation: float 6s ease-in-out infinite;"></div>
        <div style="position: relative; z-index: 1;">
            <h1 style="color: white; font-size: 3.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                       background: linear-gradient(45deg, #ffffff, #e3f2fd);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;">
                🎯 Careerzora
            </h1>
            <p style="color: rgba(255,255,255,0.95); font-size: 1.3rem; margin: 1rem 0 0 0; font-weight: 300;">
                Premium AI Career Intelligence • Professional Development • Strategic Growth
            </p>
            <div style="margin-top: 2rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">
                    🎯 Personalized Learning
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">
                    📈 Market Insights
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">
                    🚀 Career Growth
                </span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Set up the FastAPI backend URL
FASTAPI_URL = "https://cts-vibeappwe21012-4.azurewebsites.net"

def call_api(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Sends a POST request to the FastAPI backend and handles the response.
    """
    url = f"{FASTAPI_URL}/{endpoint}"
    try:
        # Show a spinner while waiting for the response
        with st.spinner(f"🔮 Careerzora  is crafting your {endpoint.replace('_', ' ')}... Please wait."):
            response = requests.post(url, json=payload, timeout=300)
        
        # Check if the response was successful
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"**🚨 Connection Error:** {e}")
        st.info("💡 Please ensure the Careerzora backend is running at 'https://cts-vibeappwe21012-4.azurewebsites.net'.")
        return None

def parse_comma_separated_input(input_str: str) -> List[str]:
    """
    Parses a comma-separated string into a list of stripped strings.
    """
    if not input_str:
        return []
    return [item.strip() for item in input_str.split(',')]

# Set page config
st.set_page_config(
    page_title="Careerzora - Premium AI Career Intelligence", 
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# Enhanced sidebar with professional styling
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.5rem 0; margin-bottom: 2rem;
            background: linear-gradient(135deg, rgba(67, 233, 123, 0.2), rgba(56, 249, 215, 0.2));
            border-radius: 15px; backdrop-filter: blur(10px);">
    <h2 style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
               -webkit-background-clip: text; 
               -webkit-text-fill-color: transparent; 
               background-clip: text;
               margin: 0; font-size: 1.4rem;">
        🎯 Navigation Hub
    </h2>
    <p style="color: #b3b3b3; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
        Choose your career development journey
    </p>
</div>
""", unsafe_allow_html=True)

functionality = st.sidebar.selectbox(
    "Select AI Service:",
    [
        "🗺️ Learning Path Generator",
        "📝 Resume Optimizer", 
        "🎤 Interview Coach",
        "📈 Career Analyzer",
        "🧠 Skill Assessor"
    ]
)

st.sidebar.markdown("""
---
### 💡 **Pro Tips**
- **Be Specific**: Detailed inputs generate better AI recommendations
- **Use Keywords**: Include industry-relevant terms for precise guidance  
- **Multiple Goals**: List various career objectives for comprehensive advice
- **Regular Updates**: Reassess your profile as you grow

### 🌟 **AI Features**
- Multi-agent intelligent system
- Real-time market analysis
- Personalized skill mapping
- Industry trend forecasting

### 🔗 **Resources**
- [📚 Career Guides](https://example.com/guides)
- [📊 Salary Insights](https://example.com/salary)
- [🎓 Learning Platforms](https://example.com/learning)
- [💬 Get Support](https://example.com/support)

### 📈 **Success Metrics**
- 95% user satisfaction
- 80% career advancement rate
- 200+ successful placements

<style>
.sidebar .markdown-text-container {
    color: #2c3e50 !important;
}
</style>
""")

# --- Enhanced UI for each functionality ---
if "Learning Path" in functionality:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;" class="learning-theme">
        <h2 style="color: #4facfe; font-size: 2.8rem; margin-bottom: 1rem;">
            🗺️ AI Learning Path Generator
        </h2>
        <p style="color: #b3b3b3; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Get a structured, personalized roadmap with curated resources, milestones, and timeline to achieve your career goals using advanced AI analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("learning_path_form"):
        st.markdown("### 📋 Your Professional Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_input("🛠️ Current Skills & Technologies", "Python, Data Analysis, SQL, Machine Learning", 
                                 help="List your current technical and soft skills")
            career_goals = st.text_input("🎯 Career Aspirations", "Data Scientist, AI Engineer, Tech Lead", 
                                       help="What roles do you want to achieve?")
            experience_level = st.selectbox(
                "📊 Professional Experience Level",
                ("beginner", "intermediate", "advanced"),
                index=1,
                help="Your current experience level in your field"
            )
            industry = st.text_input("🏢 Target Industry Sector", "Technology, AI/ML, Data Science", 
                                   help="Which industry are you targeting?")
        
        with col2:
            topic = st.text_input("📚 Specific Learning Focus", "Deep Learning, Natural Language Processing", 
                                help="Any specific technology or skill you want to master?")
            preferred_learning_style = st.selectbox(
                "🎨 Learning Preference",
                ("visual", "auditory", "hands-on", "reading", "mixed"),
                index=4,
                help="How do you learn best?"
            )
            time_commitment = st.selectbox(
                "⏰ Weekly Time Investment",
                ("light (5-10 hrs)", "moderate (10-20 hrs)", "intensive (20+ hrs)", "flexible"),
                index=3,
                help="How much time can you dedicate weekly?"
            )

        submitted = st.form_submit_button("🚀 Generate My Personalized Learning Path")

        if submitted:
            payload = {
                "skills": parse_comma_separated_input(skills),
                "career_goals": parse_comma_separated_input(career_goals),
                "experience_level": experience_level,
                "industry": industry,
                "topic": topic,
                "preferred_learning_style": preferred_learning_style,
                "time_commitment": time_commitment.split()[0]  # Extract the keyword
            }
            response = call_api("learning_path", payload)
            if response and response.get('result'):
                st.markdown("### 🎉 Your AI-Generated Learning Path")
                st.markdown(f'<div class="output-container learning-theme">{response["result"]}</div>', unsafe_allow_html=True)
            elif response:
                st.error("The AI response did not contain the expected learning path data.")

elif "Resume Optimizer" in functionality:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;" class="resume-theme">
        <h2 style="color: #f093fb; font-size: 2.8rem; margin-bottom: 1rem;">
            📝 AI Resume Optimizer
        </h2>
        <p style="color: #b3b3b3; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Get AI-powered resume analysis with ATS optimization, keyword suggestions, and strategic improvements for maximum impact.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("resume_analysis_form"):
        st.markdown("### 📄 Resume Analysis Input")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            resume_text = st.text_area("📄 Complete Resume Content", 
                                     "Paste your full resume text here for comprehensive AI analysis...", 
                                     height=350,
                                     help="Include all sections: contact info, summary, experience, education, skills")
        
        with col2:
            target_role = st.text_input("🎯 Target Position", "Senior Software Engineer", 
                                      help="The exact job title you're applying for")
            experience_years = st.number_input("📅 Total Experience (Years)", min_value=0, max_value=50, value=5,
                                             help="Total years of professional experience")
            existing_projects = st.text_input("💼 Key Projects", "E-commerce Platform, Mobile App, Data Pipeline", 
                                             help="Major projects you've worked on")
            target_companies = st.text_input("🏢 Target Companies", "Google, Microsoft, Amazon, Meta", 
                                            help="Companies you're interested in applying to")
            salary_expectations = st.text_input("💰 Salary Range", "$120,000 - $180,000", 
                                               help="Your expected salary range")

        submitted = st.form_submit_button("🔍 Analyze & Optimize My Resume")

        if submitted:
            payload = {
                "resume_text": resume_text,
                "target_role": target_role,
                "experience_years": experience_years,
                "existing_projects": parse_comma_separated_input(existing_projects),
                "target_companies": parse_comma_separated_input(target_companies),
                "salary_expectations": salary_expectations
            }
            response = call_api("resume_analysis", payload)
            if response and response.get('result'):
                st.markdown("### 📊 AI Resume Analysis & Optimization Report")
                st.markdown(f'<div class="output-container resume-theme">{response["result"]}</div>', unsafe_allow_html=True)
            elif response:
                st.error("The AI response did not contain the expected resume analysis data.")

elif "Interview Coach" in functionality:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;" class="interview-theme">
        <h2 style="color: #43e97b; font-size: 2.8rem; margin-bottom: 1rem;">
            🎤 AI Interview Coach
        </h2>
        <p style="color: #b3b3b3; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Prepare for success with AI-generated interview questions, strategic tips, company research, and mock scenarios tailored to your role.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("interview_prep_form"):
        st.markdown("### 🎯 Interview Preparation Details")
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.text_input("🎯 Target Position", "Senior Frontend Developer", 
                                      help="The specific role you're interviewing for")
            company_name = st.text_input("🏢 Company Name", "Tech Innovations Inc.", 
                                       help="Name of the company (helps with company-specific prep)")
            interview_type = st.selectbox(
                "📋 Interview Format",
                ("general", "technical", "behavioral", "case-study", "panel"),
                index=1,
                help="What type of interview are you preparing for?"
            )
        
        with col2:
            experience_level = st.selectbox(
                "📊 Your Experience Level",
                ("beginner", "intermediate", "advanced"),
                index=1,
                help="Your experience level for this role"
            )
            key_skills = st.text_input("🛠️ Key Skills to Highlight", "React, TypeScript, Node.js, AWS", 
                                     help="Skills most relevant to the position")

        submitted = st.form_submit_button("🎯 Generate Interview Preparation Guide")

        if submitted:
            payload = {
                "target_role": target_role,
                "company_name": company_name,
                "interview_type": interview_type,
                "experience_level": experience_level,
                "key_skills": parse_comma_separated_input(key_skills)
            }
            response = call_api("interview_prep", payload)
            if response and response.get('result'):
                st.markdown("### 🎯 Your Personalized Interview Preparation Guide")
                st.markdown(f'<div class="output-container interview-theme">{response["result"]}</div>', unsafe_allow_html=True)
            elif response:
                st.error("The AI response did not contain the expected interview preparation data.")
                
elif "Career Analyzer" in functionality:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;" class="career-theme">
        <h2 style="color: #ff6b6b; font-size: 2.8rem; margin-bottom: 1rem;">
            📈 AI Career Analyzer
        </h2>
        <p style="color: #b3b3b3; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Get comprehensive market analysis with salary insights, growth opportunities, industry trends, and strategic career recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("career_analysis_form"):
        st.markdown("### 📊 Career Profile Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_input("🛠️ Current Skill Portfolio", "Python, Java, Cloud Computing, DevOps", 
                                 help="Your current technical and professional skills")
            career_goals = st.text_input("🎯 Career Objectives", "Solutions Architect, Technical Lead, Engineering Manager", 
                                       help="Roles and positions you're targeting")
            experience_level = st.selectbox(
                "📊 Professional Experience",
                ("beginner", "intermediate", "advanced"),
                index=1,
                help="Your current experience level"
            )
        
        with col2:
            industry = st.text_input("🏢 Target Industry", "Cloud Services, SaaS, Enterprise Software", 
                                   help="Industries you're interested in")
            market_focus = st.text_input("🌍 Geographic/Market Focus", "San Francisco Bay Area, Remote-first companies", 
                                       help="Geographic region or specific market segment")

        submitted = st.form_submit_button("📈 Generate Career Market Analysis")

        if submitted:
            payload = {
                "user_profile": {
                    "skills": parse_comma_separated_input(skills),
                    "career_goals": parse_comma_separated_input(career_goals),
                    "experience_level": experience_level,
                    "industry": industry
                },
                "market_focus": market_focus
            }
            response = call_api("career_analysis", payload)
            if response and response.get('result'):
                st.markdown("### 💼 AI Career Analysis & Market Insights")
                st.markdown(f'<div class="output-container career-theme">{response["result"]}</div>', unsafe_allow_html=True)
            elif response:
                st.error("The AI response did not contain the expected career analysis data.")

elif "Skill Assessor" in functionality:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;" class="skill-theme">
        <h2 style="color: #ffd93d; font-size: 2.8rem; margin-bottom: 1rem;">
            🧠 AI Skill Assessor
        </h2>
        <p style="color: #b3b3b3; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Identify skill gaps and get a comprehensive development plan with prioritized learning recommendations and timeline estimates.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("skill_assessment_form"):
        st.markdown("### 🔍 Skill Gap Analysis Input")
        col1, col2 = st.columns(2)
        
        with col2:
            skills_to_assess = st.text_area("🔍 Skills to Evaluate", 
                                           "Python, Machine Learning, Docker, Kubernetes, SQL, Data Visualization, Cloud Platforms", 
                                           height=120,
                                           help="List all skills you want assessed (technical and soft skills)")
            
        with col1:
            experience_level = st.selectbox(
                "📊 Current Experience Level",
                ("beginner", "intermediate", "advanced"),
                index=1,
                help="Your overall experience level in your field"
            )
            target_role = st.text_input("🎯 Target Role", "Senior Data Scientist", 
                                      help="The role you're aiming for")

        submitted = st.form_submit_button("🧠 Perform AI Skill Assessment")

        if submitted:
            payload = {
                "skills_to_assess": parse_comma_separated_input(skills_to_assess),
                "experience_level": experience_level,
                "target_role": target_role
            }
            response = call_api("skill_assessment", payload)
            if response and response.get('result'):
                st.markdown("### 📋 AI Skill Gap Analysis & Development Plan")
                st.markdown(f'<div class="output-container skill-theme">{response["result"]}</div>', unsafe_allow_html=True)
            elif response:
                st.error("The AI response did not contain the expected skill assessment data.")

# Enhanced Footer with branding
st.markdown("""
---
<div style="text-align: center; padding: 3rem 0; 
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
            border-radius: 20px; margin-top: 3rem; backdrop-filter: blur(10px);">
    <h3 style="color: #4facfe; margin-bottom: 1rem;">🎯 Careerzora</h3>
    <p style="color: #b3b3b3; margin: 0.5rem 0; font-size: 1rem;">
        Empowering careers through premium AI-driven insights and strategic development solutions
    </p>
    <div style="margin: 2rem 0;">
        <span style="color: #43e97b; margin: 0 1rem;">✨ Premium AI</span>
        <span style="color: #f093fb; margin: 0 1rem;">🎯 Strategic</span>
        <span style="color: #4facfe; margin: 0 1rem;">🚀 Professional</span>
    </div>
    <p style="color: #666; font-size: 0.9rem; margin-top: 2rem;">
        Built with ❤️ • Premium Edition • 
        <a href="#" style="color: #667eea;">Privacy Policy</a> • 
        <a href="#" style="color: #667eea;">Terms of Service</a>
    </p>
</div>
""", unsafe_allow_html=True)
