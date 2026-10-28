import streamlit as st
from google import interactions
import pandas as pd
from datetime import datetime

# --- SAHIFA SOZLAMALARI VA ZAMONAVIY CSS STILLAR ---
st.set_page_config(
    page_title="EduAI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Interfeysni professional ko'rinishga keltirish uchun CSS
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stSidebar {
        background-color: #1e293b;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background-color: #1e293b;
        color: white;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSIYA HOLATLARINI BOSHQARISH ---
if "users" not in st.session_state:
    st.session_state.users = {
        "Kamoljon Qobilov": "parol123",
        "Dilfuza Nurullayeva": "1234",
        "Xojakbar O'rinov": "pass567",
        "Temur Tolibov": "timur2026"
    }
if "results" not in st.session_state:
    st.session_state.results = []
if "attendance" not in st.session_state:
    st.session_state.attendance = {}

# --- ASOSIY SARLAVHA ---
st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1>🚀 EduAI: Professional Mock & Skill Analitika Tizimi</h1>
        <p style='color: #94a3b8; font-size: 1.1rem;'>O'quv markazlari uchun sun'iy intellektga asoslangan zamonaviy boshqaruv platformasi</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR: KIRISH VA ROLDAR ---
st.sidebar.markdown("### 🔐 Tizimga Xavfsiz Kirish")
role = st.sidebar.selectbox("Rolingizni tanlang:", ["O'qituvchi", "O'quvchi"])

if role == "O'quvchi":
    st.sidebar.markdown("---")
    st.sidebar.subheader("👨‍🎓 O'quvchi Kabineti")
    student_names = list(st.session_state.users.keys())
    username = st.sidebar.selectbox("Ismingizni tanlang:", student_names)
    password = st.sidebar.text_input("Parol:", type="password")
    
    logged_in = False
    if username and password:
        if username in st.session_state.users and st.session_state.users[username] == password:
            logged_in = True
            st.sidebar.success(f"Xush kelibsiz, {username}!")
        else:
            st.sidebar.error("Parol xato!")

    if logged_in:
        st.markdown(f"### 📝 O'quvchi paneli: <span style='color: #38bdf8;'>{username}</span>", unsafe_allow_html=True)
        
        tab_w, tab_s, tab_g, tab_m = st.tabs(["✍️ Writing Mock", "🗣️ Speaking AI Tahlil", "📚 Grammar Test", "📊 Mening Natijalarim"])
        
        with tab_w:
            st.subheader("Writing Imtihoni")
            w_topic = st.text_input("Writing Mavzusi:")
            w_text = st.text_area("Essay matnini kiriting:", height=250, placeholder="Inssay matnini shu yerga yozing...")
            
            if st.button("Writingni Topshirish"):
                if not w_topic or not w_text:
                    st.warning("Mavzu va matnni to'liq kiriting.")
                else:
                    st.success("Writing muvaffaqiyatli topshirildi va o'qituvchiga yuborildi!")
                    st.session_state.results.append({
                        "Student": username, "Type": "Writing", "Topic": w_topic, "Content": w_text, "Status": "Tekshirilmoqda"
                    })

        with tab_s:
            st.subheader("Speaking Mock - AI Ekspert Tahlili")
            s_mode = st.selectbox("Format:", ["CEFR", "IELTS"])
            s_text = st.text_area("Speaking transkripsiyasini kiriting:", height=150, placeholder="Nutq matnini shu yerga joylashtiring...")
            
            if st.button("AI orqali tahlil qilish"):
                api_key_s = st.text_input("Gemini API Key:", type="password")
               if s_text:
    with st.spinner("AI tahlil qilmoqda..."):
        natija = ai_tahlil(s_text)
    st.info("🤖 AI Tahlili va Tavsiyalar:")
    st.markdown(natija)
else:
    st.warning("Matnni kiriting.")

        with tab_g:
            st.subheader("Haftalik Grammar Testi (30 talik)")
            g_score = st.slider("To'g'ri topgan javoblar soni:", 0, 30, 15)
            if st.button("Natijani ko'rish"):
                st.metric(label="Sizning natijangiz", value=f"{g_score} / 30")
                if g_score >= 25:
                    st.success("Ajoyib natija!")
                else:
                    st.warning("Zamonlarni takrorlashingiz kerak.")

        with tab_m:
            st.subheader("📊 Shaxsiy Statistika")
            st.info("Barcha topshiriqlaringiz ko'rib chiqish jarayonida.")

elif role == "O'qituvchi":
    st.sidebar.markdown("---")
    st.sidebar.subheader("👨‍🏫 O'qituvchi Kabineti")
    teacher_pass = st.sidebar.text_input("Admin paroli:", type="password")
    
    if teacher_pass == "admin123":
        st.markdown("### 🛠️ O'qituvchi Boshqaruv Markazi")
        if s_text:
    with st.spinner("AI tahlil qilmoqda..."):
        natija = ai_tahlil(s_text)
    st.info("🤖 AI Tahlili va Tavsiyalar:")
    st.markdown(natija)
else:
    st.warning("Matnni kiriting.")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 O'quvchilar", "📋 Davomat", "📝 Mock Boshqaruvi", "🤖 AI Tekshiruv", "📊 Excel Hisobot"])
        
        with tab1:
            st.subheader("O'quvchilar Bazasini Boshqarish")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Yangi O'quvchi Qo'shish")
                new_name = st.text_input("O'quvchining F.I.O:")
                new_pass = st.text_input("Parol o'rnatish:", value="1234")
                if st.button("Bazaga Qo'shish"):
                    if new_name:
                        st.session_state.users[new_name] = new_pass
                        st.success("O'quvchi muvaffaqiyatli qo'shildi!")
                        st.rerun()
                    else:
                        st.warning("Ismni kiriting.")
            
            with col2:
                st.markdown("#### Mavjud O'quvchilar")
                for s_name in list(st.session_state.users.keys()):
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"👤 {s_name}")
                    if c2.button("O'chirish", key=f"del_{s_name}"):
                        del st.session_state.users[s_name]
                        st.success("O'chirildi!")
                        st.rerun()

        with tab2:
            st.subheader("Dars Davomatini Qayd Etish")
            date_today = st.date_input("Dars sanasi:", datetime.now())
            students_list = list(st.session_state.users.keys())
            attendance_data = {}
            
            for s in students_list:
                attendance_data[s] = st.checkbox(f"{s} - Qatnashdi", value=True)
            
            if st.button("Davomatni Saqlash"):
                st.session_state.attendance[str(date_today)] = attendance_data
                st.success("Davomat saqlandi!")

        with tab3:
            st.subheader("Mock Test Ballarini Kiritish")
            if len(st.session_state.users) > 0:
                sel_student = st.selectbox("O'quvchini tanlang:", list(st.session_state.users.keys()), key="mock_sel")
                r_score = st.number_input("Reading balli (0-35):", 0, 35, 30)
                l_score = st.number_input("Listening balli (0-35):", 0, 35, 30)
                
                if st.button("Natijalarni Saqlash"):
                    st.success(f"{sel_student} natijalari saqlandi!")
            else:
                st.warning("Avval o'quvchi qo'shing!")

        with tab4:
            st.subheader("AI Orqali Essay Tekshiruvi")
            essay_sample = st.text_area("O'quvchi essay matni:")
            if st.button("AI Tahlilini Olish"):
                if api_key and essay_sample:
                    try:
                        client = interactions.Client(api_key=api_key)
                        prompt = f"Ushbu essayni tahlil qiling va o'qituvchiga tavsiyalar bering: {essay_sample}"
                        response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
                        st.markdown("### 📋 AI Ekspert Xulosasi:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Xatolik: {e}")
                else:
                    st.warning("API kalit va matnni kiriting.")

        with tab5:
            st.subheader("📊 Umumiy Hisobot va Excel Eksport")
            df = pd.DataFrame([
                {"O'quvchi": name, "Reading": 32, "Listening": 34, "Status": "Faol"}
                for name in st.session_state.users.keys()
            ])
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Excel (CSV) formatida yuklab olish",
                data=csv,
                file_name='oquvchilar_natijalari.csv',
                mime='text/csv'
            )
    else:
        if teacher_pass:
            st.sidebar.error("Parol noto'g'ri!")
        else:
            st.sidebar.warning("Admin parolini kiriting (Standart: admin123)")
