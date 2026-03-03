import streamlit as st
import joblib
import numpy as np

# HOSPITAL THEME CONFIG
st.set_page_config(page_title="🏥 Patient Vital Monitor", page_icon="🚨", layout="wide")

# PERFECT CSS - WHITE TEXT ON DARK INPUTS (FIXED)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    .main { 
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
        padding: 2rem; 
        color: #ffffff !important;
    }
    
    .hospital-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e) !important;
        border-radius: 15px; 
        padding: 2rem;
        border-left: 5px solid #00d4ff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin: 1rem 0;
        color: #ffffff !important;
    }
    
    .normal-card { 
        border-left: 5px solid #00ff88 !important; 
        background: linear-gradient(145deg, #0f4d1f, #1a5e2a) !important;
    }
    
    .critical { 
        border-left: 5px solid #ff4444 !important; 
        animation: pulse 1s infinite !important;
        background: linear-gradient(45deg, #ff1a1a, #ff4444) !important;
    }
    
    .stMarkdown, h1, h2, h3, h4, p, li, div, span, label {
        color: #ffffff !important;
    }
    
    /* *** FIXED: WHITE TEXT ON DARK INPUT BOXES *** */
    .stNumberInput > div > div > div > input {
        background: rgba(20, 20, 60, 0.9) !important;  /* DARK BLUE */
        border: 2px solid #00d4ff !important;
        border-radius: 12px !important;
        color: #ffffff !important;  /* WHITE TEXT */
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    
    /* INPUT LABELS WHITE */
    .stNumberInput > label {
        color: #ffffff !important;
    }
    
    /* PLACEHOLDER WHITE */
    input::placeholder {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #0099cc) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    .siren-text {
        animation: flash 0.5s infinite alternate;
        color: #ffff00 !important;
        font-size: 2.2em;
        font-weight: bold;
        text-shadow: 0 0 20px #ff0000;
        text-align: center;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,68,68,0.7); }
        70% { box-shadow: 0 0 0 20px rgba(255,68,68,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,68,68,0); }
    }
    
    @keyframes flash { 0% { opacity: 1; } 100% { opacity: 0.8; } }
    @keyframes gradientShift { 
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load models
@st.cache_resource
def load_models():
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

model, scaler = load_models()

# HEADER
st.markdown("""
<div class='hospital-card'>
    <h1 style='text-align: center; font-size: 2.8em;'>🚨 PATIENT VITAL SIGNS MONITOR</h1>
    <p style='text-align: center; font-size: 1.2em; color: #00ff88;'>AI Emergency Detection System</p>
</div>
""", unsafe_allow_html=True)

# INPUTS - 2x2 GRID
st.markdown("<h2 style='color: #00d4ff; text-align: center;'>📊 Enter Patient Vitals</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown("<div class='hospital-card normal-card'>", unsafe_allow_html=True)
    st.markdown("### 💓 Cardiovascular")
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=0.0, value=72.0)
    systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=0.0, value=120.0)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='hospital-card normal-card'>", unsafe_allow_html=True)
    st.markdown("### 🫁 Respiratory")
    respiratory_rate = st.number_input("Resp Rate (br/min)", min_value=0.0, value=16.0)
    oxygen_saturation = st.number_input("O₂ Sat (%)", min_value=0.0, value=98.0)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='hospital-card normal-card'>", unsafe_allow_html=True)
    st.markdown("### 🩸 Blood Pressure")
    diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=0.0, value=80.0)
    mean_arterial_pressure = st.number_input("MAP (mmHg)", min_value=0.0, value=93.0)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='hospital-card normal-card'>", unsafe_allow_html=True)
    st.markdown("### 🌡️ Temperature")
    body_temperature = st.number_input("Body Temp (°C)", min_value=20.0, value=36.8)
    st.markdown("</div>", unsafe_allow_html=True)

# EMERGENCY SCAN
if st.button("🚨 EMERGENCY SCAN & DIAGNOSE", type="primary", use_container_width=True):
    
    with st.spinner("🔬 AI Clinical Analysis..."):
        raw_features = np.array([[heart_rate, respiratory_rate, systolic_bp, diastolic_bp, 
                                mean_arterial_pressure, oxygen_saturation, body_temperature]])
        scaled_features = scaler.transform(raw_features)
        prediction = model.predict(scaled_features)[0]
    
    st.markdown("---")
    
    if prediction == -1:
        # CRITICAL ALERT
        st.markdown("""
        <div class='hospital-card critical'>
            <div class='siren-text'>🚨 CODE BLUE - CRITICAL PATIENT 🚨</div>
            <h2 style='color: #ffffff; text-align: center;'>IMMEDIATE INTERVENTION REQUIRED</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(90deg, #ff1a1a, #ff4444, #ff1a1a); 
                    background-size: 200% 100%; animation: gradientShift 2s ease infinite; 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0; text-align: center;'>
            <h3 style='color: #ffff00; margin: 0; font-size: 1.8em;'>🔊 EMERGENCY ALARM ACTIVE</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # DIAGNOSES
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚨 Critical Findings")
            if heart_rate > 140: st.error("🚨 **SEVERE TACHYCARDIA** >140 bpm")
            elif heart_rate > 100: st.warning("⚠️ Tachycardia")
            elif heart_rate < 50: st.error("🚨 **BRADYCARDIA** <50 bpm")
            
            if systolic_bp > 180: st.error("🚨 **HYPERTENSIVE CRISIS**")
            elif systolic_bp < 90: st.error("🚨 **HYPOTENSIVE SHOCK**")
        
        with col2:
            if respiratory_rate > 30: st.error("🚨 **TACHYPNEA** >30/min")
            elif respiratory_rate < 10: st.error("🚨 **BRADYPNEA** <10/min")
            
            if oxygen_saturation < 90: st.error("🚨 **SEVERE HYPOXIA** <90%")
            elif oxygen_saturation < 94: st.warning("⚠️ Hypoxemia")
            
            if body_temperature > 40: st.error("🚨 **HYPERPYREXIA** >40°C")
            elif body_temperature > 38.5: st.warning("🔥 High Fever")
            elif body_temperature < 35: st.error("🚨 **HYPOTHERMIA**")
        
        # PROTOCOLS
        st.markdown("""
        <div style='background: linear-gradient(145deg, #d32f2f, #b71c1c); 
                    color: white; padding: 2rem; border-radius: 15px;'>
            <h3 style='color: #ffff00; text-align: center;'>🩺 EMERGENCY PROTOCOLS</h3>
            <ul style='font-size: 1.1em; line-height: 1.8;'>
                <li>📞 STAT Call Attending Physician</li>
                <li>💉 IV Access + NS 500ml bolus</li>
                <li>🫁 O₂ 10L/min non-rebreather</li>
                <li>📋 ECG, Blood gases, Labs STAT</li>
                <li>🚨 Prepare ICU bed immediately</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div class='hospital-card normal-card' style='background: linear-gradient(145deg, #00b140, #00e676);'>
            <h2 style='color: white; text-align: center; font-size: 2.5em;'>✅ PATIENT STABLE</h2>
            <p style='color: white; font-size: 1.3em; text-align: center;'>All vitals normal</p>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #00d4ff; font-size: 1.1em;'>
    🩺 Hospital Emergency Monitor v2.0
</div>
""", unsafe_allow_html=True)
