import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import random

st.set_page_config(
    page_title="Add Fees", 
    page_icon="💰", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ==================== THEME CSS ====================
THEME_CSS = """
<style>
    body {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .section-header {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border-left: 4px solid #A9C5D8;
        padding: 15px 20px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 600;
        margin: 20px 0 15px 0;
    }
    
    .stSelectbox select, .stTextInput input, .stNumberInput input, .stDateInput input {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label {
        color: #b4a7c6 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #A9C5D8 0%, #9B8BA8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
    }
    
    /* Hide top navigation toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Hide header elements */
    header {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    /* Hide entire sidebar and all sidebar elements */
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }
    
    /* Hide Streamlit's automatic page navigation in sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }
    
    /* Hide sidebar toggle buttons */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    button[kind="header"] {
        display: none !important;
    }
</style>
"""

st.html(THEME_CSS)

# ==================== BACK BUTTON ====================
if st.button("← Back to Dashboard", use_container_width=True, key="back_btn"):
    st.switch_page("pages/teacher_dashboard.py")

st.markdown("<div class='header-title'>💰 Add & Manage Fees</div>", unsafe_allow_html=True)

# ==================== INITIALIZE DATA ====================
FEES_FILE = "data/fees.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(FEES_FILE):
    fees_df = pd.DataFrame({
        "receipt_no": [],
        "book_no": [],
        "physical_receipt_no": [],
        "date": [],
        "roll_no": [],
        "program": [],
        "year_semester": [],
        "student_name": [],
        "father_name": [],
        "on_accounts_of": [],
        "payment_mode": [],
        "amount": [],
        "amount_words": [],
        "printed_on": [],
        "issued_by": [],
        "status": []
    })
    fees_df.to_csv(FEES_FILE, index=False)
else:
    fees_df = pd.read_csv(FEES_FILE)

# ==================== CONFIGURATION ====================
FEE_TYPES = {
    "Semester Fees": "Semester Exchange",
    "Examination Fees": "Examination Exchange"
}

PAYMENT_MODES = ["Cash", "Online", "Cheque", "Demand Draft"]

STUDENTS = [
    {"roll_no": "25267546", "name": "Divanshi Khosla", "father": "Mohit Khosla"},
    {"roll_no": "25267547", "name": "Student 2", "father": "Father 2"},
    {"roll_no": "25267548", "name": "Student 3", "father": "Father 3"},
    {"roll_no": "25267549", "name": "Student 4", "father": "Father 4"},
    {"roll_no": "25267550", "name": "Student 5", "father": "Father 5"},
    {"roll_no": "25267551", "name": "Student 6", "father": "Father 6"},
    {"roll_no": "25267552", "name": "Student 7", "father": "Father 7"},
    {"roll_no": "25267553", "name": "Student 8", "father": "Father 8"}
]

def amount_to_words(amount):
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    
    if amount == 0:
        return "Zero"
    
    if amount < 10:
        return ones[amount]
    elif amount < 20:
        twenty = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 
                  'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        return twenty[amount - 10]
    elif amount < 100:
        return tens[amount // 10] + (' ' + ones[amount % 10] if amount % 10 != 0 else '')
    elif amount < 1000:
        return ones[amount // 100] + ' Hundred' + (' ' + amount_to_words(amount % 100) if amount % 100 != 0 else '')
    elif amount < 100000:
        return amount_to_words(amount // 1000) + ' Thousand' + (' ' + amount_to_words(amount % 1000) if amount % 1000 != 0 else '')
    elif amount < 10000000:
        return amount_to_words(amount // 100000) + ' Lakh' + (' ' + amount_to_words(amount % 100000) if amount % 100000 != 0 else '')
    
    return str(amount)

# ==================== TABS ====================
tab1, tab2 = st.tabs(["Add Fee", "View Records"])

# ==================== TAB 1: ADD FEES ====================
with tab1:
    st.markdown("<div class='section-header'>📝 Enter Fee Details</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fee_type = st.selectbox("Fee Type", list(FEE_TYPES.keys()), label_visibility="collapsed", key="fee_type")
    
    with col2:
        payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES, label_visibility="collapsed", key="payment_mode")
    
    with col3:
        fee_date = st.date_input("Date", value=date.today(), label_visibility="collapsed", key="fee_date")
    
    st.markdown("<div class='section-header'>💸 Fee Collection</div>", unsafe_allow_html=True)
    
    fees_records = []
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        st.write("**Roll No**")
    with col2:
        st.write("**Amount (Rs.)**")
    with col3:
        st.write("**Payment Mode**")
    with col4:
        st.write("**Status**")
    
    st.divider()
    
    for student in STUDENTS:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            st.write(f"{student['roll_no']}")
        
        with col2:
            amount = st.number_input(
                f"Amount for {student['roll_no']}", 
                min_value=0, 
                value=2500,
                key=f"amount_{student['roll_no']}", 
                label_visibility="collapsed", 
                step=100
            )
        
        with col3:
            mode = st.selectbox(
                f"Mode for {student['roll_no']}", 
                PAYMENT_MODES,
                key=f"mode_{student['roll_no']}", 
                label_visibility="collapsed"
            )
        
        with col4:
            status = st.selectbox(
                f"Status for {student['roll_no']}", 
                ["Verified", "Pending"],
                key=f"status_{student['roll_no']}", 
                label_visibility="collapsed"
            )
        
        receipt_no = f"UIE-{random.randint(10000, 99999)}"
        book_no = random.randint(2000, 2200)
        physical_receipt_no = random.randint(1, 100)
        amount_words = f"Rupees {amount_to_words(amount)} ONLY"
        on_accounts_of = f"{FEE_TYPES[fee_type]}:{amount}"
        
        fees_records.append({
            "receipt_no": receipt_no,
            "book_no": book_no,
            "physical_receipt_no": physical_receipt_no,
            "date": str(fee_date),
            "roll_no": student['roll_no'],
            "program": "Bachelor's in Computer Application",
            "year_semester": "3/7",
            "student_name": student['name'],
            "father_name": student['father'],
            "on_accounts_of": on_accounts_of,
            "payment_mode": mode,
            "amount": amount,
            "amount_words": amount_words,
            "printed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "issued_by": "System (S1001) System",
            "status": status
        })
    
    if st.button("💾 Save Fee Records", use_container_width=True, key="save_fees_btn"):
        try:
            new_df = pd.DataFrame(fees_records)
            st.dataframe(new_df, use_container_width=True)
            
            divanshi_records = [record for record in fees_records if record["roll_no"] == "25267546"]
            
            if divanshi_records:
                if os.path.exists(FEES_FILE):
                    existing_fees = pd.read_csv(FEES_FILE)
                    new_records_df = pd.DataFrame(divanshi_records)
                    combined_df = pd.concat([existing_fees, new_records_df], ignore_index=True)
                else:
                    combined_df = pd.DataFrame(divanshi_records)
                
                combined_df.to_csv(FEES_FILE, index=False)
                st.info(f"✅ Roll No 25267546 (Divanshi Khosla) fee auto-saved to fees.csv!")
            
            st.success("✅ Fee records saved successfully!")
        except Exception as e:
            st.error(f"❌ Error saving fee records: {str(e)}")

# ==================== TAB 2: VIEW RECORDS ====================
with tab2:
    st.markdown("<div class='section-header'>📊 View Fee Records</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_fee_type = st.selectbox("Filter by Fee Type", ["All"] + list(FEE_TYPES.keys()), key="filter_fee_type")
    
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Verified", "Pending"], key="filter_status")
    
    with col3:
        filter_roll = st.text_input("Filter by Roll No", key="filter_roll", placeholder="e.g., 25267546")
    
    try:
        filtered_df = fees_df.copy()
        
        if filter_fee_type != "All":
            fee_type_prefix = FEE_TYPES[filter_fee_type]
            filtered_df = filtered_df[filtered_df["on_accounts_of"].str.contains(fee_type_prefix, na=False)]
        
        if filter_status != "All":
            filtered_df = filtered_df[filtered_df["status"] == filter_status]
        
        if filter_roll:
            filtered_df = filtered_df[filtered_df["roll_no"].astype(str).str.contains(filter_roll)]
        
        if not filtered_df.empty:
            display_columns = ["receipt_no", "date", "roll_no", "student_name", "on_accounts_of", "amount", "payment_mode", "status"]
            display_df = filtered_df[[col for col in display_columns if col in filtered_df.columns]]
            
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("<div class='section-header'>📈 Statistics</div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(filtered_df))
            
            with col2:
                total_amount = pd.to_numeric(filtered_df["amount"], errors='coerce').sum()
                st.metric("Total Amount (Rs.)", f"₹{total_amount:,.0f}")
            
            with col3:
                verified_count = len(filtered_df[filtered_df["status"] == "Verified"])
                st.metric("Verified", verified_count)
            
            with col4:
                pending_count = len(filtered_df[filtered_df["status"] == "Pending"])
                st.metric("Pending", pending_count)
        else:
            st.info("📭 No fee records found with the selected filters.")
    
    except Exception as e:
        st.error(f"❌ Error loading records: {str(e)}")