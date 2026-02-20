import asyncio
import webbrowser
from flask import Flask, render_template, request, jsonify
from agents import MarketLogicAgent, FinancialAgent, CompetitiveAgent, SynthesizerAgent, MediaAnalysisAgent

app = Flask(__name__)

market_agent = MarketLogicAgent()
financial_agent = FinancialAgent()
competitive_agent = CompetitiveAgent()
media_agent = MediaAnalysisAgent()
synthesizer = SynthesizerAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    idea = data.get('idea', '')
    api_key = data.get('api_key', '')
    
    # Handle file upload
    media_file = request.files.get('media-file')
    media_data = None
    
    if media_file and media_file.filename:
        # Read file content
        if media_file.content_type.startswith('image/'):
            import base64
            media_data = f"Image: {media_file.filename}\nBase64 data: {base64.b64encode(media_file.read()).decode()[:100]}..."
        elif media_file.content_type.startswith('video/'):
            media_data = f"Video: {media_file.filename}\nDuration: Processing...\nFile size: {len(media_file.read())} bytes"
        else:
            media_data = f"File: {media_file.filename}\nType: {media_file.content_type}\nContent preview available"
    
    if not idea or not api_key:
        return jsonify({'error': 'Please enter investment idea and API key'}), 400
    
    try:
        result = asyncio.run(run_analysis(idea, api_key, media_data))
        return jsonify(result)
    except Exception as e:
        import traceback
        error_details = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(f"Analysis error: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500


async def run_analysis(idea: str, api_key: str, media_data: str = None) -> dict:
    market_task = market_agent.analyze(idea, api_key)
    financial_task = financial_agent.analyze(idea, api_key)
    competitive_task = competitive_agent.analyze(idea, api_key)
    
    # Only run media analysis if media data is provided
    if media_data:
        media_task = media_agent.analyze(media_data, api_key)
        market_result, financial_result, competitive_result, media_result = await asyncio.gather(
            market_task,
            financial_task,
            competitive_task,
            media_task
        )
    else:
        market_result, financial_result, competitive_result = await asyncio.gather(
            market_task,
            financial_task,
            competitive_task
        )
        media_result = "No media file provided for analysis."
    
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
        'media_analysis': media_result,
        'final_verdict': final_verdict
    }


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(debug=True, use_reloader=False)
