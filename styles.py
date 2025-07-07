CUSTOM_CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    color: #222;
    background-color: #f9f9f9;
}

.stApp {
    background-color: #f9f9f9;
}

.stSidebar {
    background-color: #ffffff;
    padding: 20px;
    box-shadow: 2px 0px 5px rgba(0,0,0,0.03);
    border-radius: 10px;
}

.stSidebar h2 {
    color: #2196F3;
    font-weight: 700;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #2196F3;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
}

.stButton>button:hover {
    background-color: #1976D2;
    transform: translateY(-3px);
    box-shadow: 0 6px 8px rgba(0,0,0,0.10);
}

.stTextInput>div>div>input, .stSelectbox>div>div>select, .stDateInput>div>div>input {
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    padding: 10px 12px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    background-color: #ffffff;
    color: #000000 !important;
    font-weight: 500;
}

.stTextInput>div>div>input:focus, .stSelectbox>div>div:focus-within, .stDateInput>div>div:focus-within {
    border-color: #2196F3;
    box-shadow: 0 0 0 0.2rem rgba(33, 150, 243, 0.15);
    outline: none;
}

.stMetric {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.07);
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-left: 5px solid #2196F3;
}

.stMetric:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.10);
}

.stMetric label {
    font-size: 1.2em;
    font-weight: 600;
    color: #444;
    margin-bottom: 5px;
}

.stMetric .css-1g6x9st-StMetric {
    font-size: 2.2em !important;
    font-weight: 700;
    color: #222;
}

.icon {
    margin-right: 8px;
    vertical-align: middle;
}

.fade-in {
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.st-emotion-cache-1c7y2kl {
    padding: 2rem 3rem;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

h1, h2, h3, h4, h5, h6 {
    color: #222;
    font-weight: 700;
}

p {
    line-height: 1.6;
    color: #222;
}

.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
    background: #fff;
}

/* Fix for selectbox text visibility */
div[data-baseweb="select"] div[class*="SingleValue"],
div[data-baseweb="select"] div[class*="Placeholder"],
div[data-baseweb="select"] div[class*="ValueContainer"],
div[data-baseweb="select"] input {
    color: #000000 !important;
    background-color: #ffffff !important;
    font-weight: 500 !important;
}

div[data-baseweb="menu"],
div[data-baseweb="select"] ul {
    background-color: #ffffff !important;
    color: #000000 !important;
}

div[data-baseweb="menu"] li {
    color: #000000 !important;
    background-color: #ffffff !important;
}

div[data-baseweb="menu"] li:hover {
    background-color: #1976D2 !important;
    color: white !important;
}

.stAlert > div {
    background-color: #dff0d8;
    color: #3c763d;
}

.stAlert[data-testid="stAlert"][role="alert"][data-baseweb="notification"] > div {
    background-color: #dff0d8;
    color: #3c763d;
}

.stAlert[data-testid="stAlert"][role="alert"][data-baseweb="notification"][kind="warning"] > div {
    background-color: #fcf8e3;
    color: #8a6d3b;
}

.stAlert[data-testid="stAlert"][role="alert"][data-baseweb="notification"][kind="error"] > div {
    background-color: #f2dede;
    color: #dc3545;
}

.stAlert[data-testid="stAlert"][role="alert"][data-baseweb="notification"][kind="info"] > div {
    background-color: #d9edf7;
    color: #31708f;
}
''' 