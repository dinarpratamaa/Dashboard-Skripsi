import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Penelitian AI Terhadap Strategi Pemasaran Digital",
    page_icon="logo_ibik.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .cta-button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Session state untuk login dan navigasi
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = " Beranda"
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Fungsi login
def login():
    st.markdown("###  Login untuk Mengakses Data Analisis")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # Kredensial sederhana untuk demo
            if username == "admin" and password == "@Admin2025":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login berhasil!")
                st.rerun()
            if username == "dinar" and password == "dinar123":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Username atau password salah!")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.data_loaded = False
    st.session_state.processed_data = None
    st.rerun()

def create_composite_variables(data, show_debug=False):
    """Fungsi standar untuk membuat variabel komposit """
    
    # Mapping kolom 
    composite_vars = {
        'X1': [
            '1. Penggunaan teknologi AI membantu saya mempercepat penyelesaian pekerjaan.',
            '2. Teknologi AI membuat pekerjaan saya menjadi lebih efektif.',
            '3. Teknologi AI mempermudah saya dalam melaksanakan tugas-tugas pemasaran digital.',
            '4. Teknologi AI meningkatkan produktivitas kerja saya dalam aktivitas pemasaran digital.'
        ],
        
        'X2': [
            '5.  Teknologi AI mudah saya pelajari. ',
            '6. Fitur-fitur dalam sistem AI jelas dan mudah dipahami.',
            '7. Saya merasa dapat mengendalikan penggunaan teknologi AI dengan baik.',
            '8. Saya merasa mudah menjadi terampil dalam menggunakan AI untuk pekerjaan saya.',
            '9. Saya merasa teknologi AI fleksibel untuk berinteraksi dengan berbagai kebutuhan pemasaran digital saya.'
        ],
        
        'X3': [
            '10. Saya memiliki niat untuk terus menggunakan teknologi AI dalam pekerjaan saya.',
            '11. Saya berencana menggunakan teknologi AI kembali di masa mendatang.',
            '12. Saya memiliki sikap positif terhadap penggunaan teknologi AI.',
            '13. Saya berniat merekomendasikan penggunaan teknologi AI kepada rekan kerja saya.'
        ],

        'X4': [
            '14. Saya sering menggunakan teknologi AI dalam aktivitas pemasaran digital saya.',
            '15. Saya menggunakan berbagai fitur AI untuk mendukung aktivitas pemasaran digital saya.',
            '16. Rata-rata, saya mengandalkan AI untuk mendukung aktivitas pemasaran digital saya.'
        ],
          
        'Y1': [
            '17. AI membantu saya mengenali target audiens dengan lebih tepat.',
            '18. AI memudahkan saya mengidentifikasi kebutuhan dan preferensi pelanggan.',
            '19. AI meningkatkan akurasi dalam menentukan segmen pasar.'
        ],

        'Y2': [
            '20. AI memungkinkan saya membuat konten yang lebih personal untuk audiens.',
            '21. AI membantu meningkatkan relevansi pesan pemasaran yang saya sampaikan.',
            '22. AI mendukung pembuatan pesan yang disesuaikan dengan perilaku pengguna.'
        ],

        'Y3': [
            '23. Saya merasa biaya pemasaran menjadi lebih efisien sejak menggunakan AI.',
            '24. AI membantu saya menentukan strategi pemasaran yang lebih hemat biaya.',
            '25. AI membantu saya meminimalisir pemborosan anggaran dalam kampanye pemasaran.'
        ],
        
        'Y4': [
            '26.  Interaksi dengan konsumen meningkat setelah saya menggunakan AI dalam kampanye.',
            '27. AI membantu mempertahankan hubungan jangka panjang dengan audiens digital.',
            '28. AI meningkatkan keterlibatan audiens terhadap konten yang saya buat.'
        ],
        
        'Y5': [
            '29. AI membantu saya menganalisis efektivitas kampanye dengan lebih akurat.',
            '30. AI membantu saya mengukur return on investment (ROI) dari aktivitas pemasaran digital.',
            '31. AI memberikan wawasan berbasis data yang mendukung pengambilan keputusan pemasaran saya.'
        ]
    }

    # Buat variabel komposit
    for var_name, columns in composite_vars.items():
        # Cek apakah semua kolom ada
        missing_cols = [col for col in columns if col not in data.columns]
        if missing_cols and show_debug:
            st.error(f"❌ Kolom tidak ditemukan untuk {var_name}:")
            for col in missing_cols:
                st.write(f"   - {col}")
            return None
        elif missing_cols:
            return None
        
        # Hitung rata-rata
        data[var_name] = data[columns].mean(axis=1)
        if show_debug:
            st.success(f"✅ Variabel {var_name} berhasil dibuat dari {len(columns)} indikator")
    
    return data

def validate_data_consistency(data, show_debug=False):
    """Validasi konsistensi data"""
    
    if show_debug:
        st.markdown("### Validasi Data")
        
        # Cek ukuran dataset
        st.write(f"**Ukuran dataset:** {data.shape}")
    
    # Cek statistik deskriptif variabel utama
    variables = ['X1', 'X2', 'X3', 'X4', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']
    
    if all(var in data.columns for var in variables):
        desc_stats = data[variables].describe().round(4)
        if show_debug:
            st.write("**Statistik Deskriptif:**")
            st.dataframe(desc_stats, use_container_width=True)
        
        # Cek missing values
        missing_data = data[variables].isnull().sum()
        if missing_data.sum() > 0:
            if show_debug:
                st.warning(f"⚠️ Missing values ditemukan:")
                for var, count in missing_data[missing_data > 0].items():
                    st.write(f"   - {var}: {count} missing values")
        else:
            if show_debug:
                st.success("✅ Tidak ada missing values ditemukan")
        
        # Cek range data (harus 1-5 untuk skala Likert)
        if show_debug:
            st.write("**Validasi Range Data (harus 1-5):**")
        for var in variables:
            min_val, max_val = data[var].min(), data[var].max()
            if min_val < 1 or max_val > 5:
                if show_debug:
                    st.warning(f"⚠️ {var}: Range data di luar 1-5 ({min_val:.2f} - {max_val:.2f})")
            else:
                if show_debug:
                    st.write(f"✅ {var}: Range valid ({min_val:.2f} - {max_val:.2f})")
        
        return True
    else:
        if show_debug:
            st.error("❌ Tidak semua variabel komposit berhasil dibuat")
        return False

# Load CSV dengan error handling yang tidak menampilkan debug secara default
@st.cache_data
def load_csv_data_silent():
    """Load data tanpa menampilkan debug info"""
    try:
        # Coba beberapa lokasi file yang mungkin
        possible_paths = [
            "data/Kuesioner Penelitian (Responses) - Form Responses 1.csv",
            "./data/Kuesioner Penelitian (Responses) - Form Responses 1.csv",
            "Kuesioner Penelitian (Responses) - Form Responses 1.csv",
            "data.csv"  # fallback name
        ]
        
        data = None
        file_path = None
        
        for path in possible_paths:
            if os.path.exists(path):
                data = pd.read_csv(path)
                file_path = path
                break
        
        if data is None:
            return None, None
        
        # Buat variabel komposit tanpa debug
        data = create_composite_variables(data, show_debug=False)
        
        if data is None:
            return None, None
        
        # Validasi data tanpa debug
        if not validate_data_consistency(data, show_debug=False):
            return None, None
        
        return data, file_path
        
    except Exception as e:
        return None, None

def load_csv_data_with_debug():
    """Load data dengan menampilkan semua debug info untuk halaman khusus"""
    try:
        # Coba beberapa lokasi file yang mungkin
        possible_paths = [
            "data/Kuesioner Penelitian (Responses) - Form Responses 1.csv",
            "./data/Kuesioner Penelitian (Responses) - Form Responses 1.csv",
            "Kuesioner Penelitian (Responses) - Form Responses 1.csv",
            "data.csv"  # fallback name
        ]
        
        data = None
        file_path = None
        
        for path in possible_paths:
            if os.path.exists(path):
                data = pd.read_csv(path)
                file_path = path
                break
        
        if data is None:
            st.error("❌ File CSV tidak ditemukan! Pastikan file berada di salah satu lokasi berikut:")
            for path in possible_paths:
                st.write(f"   - {path}")
            return None
        
        st.success(f"✅ Data berhasil dimuat dari: {file_path}")
        st.info(f" Total data: {len(data)} responden, {len(data.columns)} kolom")
        
        # Debug: Tampilkan 5 baris pertama data mentah
        with st.expander(" Debug: Preview Data Mentah"):
            st.dataframe(data.head(), use_container_width=True)
        
        # Tampilkan kolom yang tersedia untuk debugging
        with st.expander(" Kolom yang tersedia dalam dataset"):
            st.write("**Daftar semua kolom dalam CSV:**")
            for i, col in enumerate(data.columns, 1):
                st.write(f"{i}. {col}")
        
        # Debug: Tampilkan kolom untuk setiap pertanyaan
        with st.expander(" Debug: Mapping Kolom per Pertanyaan"):
            for i in range(1, 32):  # Asumsi 31 pertanyaan
                cols_found = [col for col in data.columns if f"{i}." in col]
                if cols_found:
                    st.write(f"**Q{i}:** {cols_found[0]}")
                else:
                    st.write(f"**Q{i}:** ❌ Tidak ditemukan")
        
        # Buat variabel komposit menggunakan fungsi standar
        st.markdown("###  Membuat Variabel Komposit")
        data = create_composite_variables(data, show_debug=True)
        
        if data is None:
            return None
        
        # Validasi data
        if not validate_data_consistency(data, show_debug=True):
            return None
        
        st.success(" Data berhasil diproses dan siap untuk analisis!")
        
        return data
        
    except Exception as e:
        st.error(f"❌ Error saat memuat data: {str(e)}")
        st.write("**Detail error:**")
        st.code(str(e))
        return None

# Fungsi regresi 
def run_unified_regression_analysis(data):
    """Fungsi regresi """
    
    if data is None:
        return {}, []
    
    results = {}
    regression_summary = []
    
    try:
        # Model 1: X2 → X1 
        X = sm.add_constant(data['X2'])
        model1 = sm.OLS(data['X1'], X).fit()
        results['Model 1: X2 → X1'] = model1
        
        # Model 2: X1 dan X2 → X3
        X = sm.add_constant(data[['X1', 'X2']])
        model2 = sm.OLS(data['X3'], X).fit()
        results['Model 2: X1 dan X2 → X3'] = model2
        
        # Model 3: X3 → X4
        X = sm.add_constant(data['X3'])
        model3 = sm.OLS(data['X4'], X).fit()
        results['Model 3: X3 → X4'] = model3
        
        # Models 4-8: X4 → Y1, Y2, Y3, Y4, Y5
        for i, y_var in enumerate(['Y1', 'Y2', 'Y3', 'Y4', 'Y5'], 4):
            X = sm.add_constant(data['X4'])
            model = sm.OLS(data[y_var], X).fit()
            results[f'Model {i}: X4 → {y_var}'] = model
        
        # Ekstrak hasil untuk perbandingan
        hipotesis = ['H1: X1 → X3', 'H2: X2 → X1', 'H3: X2 → X3', 'H4: X3 → X4',
                     'H5: X4 → Y1', 'H6: X4 → Y2', 'H7: X4 → Y3', 'H8: X4 → Y4', 'H9: X4 → Y5']
        
        models_list = [model2, model1, model2, model3, 
                       results['Model 4: X4 → Y1'], results['Model 5: X4 → Y2'], 
                       results['Model 6: X4 → Y3'], results['Model 7: X4 → Y4'], 
                       results['Model 8: X4 → Y5']]
        
        param_indices = [1, 1, 2, 1, 1, 1, 1, 1, 1]  # Index parameter yang relevan
        
        for i, (hip, model, param_idx) in enumerate(zip(hipotesis, models_list, param_indices)):
            coef = model.params.iloc[param_idx]
            p_val = model.pvalues.iloc[param_idx]
            r_squared = model.rsquared
            
            regression_summary.append({
                'Hipotesis': hip,
                'Koefisien': round(coef, 4),
                'p-value': round(p_val, 4),
                'R²': round(r_squared, 4),
                'Signifikan': 'Ya' if p_val < 0.05 else 'Tidak'
            })
        
        return results, regression_summary
        
    except Exception as e:
        st.error(f"❌ Error dalam analisis regresi: {str(e)}")
        return {}, []

# Sidebar navigation
st.sidebar.title("Dashboard Visualisasi dan Analisis")

if st.session_state.logged_in:
    st.sidebar.success(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        logout()

# Navigation dengan session state
page_options = [" Beranda", " Proses Data", " Analisis Data", " Visualisasi", " Tentang"]
selected_page = st.sidebar.selectbox(
    "Pilih Halaman",
    page_options,
    index=page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0
)

# Update current page
st.session_state.current_page = selected_page

# Load data untuk halaman yang membutuhkan (tanpa debug)
if st.session_state.current_page not in [" Proses Data"]:
    if not st.session_state.data_loaded:
        data, file_path = load_csv_data_silent()
        if data is not None:
            st.session_state.processed_data = data
            st.session_state.data_loaded = True
    else:
        data = st.session_state.processed_data
else:
    data = st.session_state.processed_data

# HALAMAN BERANDA
if st.session_state.current_page == " Beranda":
    # Header utama
    st.markdown("""
    <div class="main-header">
        <h1>Analisis Pengaruh Adopsi Teknologi AI terhadap Strategi Pemasaran Digital</h1>
        <p>Pendekatan Technology Acceptance Model dan Analisis Regresi Linear</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Latar Belakang
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Latar Belakang
        
        Perkembangan teknologi kecerdasan buatan (Artificial Intelligence/AI) telah mengubah lanskap pemasaran digital secara signifikan. Lebih dari 80% perusahaan global kini telah mengintegrasikan AI ke dalam strategi pemasaran mereka, khususnya melalui beberapa aplikasi utama, seperti:
        
        -  **Chatbot** untuk meningkatkan layanan pelanggan secara otomatis
        -  **Predictive Analytics** untuk melakukan prediksi tren dan perilaku konsumen
        -  **Content Automation** untuk menghasilkan konten yang lebih personal dan relevan secara efisien.
        
        Namun demikian, proses adopsi teknologi ini masih menghadapi berbagai tantangan, terutama di Indonesia. Salah satu faktor krusial yang memengaruhi tingkat adopsi adalah persepsi pelaku industri terhadap kemanfaatan (perceived usefulness) dan kemudahan penggunaan (perceived ease of use) dari teknologi AI itu sendiri. Pemahaman terhadap kedua aspek ini menjadi kunci untuk mendorong pemanfaatan AI secara optimal dalam strategi pemasaran digital.
        """)
    
    with col2:
        # Metrics cards
        if data is not None:
            total_responden = len(data)
        else:
            total_responden = "N/A"
            
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_responden}</h3>
            <p>Total Responden</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3>9</h3>
            <p>Hipotesis Diuji</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3>8</h3>
            <p>Model Regresi Diuji</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tujuan Penelitian
    st.markdown("## Tujuan Penelitian")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Variabel Technology Acceptance Model:**
        1. Menganalisis pengaruh *Perceived Usefulness* terhadap *Behavioral Intention*
        2. Menganalisis pengaruh *Perceived Ease of Use* terhadap *Perceived Usefulness*
        3. Menganalisis pengaruh *Perceived Ease of Use* terhadap *Behavioral Intention*
        4. Menganalisis pengaruh *Behavioral Intention* terhadap *Use Behavior*
        5. Menganalisis pengaruh *Use Behavior* terhadap *Lima dimensi Variabel Strategi Pemasaran Digital*
        """)
    
    with col2:
        st.markdown("""
        **Variabel Strategi Pemasaran Digital:**
        1. Targeting Audiens
        2. Konten Lebih Personal
        3. Efisiensi Anggaran Pemasaran
        4. Peningkatan Engagement Audiens
        5. Pengukuran & Analisis Hasil
        """)
    
    # Preview Visualisasi
    if data is not None:
        st.markdown("##  Preview Hasil Penelitian")
        
        # Correlation heatmap
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Korelasi Antar Variabel")
            variables = ['X1', 'X2', 'X3', 'X4', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']
            if all(var in data.columns for var in variables):
                corr_data = data[variables].corr()
                
                fig = px.imshow(corr_data, 
                               text_auto=True, 
                               aspect="auto",
                               color_continuous_scale='RdBu_r',
                               title="Matriks Korelasi")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Tidak dapat membuat matriks korelasi - variabel komposit belum tersedia")
        
        with col2:
            st.markdown("### Statistik Deskriptif")
            if all(var in data.columns for var in variables):
                desc_stats = data[variables].describe().round(3)
                st.dataframe(desc_stats, use_container_width=True)
            else:
                st.warning("⚠️ Tidak dapat menampilkan statistik deskriptif - variabel komposit belum tersedia")
        
        # Hasil Utama
        st.markdown(f"""
    ##  Metodologi Penelitian
    
    **Responden:** {total_responden} profesional pemasaran digital
    
    **Variabel Penelitian:**
    - **X1:** Perceived Usefulness (4 indikator)
    - **X2:** Perceived Ease of Use (5 indikator) 
    - **X3:** Behavioral Intention (4 indikator)
    - **X4:** Use Behavior (3 indikator)
    - **Y1-Y5:** 5 dimensi strategi pemasaran digital (masing-masing 3 indikator)
    
    **Analisis:**
    - Statistik deskriptif
    - Analisis korelasi Pearson
    - Regresi linear (OLS)
    - Uji signifikansi (α = 0.05)
    
    ##  Kesimpulan Utama
    
    1. **Model Technology Acceptance Model terbukti valid** dalam menjelaskan perilaku adopsi teknologi AI dalam konteks pemasaran digital.
    2. **Perceived Ease of Use** memiliki pengaruh signifikan terhadap **Perceived Usefulness** (β = 0.698), yang menunjukkan bahwa semakin mudah teknologi digunakan, semakin besar persepsi terhadap kegunaannya.
    3. **Behavioral Intention**  berperan sebagai penghubung penting menuju perilaku penggunaan aktual, dengan pengaruh yang sangat kuat (β = 0.836).
    4. **Use Behavior AI** terhadap teknologi AI memberikan dampak positif dan signifikan terhadap seluruh dimensi strategi pemasaran digital.
    5. Dampak paling menonjol terlihat pada dimensi **Targeting Audiens** (β = 0.817) dan **Efisiensi Anggaran** (β = 0.792), yang mengindikasikan pentingnya AI dalam mengenali audiens secara tepat dan mendorong interaksi yang lebih kuat.

    
    ##  Implikasi Praktis
    
    - **fokus pada kemudahan penggunaan  (ease of use)** menjadi langkah strategis untuk meningkatkan tingkat adopsi teknologi AI di kalangan pelaku pemasaran digital.
    - **Penyediaan pelatihan dan dukungan teknis (training & support)** akan memperkuat persepsi pengguna terhadap kemanfaatan AI dalam meningkatkan produktivitas kerja.
    - **Investasi dalam teknologi AI** terbukti mampu memberikan  **return on investment (ROI)** yang positif, terutama dalam hal efisiensi anggaran, personalisasi konten, dan efektivitas kampanye pemasaran secara menyeluruh.
    
    ##  Detail Teknis
    
    **Model Regresi yang Digunakan:**
    1. Model 1: X2 → X1 (Perceived Ease of Use → Perceived Usefulness)
    2. Model 2: X1, X2 → X3 (Perceived Usefulness, Ease of Use → Behavioral Intention)
    3. Model 3: X3 → X4 (Behavioral Intention → Use Behavior)
    4. Model 4-8: X4 → Y1,Y2,Y3,Y4,Y5 (Use Behavior → Digital Marketing Strategies)
    
    **Hipotesis yang Diuji:**
    - H1: Perceived Usefulness berpengaruh positif terhadap Behavioral Intention
    - H2: Perceived Ease of Use berpengaruh positif terhadap Perceived Usefulness
    - H3: Perceived Ease of Use berpengaruh positif terhadap Behavioral Intention
    - H4: Behavioral Intention berpengaruh positif terhadap Use Behavior
    - H5-H9: Use Behavior berpengaruh positif terhadap 5 dimensi strategi pemasaran digital

    **Regresi yang Diuji:**
    - Model 1: Perceived Ease of Use terhadap Behavioral Perceived Usefulness
    - Model 2: Perceived Usefulness dan Perceived Ease of Use terhadap Behavioral Intention
    - Model 3: Behavioral Intention berpengaruh positif terhadap Use Behavior
    - Model 4 - 8: Use Behavior  terhadap 5 dimensi strategi pemasaran digital
            """)
            
    
    # Call to Action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h3> Ingin Melihat Analisis Lengkap?</h3>
            <p>Akses data detail, model regresi, dan visualisasi interaktif</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Akses Data Analisis", type="primary", use_container_width=True):
            st.session_state.current_page = " Analisis Data"
            st.rerun()

# HALAMAN PROSES DATA
elif st.session_state.current_page == " Proses Data":
    st.title(" Proses Loading dan Validasi Data")
    
    st.markdown("""
    ### Informasi
    Halaman ini menampilkan proses loading data CSV, validasi, dan pembuatan variabel komposit dengan detail lengkap.
    """)
    
    if st.button("🔄 Mulai Proses Loading Data", type="primary"):
        # Load data dengan debug lengkap
        processed_data = load_csv_data_with_debug()
        
        if processed_data is not None:
            # Update session state
            st.session_state.processed_data = processed_data
            st.session_state.data_loaded = True
            
            st.markdown("---")
            st.success(" **Proses selesai!** Data siap digunakan untuk analisis.")
            
        else:
            st.error("❌ Gagal memproses data. Periksa file CSV Anda.")
    
    if st.session_state.data_loaded and st.session_state.processed_data is not None:
        st.markdown("---")
        st.info("✅ Data sudah diproses sebelumnya dan siap digunakan.")

# HALAMAN ANALISIS DATA
elif st.session_state.current_page == " Analisis Data":
    if not st.session_state.logged_in:
        st.markdown("## Silahkan Login")
        st.warning("untuk mengakses Analisis Data.")
        login()
    else:
        st.title(" Analisis Data Regresi")
        
        if data is None:
            st.error("❌ Data tidak tersedia. Silahkan ke halaman 'Proses Data' untuk memuat data terlebih dahulu.")
            if st.button(" Ke Halaman Proses Data"):
                st.session_state.current_page = " Proses Data"
                st.rerun()
        else:
            # Run regression analysis
            models, regression_summary = run_unified_regression_analysis(data)
            
            if models and regression_summary:
                # Tampilkan ringkasan hasil terlebih dahulu
                st.markdown("###  Ringkasan Hasil Semua Hipotesis")
                df_summary = pd.DataFrame(regression_summary)
                st.dataframe(df_summary, use_container_width=True)
                
                # Model selector
                model_names = list(models.keys())
                selected_model = st.selectbox("Pilih Model Regresi untuk Detail:", model_names)
                
                if selected_model:
                    model = models[selected_model]
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### {selected_model}")
                        st.markdown("**Ringkasan Model:**")
                        
                        # Model summary
                        r_squared = model.rsquared
                        adj_r_squared = model.rsquared_adj
                        p_value = model.f_pvalue
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("R²", f"{r_squared:.4f}")
                        with col_b:
                            st.metric("Adjusted R²", f"{adj_r_squared:.4f}")
                        with col_c:
                            st.metric("p-value", f"{p_value:.4f}")
                        
                        # Coefficients table
                        st.markdown("**Koefisien dan Signifikansi:**")
                        coef_data = []
                        for i, (var_name, coef, p_val) in enumerate(zip(model.model.exog_names, model.params, model.pvalues)):
                            significance = "Signifikan" if p_val < 0.05 else "Tidak Signifikan"
                            coef_data.append({
                                "Variabel": var_name,
                                "Koefisien (β)": f"{coef:.4f}",
                                "p-value": f"{p_val:.4f}",
                                "Status": significance
                            })
                        
                        st.dataframe(pd.DataFrame(coef_data), use_container_width=True)
                    
                    with col2:
                        st.markdown("### Model Fit")
                        # Residual plot
                        residuals = model.resid
                        fitted = model.fittedvalues
                        
                        fig = px.scatter(x=fitted, y=residuals, 
                                       title="Residuals vs Fitted Values",
                                       labels={"x": "Fitted Values", "y": "Residuals"})
                        fig.add_hline(y=0, line_dash="dash", line_color="red")
                        st.plotly_chart(fig, use_container_width=True)
 # HALAMAN VISUALISASI
elif st.session_state.current_page == " Visualisasi":
    if not st.session_state.logged_in:
        st.markdown("## Silahkan Login ")
        st.warning("untuk mengakses visualisasi.")
        login()
    else:
        st.title(" Visualisasi Hasil Penelitian")
        
        if data is None:
            st.error("❌ Data tidak tersedia. Silahkan ke halaman 'Proses Data' untuk memuat data terlebih dahulu.")
            if st.button(" Ke Halaman Proses Data"):
                st.session_state.current_page = " Proses Data"
                st.rerun()
        else:
            models, regression_summary = run_unified_regression_analysis(data)
            
            if models and regression_summary:
                # Hypothesis results visualization
                df_summary = pd.DataFrame(regression_summary)
                
                # Bar chart untuk koefisien
                colors = ['green' if status == 'Ya' else 'red' for status in df_summary['Signifikan']]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=df_summary['Hipotesis'], 
                        y=df_summary['Koefisien'],
                        marker_color=colors,
                        text=[f'β = {c:.3f}<br>p = {p:.4f}' for c, p in zip(df_summary['Koefisien'], df_summary['p-value'])],
                        textposition='outside'
                    )
                ])
                
                fig.update_layout(
                    title="Koefisien Regresi dan Signifikansi Hipotesis",
                    xaxis_title="Hipotesis",
                    yaxis_title="Koefisien Regresi (β)",
                    xaxis_tickangle=-45,
                    height=600
                )
                
                fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary table
                st.markdown("### Ringkasan Hasil Pengujian Hipotesis")
                st.dataframe(df_summary, use_container_width=True)
                
            # Correlation heatmap
            st.markdown("###  Matriks Korelasi Antar Variabel")
            variables = ['X1', 'X2', 'X3', 'X4', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']
            
            if all(var in data.columns for var in variables):
                corr_data = data[variables].corr()
                
                fig_corr = px.imshow(corr_data, 
                                   text_auto=True, 
                                   aspect="auto",
                                   color_continuous_scale='RdBu_r',
                                   title="Matriks Korelasi Variabel Penelitian")
                fig_corr.update_layout(height=600, width=800)
                st.plotly_chart(fig_corr, use_container_width=True)
            
            # Distribusi data
            st.markdown("###  Distribusi Variabel Penelitian")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Box plot untuk variabel independen
                tam_vars = ['X1', 'X2', 'X3', 'X4']
                if all(var in data.columns for var in tam_vars):
                    fig_box1 = go.Figure()
                    for var in tam_vars:
                        fig_box1.add_trace(go.Box(y=data[var], name=var))
                    
                    fig_box1.update_layout(
                        title="Distribusi Variabel Technology Acceptance Model",
                        yaxis_title="Nilai",
                        xaxis_title="Variabel"
                    )
                    st.plotly_chart(fig_box1, use_container_width=True)
            
            with col2:
                # Box plot untuk variabel dependen
                strategy_vars = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5']
                if all(var in data.columns for var in strategy_vars):
                    fig_box2 = go.Figure()
                    for var in strategy_vars:
                        fig_box2.add_trace(go.Box(y=data[var], name=var))
                    
                    fig_box2.update_layout(
                        title="Distribusi Variabel Strategi Pemasaran Digital",
                        yaxis_title="Nilai",
                        xaxis_title="Variabel"
                    )
                    st.plotly_chart(fig_box2, use_container_width=True)
            
            # Scatter plots untuk relationship key
            st.markdown("###  Scatter Plot Hubungan Kunci")
            
            # Key relationships
            key_relationships = [
                ('X2', 'X1', 'Perceived Ease of Use → Perceived Usefulness'),
                ('X3', 'X4', 'Behavioral Intention → Use Behavior'),
                ('X4', 'Y1', 'Use Behavior → Targeting Audiens'),
                ('X4', 'Y3', 'Use Behavior → Efisiensi Anggaran')
            ]
            
            fig_scatter = make_subplots(
                rows=2, cols=2,
                subplot_titles=[rel[2] for rel in key_relationships]
            )
            
            for i, (x_var, y_var, title) in enumerate(key_relationships):
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                if x_var in data.columns and y_var in data.columns:
                    fig_scatter.add_trace(
                        go.Scatter(
                            x=data[x_var], 
                            y=data[y_var],
                            mode='markers',
                            name=f'{x_var} vs {y_var}',
                            showlegend=False
                        ),
                        row=row, col=col
                    )
            
            fig_scatter.update_layout(height=600, title_text="Hubungan Antar Variabel Kunci")
            st.plotly_chart(fig_scatter, use_container_width=True)

# HALAMAN TENTANG
elif st.session_state.current_page == " Tentang":
    st.title(" Tentang Penelitian")
        
    st.markdown(f"""
    
    **Peneliti:** Muhammad Dinar Pratama Ilham
    
    **Tahun:** 2024 - 2025
    
    **Teknologi:** Python, Pandas, Statsmodels, Plotly, Streamlit
    """)
    
    # Tambahan informasi login
    if not st.session_state.logged_in:
        st.markdown("---")
        st.info("💡 **Tips:** Login untuk mengakses analisis lengkap!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>© 2025 Penelitian AI | Powered by Streamlit</p>
    <p>Muhammad Dinar Pratama Ilham  | Institut Bisnis dan Informatika Kesatuan</p>
</div>
""", unsafe_allow_html=True)