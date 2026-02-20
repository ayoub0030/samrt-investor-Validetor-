import asyncio
import webbrowser
from flask import Flask, render_template, request, jsonify
from agents import MarketLogicAgent, FinancialAgent, CompetitiveAgent, SynthesizerAgent, MediaAnalysisAgent

app = Flask(__name__)

market_agent = MarketLogicAgent()
financial_agent = FinancialAgent()
competitive_agent = CompetitiveAgent()
synthesizer = SynthesizerAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    idea = data.get('idea', '')
    api_key = data.get('api_key', '')
    
    if not idea or not api_key:
        return jsonify({'error': 'Please enter the investment idea and API key'}), 400
    
    try:
        result = asyncio.run(run_analysis(idea, api_key))
        return jsonify(result)
    except Exception as e:
        import traceback
        error_details = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(f"Analysis error: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500


async def run_analysis(idea: str, api_key: str) -> dict:
    market_task = market_agent.analyze(idea, api_key)
    financial_task = financial_agent.analyze(idea, api_key)
    competitive_task = competitive_agent.analyze(idea, api_key)
    
    market_result, financial_result, competitive_result = await asyncio.gather(
        market_task,
        financial_task,
        competitive_task
    )
    
    final_verdict = await synthesizer.synthesize(
        idea=idea,
        market_analysis=market_result,
        financial_analysis=financial_result,
        competitive_analysis=competitive_result,
        api_key=api_key
    )
    
    return {
        'market_analysis': market_result,
        'financial_analysis': financial_result,
        'competitive_analysis': competitive_result,
        'final_verdict': final_verdict
    }


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(debug=True, use_reloader=False)
