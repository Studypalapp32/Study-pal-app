"""
Study Pal - Smart Learning Platform

A Flask-based multiple choice quiz application with AI-powered question generation
from PDF documents using DeepSeek API.

Setup:
1. Install dependencies: pip install -r requirements.txt
2. Set up DeepSeek API (for AI quiz generation):
   - Get API key from: https://platform.deepseek.com/
   - Create .env file in project root
   - Add: DEEPSEEK_API_KEY=your_api_key_here
3. Run the application: python app.py
4. Visit http://localhost:5000

Features:
- AI Quiz Generation: Upload PDF and auto-generate questions
- Manual CSV Upload: Use custom question files
- Quiz History: Track performance and progress
- Study-Friendly Design: Focus mode, dark mode, timers
- Progress Analytics: Performance trends and statistics

CSV Format (for manual upload):
question,A,B,C,D,answer
"What is 2+2?","2","3","4","5","C"

AI Generation Requirements:
- PDF files up to 16MB
- Text-based PDFs (not scanned images)
- DeepSeek API key configured
"""

import csv
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import secrets
import PyPDF2
import requests
from dotenv import load_dotenv
import re
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load environment variables
load_dotenv()

# Global variable to store questions
questions = []

# File to store quiz history
HISTORY_FILE = 'quiz_history.json'

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# PDF upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_questions(csv_file_path):
    """Load questions from CSV file"""
    global questions
    questions = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, 1):
                # Validate required columns
                required_cols = ['question', 'A', 'B', 'C', 'D', 'answer']
                if not all(col in row for col in required_cols):
                    raise ValueError(f"Row {i}: Missing required columns. Expected: {required_cols}")
                
                # Validate answer is A, B, C, or D
                if row['answer'].upper() not in ['A', 'B', 'C', 'D']:
                    raise ValueError(f"Row {i}: Answer must be A, B, C, or D, got '{row['answer']}'")
                
                questions.append({
                    'id': i,
                    'question': row['question'].strip(),
                    'A': row['A'].strip(),
                    'B': row['B'].strip(),
                    'C': row['C'].strip(),
                    'D': row['D'].strip(),
                    'answer': row['answer'].upper().strip()
                })
        
        if not questions:
            raise ValueError("No questions found in CSV file")
            
        return True, f"Successfully loaded {len(questions)} questions"
    
    except FileNotFoundError:
        return False, f"CSV file '{csv_file_path}' not found"
    except ValueError as e:
        return False, f"CSV format error: {str(e)}"
    except Exception as e:
        return False, f"Error reading CSV: {str(e)}"

def grade_quiz(user_answers):
    """Grade the quiz and return results"""
    results = []
    correct_count = 0
    
    for question in questions:
        qid = str(question['id'])
        user_answer = user_answers.get(f'q{qid}', '').upper()
        correct_answer = question['answer']
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct_count += 1
        
        results.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
    
    total_questions = len(questions)
    percentage = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
    
    return {
        'results': results,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'percentage': percentage
    }

def load_quiz_history():
    """Load quiz history from JSON file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []
    except Exception as e:
        print(f"Error loading quiz history: {e}")
        return []

def save_quiz_result(quiz_results):
    """Save quiz result to history"""
    try:
        history = load_quiz_history()
        
        # Create a new entry
        entry = {
            'id': len(history) + 1,
            'timestamp': datetime.now().isoformat(),
            'score': quiz_results['correct_count'],
            'total_questions': quiz_results['total_questions'],
            'percentage': quiz_results['percentage'],
            'time_taken': None,  # Can be enhanced later
            'quiz_title': f"Quiz {len(history) + 1}",
            'results': []
        }
        
        # Store detailed results (without storing all question data)
        for result in quiz_results['results']:
            entry['results'].append({
                'question_id': result['question']['id'],
                'question': result['question']['question'],
                'user_answer': result['user_answer'],
                'correct_answer': result['correct_answer'],
                'is_correct': result['is_correct']
            })
        
        history.append(entry)
        
        # Keep only last 50 attempts to avoid file getting too large
        if len(history) > 50:
            history = history[-50:]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving quiz result: {e}")
        return False

def get_quiz_statistics():
    """Calculate quiz statistics from history"""
    history = load_quiz_history()
    if not history:
        return {
            'total_attempts': 0,
            'average_score': 0,
            'best_score': 0,
            'recent_performance': [],
            'improvement_trend': 'No data'
        }
    
    total_attempts = len(history)
    scores = [entry['percentage'] for entry in history]
    average_score = round(sum(scores) / len(scores), 1)
    best_score = max(scores)
    
    # Get recent performance (last 5 attempts)
    recent_performance = history[-5:] if len(history) >= 5 else history
    
    # Calculate improvement trend
    if len(history) >= 3:
        recent_avg = sum(entry['percentage'] for entry in history[-3:]) / 3
        older_avg = sum(entry['percentage'] for entry in history[-6:-3]) / 3 if len(history) >= 6 else recent_avg
        
        if recent_avg > older_avg + 5:
            improvement_trend = 'Improving'
        elif recent_avg < older_avg - 5:
            improvement_trend = 'Declining'
        else:
            improvement_trend = 'Stable'
    else:
        improvement_trend = 'Insufficient data'
    
    return {
        'total_attempts': total_attempts,
        'average_score': average_score,
        'best_score': best_score,
        'recent_performance': recent_performance,
        'improvement_trend': improvement_trend
    }

def allowed_file(filename):
    """Check if the uploaded file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file"""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
        text = text.strip()
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def generate_questions_with_deepseek(text, num_questions, difficulty_level='', focus_area=''):
    """Generate MCQ questions using DeepSeek API with customizable difficulty and focus"""
    if not DEEPSEEK_API_KEY:
        return None, "DeepSeek API key not configured. Please set DEEPSEEK_API_KEY in your environment variables."
    
    # Truncate text if too long (API has token limits)
    max_chars = 8000  # Conservative limit
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    
    # Build difficulty instruction
    difficulty_instruction = ""
    if difficulty_level:
        difficulty_map = {
            'easy': 'Make questions EASY level - focus on basic concepts, definitions, and direct recall. Questions should test fundamental understanding.',
            'medium': 'Make questions MEDIUM level - include moderate analysis, application of concepts, and some reasoning. Balance recall with understanding.',
            'hard': 'Make questions HARD level - require complex reasoning, critical thinking, analysis, and synthesis of multiple concepts.',
            'expert': 'Make questions EXPERT level - demand advanced synthesis, evaluation, complex problem-solving, and deep analytical thinking.'
        }
        difficulty_instruction = f"\n{difficulty_map.get(difficulty_level, '')}"
    
    # Build focus area instruction
    focus_instruction = ""
    if focus_area:
        focus_instruction = f"\nSpecial Focus: Emphasize questions related to {focus_area}. Prioritize this topic area when selecting concepts for questions."
    
    prompt = f"""
Based on the following text, create exactly {num_questions} multiple-choice questions. Each question should:
1. Be clear and educational
2. Have 4 options (A, B, C, D)  
3. Have exactly one correct answer
4. Test understanding of key concepts from the text{difficulty_instruction}{focus_instruction}

Format your response as a valid CSV with this exact header:
question,A,B,C,D,answer

Make sure each question and option is properly quoted if it contains commas. The answer should be just the letter (A, B, C, or D).

Text to analyze:
{text}

Generate {num_questions} questions now:
"""

    try:
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 2000,
            'temperature': 0.7
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['choices'][0]['message']['content'].strip()
        
        # Extract CSV content (remove any extra text before/after CSV)
        lines = generated_text.split('\n')
        csv_lines = []
        header_found = False
        
        for line in lines:
            line = line.strip()
            if not header_found and line.startswith('question,A,B,C,D,answer'):
                header_found = True
                csv_lines.append(line)
            elif header_found and line and not line.startswith('#') and ',' in line:
                csv_lines.append(line)
        
        if not csv_lines:
            return None, "Could not extract valid CSV format from API response"
        
        csv_content = '\n'.join(csv_lines)
        return csv_content, None
        
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {str(e)}"
    except Exception as e:
        return None, f"Error generating questions: {str(e)}"

def save_generated_questions(csv_content):
    """Save generated questions to questions.csv and load them"""
    try:
        # Backup existing questions
        if os.path.exists('questions.csv'):
            backup_name = f'questions_backup_{int(time.time())}.csv'
            os.rename('questions.csv', backup_name)
        
        # Save new questions
        with open('questions.csv', 'w', encoding='utf-8') as file:
            file.write(csv_content)
        
        # Load the new questions
        success, message = load_questions('questions.csv')
        return success, message
        
    except Exception as e:
        return False, f"Error saving questions: {str(e)}"

@app.route('/')
def home():
    """Home page - show quiz info and start button"""
    quiz_loaded = len(questions) > 0
    statistics = get_quiz_statistics()
    return render_template('home.html', 
                         quiz_loaded=quiz_loaded, 
                         question_count=len(questions),
                         statistics=statistics)

@app.route('/upload', methods=['POST'])
def upload_csv():
    """Handle CSV file upload"""
    if 'csv_file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('home'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('home'))
    
    if not file.filename.lower().endswith('.csv'):
        flash('Please upload a CSV file', 'error')
        return redirect(url_for('home'))
    
    # Save uploaded file temporarily
    temp_path = 'temp_questions.csv'
    try:
        file.save(temp_path)
        success, message = load_questions(temp_path)
        
        if success:
            # Replace the default questions.csv with uploaded file
            if os.path.exists('questions.csv'):
                os.remove('questions.csv')
            os.rename(temp_path, 'questions.csv')
            flash(message, 'success')
        else:
            flash(message, 'error')
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return redirect(url_for('home'))

@app.route('/quiz')
def quiz():
    """Display the quiz questions"""
    if not questions:
        flash('No quiz available. Please upload a CSV file first.', 'error')
        return redirect(url_for('home'))
    
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit_quiz():
    """Process quiz submission and redirect to results"""
    if not questions:
        flash('No quiz available', 'error')
        return redirect(url_for('home'))
    
    # Grade the quiz
    user_answers = request.form.to_dict()
    quiz_results = grade_quiz(user_answers)
    
    # Save to history
    if save_quiz_result(quiz_results):
        flash('Quiz result saved to history!', 'success')
    else:
        flash('Quiz completed but could not save to history.', 'warning')
    
    # Store results in session
    session['quiz_results'] = quiz_results
    
    return redirect(url_for('result'))

@app.route('/result')
def result():
    """Display quiz results"""
    quiz_results = session.get('quiz_results')
    if not quiz_results:
        flash('No quiz results found. Please take the quiz first.', 'warning')
        return redirect(url_for('home'))
    
    return render_template('result.html', results=quiz_results)

@app.route('/clear-results')
def clear_results():
    """Clear quiz results and return to home"""
    session.pop('quiz_results', None)
    return redirect(url_for('home'))

@app.route('/history')
def history():
    """Display quiz history"""
    quiz_history = load_quiz_history()
    statistics = get_quiz_statistics()
    return render_template('history.html', 
                         history=quiz_history[::-1],  # Reverse to show newest first
                         statistics=statistics)

@app.route('/history/<int:quiz_id>')
def view_quiz_result(quiz_id):
    """View detailed results of a specific quiz"""
    quiz_history = load_quiz_history()
    
    # Find the quiz by ID
    quiz_result = None
    for entry in quiz_history:
        if entry['id'] == quiz_id:
            quiz_result = entry
            break
    
    if not quiz_result:
        flash('Quiz result not found', 'error')
        return redirect(url_for('history'))
    
    return render_template('quiz_detail.html', quiz=quiz_result)

@app.route('/clear-history')
def clear_history():
    """Clear all quiz history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        flash('Quiz history cleared successfully', 'success')
    except Exception as e:
        flash(f'Error clearing history: {str(e)}', 'error')
    
    return redirect(url_for('history'))

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and question generation"""
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file selected'})
    
    file = request.files['pdf_file']
    num_questions = request.form.get('num_questions', 10, type=int)
    difficulty_level = request.form.get('difficulty_level', '').strip()
    focus_area = request.form.get('focus_area', '').strip()
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if not file or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Please upload a valid PDF file'})
    
    if num_questions < 1 or num_questions > 50:
        return jsonify({'success': False, 'message': 'Number of questions must be between 1 and 50'})
    
    try:
        # Save uploaded file
        filename = f"uploaded_{int(time.time())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        text = extract_text_from_pdf(filepath)
        if not text:
            os.remove(filepath)  # Clean up
            return jsonify({'success': False, 'message': 'Could not extract text from PDF. Please ensure the PDF contains readable text.'})
        
        # Check if text is substantial enough
        if len(text.strip()) < 100:
            os.remove(filepath)
            return jsonify({'success': False, 'message': 'PDF content too short. Please upload a PDF with more substantial content.'})
        
        # Generate questions using DeepSeek API
        csv_content, error = generate_questions_with_deepseek(text, num_questions, difficulty_level, focus_area)
        if error:
            os.remove(filepath)
            return jsonify({'success': False, 'message': error})
        
        # Save generated questions
        success, message = save_generated_questions(csv_content)
        if not success:
            os.remove(filepath)
            return jsonify({'success': False, 'message': message})
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True, 
            'message': f'Successfully generated {len(questions)} questions from PDF!',
            'questions_count': len(questions)
        })
        
    except Exception as e:
        # Clean up on error
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'success': False, 'message': f'Error processing PDF: {str(e)}'})

@app.route('/generate-status')
def generate_status():
    """Get the current status of question generation"""
    # This route can be used for real-time updates if needed
    return jsonify({
        'questions_loaded': len(questions),
        'status': 'ready'
    })

def initialize_app():
    """Initialize the application with default questions"""
    print("📚 Loading default questions...")
    
    # Load default questions if available
    default_csv = 'questions.csv'
    if os.path.exists(default_csv):
        success, message = load_questions(default_csv)
        if success:
            print(f"✓ {message}")
        else:
            print(f"⚠ Warning: {message}")
    else:
        print(f"⚠ Warning: Default questions file '{default_csv}' not found")

if __name__ == '__main__':
    print("="*50)
    print("🎓 Study Pal - Smart Learning Platform")
    print("="*50)
    print("🚀 Starting application...")
    
    initialize_app()
    
    # Run in development mode
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Initialize for production (Azure App Service)
    initialize_app() 