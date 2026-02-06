# ✈️ AI Smart Travel Ops Assistant

An intelligent AI-powered travel safety assistant that provides real-time recommendations by analyzing weather conditions and news alerts using a 3-agent system powered by Groq's Llama 3.3.

## 🚀 Quick Start (Single Command)

```bash
streamlit run app.py
```

This launches a beautiful web interface at `http://localhost:8501`

## 📋 Features

✅ **3-Agent System**
- **Planner Agent**: Analyzes queries and creates structured execution plans
- **Executor Agent**: Calls external APIs (Weather + News)
- **Verifier Agent**: Validates results and generates AI-powered recommendations

✅ **Dual Interfaces**
- **Web UI**: Interactive Streamlit dashboard with real-time progress tracking
- **CLI**: Command-line interface for quick queries

✅ **Real-time Data**
- OpenWeatherMap API for weather conditions
- NewsData.io API for safety alerts and news
- RSS fallback for news when primary API fails

✅ **AI-Powered Analysis**
- Groq Cloud API (Llama 3.3 70B Versatile)
- JSON-structured output
- Travel safety scoring (0-10 scale)

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- API Keys (all free tier):
  - [Groq API](https://console.groq.com/keys)
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [NewsData.io](https://newsdata.io/api-key)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-travel-assistant
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```
   
   Edit `.env` and add your API keys:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   GROQ_MODEL_ID=llama-3.3-70b-versatile
   OPENWEATHER_API_KEY=your_openweather_api_key
   NEWSDATA_API_KEY=your_newsdata_api_key
   ```

5. **Run the application**
   
   **Web Interface (Recommended):**
   ```bash
   streamlit run app.py
   ```
   
   **CLI Interface:**
   ```bash
   python main.py "Is it safe to travel to Mumbai tomorrow?"
   ```

## 💻 Usage

### Web Interface

1. Start the server: `streamlit run app.py`
2. Open browser at `http://localhost:8501`
3. Enter your travel query
4. Click "🚀 Get Recommendation"
5. View results with weather, alerts, and AI recommendations

### CLI Interface

```bash
python main.py "Your travel safety question here"
```

**Example queries:**
```bash
python main.py "Is it safe to travel to Paris next week?"
python main.py "Weather conditions in Tokyo tomorrow?"
python main.py "Travel safety to Iran from Delhi on Feb 10?"
```

## 🏗️ Project Structure

```
ai-travel-assistant/
├── app.py                 # Streamlit web interface
├── main.py                # CLI interface
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not in git)
├── .env.example           # Template for API keys
├── agents/
│   ├── planner.py         # Planner Agent (Query → Plan)
│   ├── executor.py        # Executor Agent (Plan → API Calls)
│   └── verifier.py        # Verifier Agent (Results → Recommendation)
├── llm/
│   └── llm_client.py      # Groq API client
└── tools/
    ├── weather_tool.py    # OpenWeatherMap integration
    ├── news_tool.py       # NewsData.io integration
    └── rss_tool.py        # RSS fallback tool
```

## 📊 Sample Output

```json
{
  "destination": "Paris",
  "date": "2026-02-13",
  "weather": {
    "condition": "Clear sky with moderate humidity",
    "temperature": 8.5
  },
  "alerts": [
    "No major travel advisories",
    "Standard tourist safety measures recommended"
  ],
  "travel_score": 8,
  "recommendation": "Safe to travel. Weather is pleasant. No significant alerts."
}
```

## 🔧 Tech Stack

- **Framework**: Streamlit (Web UI), Python (CLI)
- **LLM**: Groq Cloud API (Llama 3.3 70B Versatile)
- **Weather API**: OpenWeatherMap (with retry logic)
- **News API**: NewsData.io with RSS fallback (with retry logic)
- **Validation**: Pydantic schemas for type safety
- **Date Parsing**: dateparser for natural language dates
- **Retry Logic**: tenacity for exponential backoff
- **Dependencies**: See `requirements.txt`

## 📝 Assignment Requirements Met

✅ **2 External APIs**: OpenWeatherMap + NewsData.io  
✅ **3 AI Agents**: Planner + Executor + Verifier  
✅ **JSON Output**: Pydantic-validated structured recommendations  
✅ **Single Command Execution**: `streamlit run app.py`  
✅ **Error Handling**: Exponential backoff retry + RSS fallback  
✅ **Documentation**: Comprehensive README + code comments  
✅ **Production Features**: Type safety, robust date parsing, fault tolerance

## 🧪 Example Prompts to Test

Try these queries to test the system:

1. **Basic Weather Query**
   ```
   What's the weather in London tomorrow?
   ```

2. **Multi-City Travel Safety**
   ```
   Is it safe to travel to Iran from Delhi on Feb 10? I want weather for both locations
   ```

3. **Future Travel Planning**
   ```
   Is it safe to travel to Paris next week?
   ```

4. **Specific Destination Focus**
   ```
   Any travel alerts or weather updates for Mumbai?
   ```

5. **General Safety Check**
   ```
   Should I travel to Tokyo tomorrow? What's the current situation?
   ```

**Expected Output**: JSON with destination, date, weather conditions, travel alerts, safety score (0-10), and AI recommendation.

## ⚠️ Known Limitations & Tradeoffs

### Limitations

1. **Free Tier API Rate Limits**
   - OpenWeatherMap: 60 calls/minute
   - NewsData.io: 200 requests/day on free tier
   - Groq: Rate limited but generous free tier
   - *Mitigation*: RSS fallback for news when API limits hit

2. **Weather Data Scope**
   - Only provides current weather, not multi-day forecasts
   - City-level granularity (not specific neighborhoods)
   - *Tradeoff*: Simpler, faster queries vs detailed forecasts

3. **News Relevance**
   - News API may return general news, not always travel-specific
   - Depends on keyword matching quality
   - *Mitigation*: Verifier Agent filters and summarizes relevant info

4. **LLM Consistency**
   - Groq model may occasionally return non-JSON text
   - Requires prompt engineering for structured outputs
   - *Mitigation*: JSON parsing with fallback error messages

5. **Date Handling**
   - "Next week" requires manual date interpretation by LLM
   - May not always parse complex date expressions
   - *Tradeoff*: Natural language flexibility vs precision

### Design Tradeoffs

| Choice | Benefit | Tradeoff |
|--------|---------|----------|
| **Groq API** | Fastest inference, generous free tier | Smaller context window than GPT-4 |
| **Streamlit over React** | Rapid development, Python-native | Less customizable UI |
| **3-Agent Pattern** | Clear separation of concerns | More API calls, slightly slower |
| **RSS Fallback** | Reliability when news API fails | Less structured data |
| **JSON Output** | Machine-readable, structured | Less human-friendly for raw output |

## 🐛 Troubleshooting

**Issue: "GROQ_API_KEY not found"**
- Ensure `.env` file exists and contains your API key
- Verify you've activated the virtual environment

**Issue: "Model decommissioned" error**
- Update `GROQ_MODEL_ID` in `.env` to `llama-3.3-70b-versatile`

**Issue: Weather/News API errors**
- Verify API keys are valid and active
- Check rate limits on free tier
- RSS fallback activates automatically for news

## 📄 License

MIT License - Feel free to use for educational purposes.

## 👨‍💻 Author

Prince Kumar Singh
