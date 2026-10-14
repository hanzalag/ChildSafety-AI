# Child-Safety-AI

Child-Safety-AI is a production-grade digital safety ecosystem designed to protect children from sociotechnical risks in AI-driven environments. Built for the Child Safety in AI hackathon, the platform delivers real-time content moderation, AI companion safety auditing, deepfake computer vision analysis, and a non-surveillant parent and educator dashboard.

---

## Challenge & Track Alignment

### Hackathon Track

**Child Safety in AI** (Addressing sociotechnical challenges of protecting children in an AI-powered world).

### Main Challenge

Children interact increasingly with LLM chat interfaces, synthetic media, and generative AI companions. Existing solutions either rely on blunt content filters that fail to detect psychological manipulation (such as online grooming and cyberbullying) or enforce invasive monitoring that violates child privacy and autonomy.

Child-Safety-AI addresses this gap by providing real-time psycholinguistic detection, safety auditing of third-party AI companions, computer vision deepfake identification, and aggregated analytics that inform caregivers without engaging in invasive surveillance.

---

## Project Description

### Problem Statement

1. **Online Harassment and Grooming:** Traditional keyword blocking misses subtle emotional manipulation, predatory rapport-building, and peer cyberbullying in youth communications.
2. **Unregulated AI Companions:** Conversational bots often lack age-appropriate boundaries, encouraging parasocial over-reliance or providing inappropriate guidance.
3. **Synthetic Media Exploitation:** Generative AI allows malicious actors to easily produce deepfake visuals and audio designed to scam, deceive, or harass minors.
4. **Excessive Surveillance vs. Safety:** Caregivers lack tools to monitor child safety metrics without constantly reading private messages.

<img width="879" height="636" alt="11" src="https://github.com/MuhammadHuzaifaG/Child-Safety-AI/blob/main/screenshots/ch1.PNG" />

### Solution

Child-Safety-AI combines asynchronous FastAPI web architecture, SQLAlchemy persistent storage, and Google Gemini API integration into four core modular services:

* **SafeChat Sentinel:** Analyzes incoming text messages for cyberbullying, toxicity, grooming patterns, and emotional distress. Provides real-time confidence scores and reframed alternative phrasing to promote positive digital citizenship.
* **SafeCompanion Guard:** Audits interactions between children and AI chatbots. Enforces human-AI boundary guidelines, flags emotional dependency indicators, and overrides harmful companion responses.
* **Media Detective (Computer Vision):** Inspects uploaded visual media for synthetic generation markers, deepfake artifacts, and manipulative content.
* **Non-Surveillant Parent & Educator Dashboard:** Displays aggregate safety KPIs, interactive trend charts, and moderation history logs without exposing raw message contents to caregivers.

### Target Users

* **Children and Youth:** Receive real-time protection from hostile communication, deepfake deception, and unsafe AI companion interactions.
* **Parents and Guardians:** Gain visibility into overall safety metrics and risk trends without reading private personal messages.
* **Educators and School Administrators:** Access exportable activity logs (CSV/Print) and analytics to evaluate digital wellness across student communities.

<img width="879" height="636" alt="11" src="https://github.com/MuhammadHuzaifaG/Child-Safety-AI/blob/main/screenshots/ch2.PNG" />

### Expected Impact

* **Emotional Well-being:** Reduces exposure to toxic communication and parasocial manipulation.
* **Digital Literacy:** Educates children on identifying synthetic media and deepfakes through actionable forensic feedback.
* **Privacy-Preserving Safety:** Establishes a balanced safety model that protects minors while respecting their personal privacy.

---

<img width="879" height="636" alt="11" src="https://github.com/MuhammadHuzaifaG/Child-Safety-AI/blob/main/screenshots/ch3.PNG" />

## Tech Stack

### Backend & AI Infrastructure

* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Database ORM:** SQLAlchemy 2.0 (Async Engine)
* **Database Driver:** AioSQLite (SQLite3 backend)
* **AI Model Integration:** Google Gemini API (`gemini-1.5-flash`) via `google-generativeai`

### Frontend Architecture

* **Markup & Templating:** HTML5, Jinja2
* **Styling:** CSS3 (Flexbox/Grid layout, custom responsive styling)
* **Dynamic Scripting:** JavaScript (Fetch API, asynchronous DOM operations)
* **Data Visualization:** Chart.js

---

## Key Features & Capabilities

* **Asynchronous Database Processing:** Persistent storage of user sessions, moderation events, companion safety audits, and visual forensic records.
* **Multimodal Forensics:** Computer vision processing for uploaded image files to detect artificial generation markers and harmful content.
* **Automated Data Sync:** Real-time polling updates the dashboard metrics and interactive charts every 5 seconds without full page refreshes.
* **Data Export Utilities:** Native print-to-PDF and CSV log generation for administrative compliance reporting.
* **Fail-Safe Heuristic Fallbacks:** Advanced NLP fallback engine ensures continuous operational stability during network disruptions or API key misconfigurations.

---

<img width="879" height="636" alt="11" src="https://github.com/MuhammadHuzaifaG/Child-Safety-AI/blob/main/screenshots/ch4.PNG" />

## Project Structure

```text
Child-Safety-AI/
├── config.py                 # Application settings and environment variable parser
├── database.py               # Asynchronous SQLAlchemy engine and session management
├── models.py                 # Database models (UserSession, ModerationLog, CompanionAudit, ImageAuditLog)
├── main.py                   # FastAPI initialization, middleware, static mounts, page routes
├── requirements.txt          # Python package dependencies
├── .env.example              # Environment configuration template
├── routers/                  # Modular API endpoints
│   ├── sentinel_router.py    # SafeChat Sentinel text analysis
│   ├── companion_router.py   # SafeCompanion Guard chatbot auditing
│   ├── detector_router.py    # Media Detective computer vision analysis
│   └── dashboard_router.py   # Dashboard metrics and analytics retrieval
├── services/                 # Core AI logic and integration layers
│   ├── gemini_service.py     # Gemini API integration and fallback heuristic engines
│   ├── moderation_service.py # Text moderation analysis service
│   └── audit_service.py      # AI companion boundary audit service
├── utils/                    # Utility functions
│   └── security.py           # Session identifier utilities
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css         # Responsive dark-theme styling
│   └── js/
│       └── app.js            # Client API requests, chart rendering, CSV export logic
└── templates/                # Jinja2 HTML templates
    ├── base.html             # Structural layout template
    ├── index.html            # Landing page
    ├── sentinel.html         # SafeChat Sentinel page
    ├── companion.html        # SafeCompanion Guard page
    ├── detector.html         # Media Detective computer vision page
    └── dashboard.html        # Parent & Educator analytics dashboard

```

---

## Local Setup Instructions

### Prerequisites

* Python 3.10 or higher
* `pip` package manager
* Google Gemini API key (Optional; system defaults to local heuristic processing if omitted)

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/muhammadhuzaifa/Child-Safety-AI.git
cd Child-Safety-AI

```


2. **Create and Activate a Virtual Environment**
* **Windows:**
```cmd
python -m venv venv
venv\Scripts\activate

```


* **macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt

```


4. **Configure Environment Variables**
Create a `.env` file in the root directory based on `.env.example`:
```env
APP_NAME=AegisYouth AI
DEBUG=True
SECRET_KEY=your_generated_secret_key
GEMINI_API_KEY=your_actual_gemini_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./aegisyouth.db

```


*Note: To generate a secure secret key, run:*
```bash
python -c "import secrets; print(secrets.token_hex(32))"

```


5. **Run the Application**
```bash
python main.py

```


Or run using Uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```


6. **Access the Web Interface**
Open your browser and navigate to `http://localhost:8000`.

---

## License

This project is open-source software built for the Child Safety in AI Hackathon.
