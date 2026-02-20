# 🔮 Smart Investment Oracle AI

> **Watch the complete project explanation and step-by-step build tutorial on YouTube:**
> 
> [![Project Tutorial on YouTube](https://img.youtube.com/vi/S5shoHtZMAk/maxresdefault.jpg)](https://youtu.be/S5shoHtZMAk)
> 
> **[Click here to watch the video now](https://youtu.be/S5shoHtZMAk)** 🚀

## 📋 Project Overview

This project is an AI-powered "Smart Investment Committee" system designed to analyze investment ideas and startup projects from multiple strategic perspectives. The system simulates the role of three specialized analysts plus a final decision maker to provide comprehensive reports that help entrepreneurs and investors make informed decisions.

## 🌟 Key Features

The system uses a **Diamond Structure** in prompt engineering, distributing tasks and then aggregating them:

1. **Market Logic Analysis Agent**:
   - Studies market size and growth
   - Analyzes supply and demand dynamics
   - Identifies market gaps and consumer behavior

2. **Financial Sustainability Agent**:
   - Analyzes unit economics
   - Studies cost and revenue structure
   - Estimates break-even points and funding requirements

3. **Competitive Analysis Agent**:
   - Evaluates barriers to entry
   - Analyzes competitive moats
   - Studies competitive risks and copycat potential

4. **Synthesizer Decision Agent**:
   - Aggregates the three reports
   - Balances different perspectives
   - Issues final verdict (Invest, Caution, Reject) with strategic advice

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Flask**: Web framework for backend
- **OpenAI API**: AI engine for the agents
- **Tailwind CSS**: Modern and attractive UI design
- **Asyncio**: Parallel processing management for agents

## 🚀 Installation and Running

Follow these steps to run the project on your machine:

### 1. Prerequisites
Make sure you have [Python](https://www.python.org/) installed on your machine.

### 2. Clone Repository
Download the project to your machine:
```bash
git clone <repository-url>
cd smart-investor
```

### 3. Install Required Libraries
Install the requirements listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask server:
```bash
python app.py
```

The browser will automatically open `http://localhost:5000`.

## 💡 How to Use

1. After running the application, you'll see the "Oracle AI" interface.
2. Enter your **OpenAI API key** in the designated field.
3. Write your **investment idea** in detail in the text box.
4. Click the **INITIALIZE ANALYSIS** button.
5. Enjoy watching the deep analysis from three perspectives, then the final decision!

## 📂 Project Structure

- `app.py`: Main application file and endpoints
- `agents/`: Contains AI agent code:
  - `base.py`: Base agent class
  - `market_logic.py`: Market agent
  - `financial.py`: Financial agent
  - `competitive.py`: Competition agent
  - `synthesizer.py`: Final decision agent
- `templates/`: HTML files
- `static/`: CSS and JavaScript files

---

**This project was developed as part of an educational series about building AI agent systems. Don't forget to [watch the video](https://youtu.be/S5shoHtZMAk) to understand the code in depth!** ❤️
