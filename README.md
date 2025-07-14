# Study Pal - Smart Learning Platform 🎓

A modern, AI-powered quiz application that automatically generates MCQ questions from PDF documents and provides comprehensive study tracking.

## ✨ Features

### 🤖 AI Quiz Generation
- **Upload PDF documents** and automatically generate custom MCQ questions
- **Powered by DeepSeek AI** for intelligent question creation
- **Customizable question count** (5-30 questions)
- **Smart content analysis** extracts key concepts from your study materials

### 📚 Study-Friendly Design
- **Focus Mode**: Distraction-free studying environment
- **Dark Mode**: Reduced eye strain for evening study sessions
- **Study Timer**: Track your study sessions with break reminders
- **Adjustable Font Size**: Customize readability for your preferences
- **Progress Tracking**: Visual progress bars and completion indicators

### 📊 Comprehensive Analytics
- **Quiz History**: Track all your quiz attempts with detailed timestamps
- **Performance Statistics**: Average scores, best scores, and improvement trends
- **Detailed Review**: Question-by-question analysis with study tips
- **Progress Visualization**: Charts showing your learning journey

### 🎯 Smart Learning Features
- **Automatic Result Saving**: Never lose your progress
- **Study Break Reminders**: Pomodoro-style break notifications
- **Keyboard Shortcuts**: Quick access to study features
- **RTL Language Support**: Support for Arabic, Kurdish, and other RTL languages

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure AI Features (Optional)
For AI quiz generation from PDFs, you'll need a DeepSeek API key:

1. Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   DEEPSEEK_API_KEY=your_actual_api_key_here
   ```

### 3. Run the Application
```bash
python app.py
```

### 4. Access Study Pal
Open your browser and go to: `http://localhost:5000`

## 📖 How to Use

### AI Quiz Generation
1. **Upload PDF**: Choose a PDF file with your study material (up to 16MB)
2. **Select Questions**: Choose how many questions you want (5-30)
3. **Generate**: Click "Generate Quiz from PDF" and wait 30-60 seconds
4. **Study**: Your custom quiz will be automatically loaded and ready!

### Manual Quiz Upload
1. **Prepare CSV**: Create a CSV file with the format:
   ```csv
   question,A,B,C,D,answer
   "What is 2+2?","2","3","4","5","C"
   ```
2. **Upload**: Use the "Manual Upload - CSV Questions" section
3. **Study**: Take your quiz and track your progress

### Study Features
- **Ctrl+F**: Toggle Focus Mode
- **Ctrl+D**: Toggle Dark Mode
- **Ctrl+T**: Toggle Study Timer
- **Ctrl+=**: Increase Font Size

## 📁 File Structure
```
mcq_quiz/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── questions.csv         # Current quiz questions
├── quiz_history.json    # Your quiz history (auto-generated)
├── .env.example         # API key configuration template
├── static/
│   └── css/
│       └── style.css    # Study-friendly styling
├── templates/
│   ├── base.html        # Base template with study features
│   ├── home.html        # Home page with upload options
│   ├── quiz.html        # Interactive quiz interface
│   ├── result.html      # Results with detailed feedback
│   ├── history.html     # Quiz history and analytics
│   └── quiz_detail.html # Detailed quiz review
└── uploads/             # Temporary PDF storage (auto-generated)
```

## 🔧 Configuration

### DeepSeek API Setup
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account and get your API key
3. Add the key to your `.env` file:
   ```
   DEEPSEEK_API_KEY=sk-your-actual-key-here
   ```

### PDF Requirements
- **Format**: Text-based PDFs (not scanned images)
- **Size**: Up to 16MB
- **Content**: Study materials, textbooks, notes, articles
- **Language**: English content works best

## 📊 CSV Format for Manual Upload
```csv
question,A,B,C,D,answer
"What is the capital of France?","London","Berlin","Paris","Madrid","C"
"Which planet is closest to the Sun?","Venus","Mercury","Earth","Mars","B"
```

**Important**: 
- Answer must be A, B, C, or D (case-insensitive)
- Use quotes around text containing commas
- All columns are required

## 🎨 Study Modes

### Focus Mode (Ctrl+F)
- Removes distractions
- Dark theme with minimal interface
- Perfect for concentration

### Dark Mode (Ctrl+D)
- Reduces eye strain
- Better for evening study sessions
- Maintains all functionality

### Study Timer (Ctrl+T)
- Tracks your study time
- Shows elapsed time
- Break reminders every 25 minutes

## 📱 Responsive Design
Study Pal works perfectly on:
- 💻 Desktop computers
- 📱 Mobile phones
- 📲 Tablets
- 🖥️ All screen sizes

## 🔒 Privacy & Security
- **Local Storage**: All data stays on your device
- **No Cloud Dependencies**: Works offline (except AI generation)
- **Secure API**: DeepSeek API calls are encrypted
- **Private Files**: Your PDFs are processed locally and deleted after use

## 🚀 Advanced Features

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Toggle Focus Mode |
| `Ctrl+D` | Toggle Dark Mode |
| `Ctrl+T` | Toggle Study Timer |
| `Ctrl+=` | Increase Font Size |

### Study Analytics
- **Performance Trends**: Track improvement over time
- **Question Analysis**: See which topics need more study
- **Study Sessions**: Monitor your study habits
- **Grade System**: A+, A, B, C, F grading

## 🔧 Troubleshooting

### AI Generation Not Working
1. Check your API key in `.env` file
2. Ensure PDF contains readable text (not scanned images)
3. Try with a smaller PDF (under 5MB)
4. Check your internet connection

### PDF Upload Issues
1. Ensure file is a valid PDF
2. Check file size (must be under 16MB)
3. Try with a different PDF file
4. Clear browser cache and reload

### Performance Issues
1. Close unnecessary browser tabs
2. Try in incognito/private mode
3. Refresh the page
4. Check system resources

## 🆘 Support

Having issues? Here's how to get help:

1. **Check Console**: Open browser developer tools (F12) and check console for errors
2. **API Issues**: Verify your DeepSeek API key is correct
3. **File Issues**: Ensure PDFs are text-based and under 16MB
4. **Performance**: Try in a fresh browser window

## 🎯 Tips for Best Results

### For AI Quiz Generation:
- Use PDFs with clear, structured content
- Academic papers and textbooks work best
- Ensure text is selectable (not scanned images)
- Keep PDFs under 10MB for faster processing

### For Better Learning:
- Take quizzes multiple times to track improvement
- Review wrong answers carefully
- Use study timer to maintain focus
- Try different question counts for variety

---

**Happy Studying! 📚✨**

Study Pal makes learning more efficient, engaging, and trackable. Whether you're a student, professional, or lifelong learner, our AI-powered platform adapts to your study needs. 