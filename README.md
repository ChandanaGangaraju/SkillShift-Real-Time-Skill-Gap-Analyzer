# SkillShift – Real-Time Skill Gap Analyzer

An AI-powered web application that analyzes skill gaps between resumes and job descriptions, providing personalized recommendations for career growth.

## 🚀 Features

- **Resume Parsing**: Upload PDF/DOCX resumes and extract skills automatically
- **Job Description Analysis**: Paste job descriptions to extract required skills
- **Skill Gap Analysis**: Compare your skills with job requirements
- **AI-Powered Feedback**: Get personalized resume feedback using OpenAI GPT
- **Role-Specific Advice**: Receive targeted advice based on your target role
- **Learning Paths**: Dynamic recommendations for upskilling
- **Visual Analytics**: Skill radar charts and progress bars
- **PDF Reports**: Download comprehensive analysis reports

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: OpenAI GPT API
- **Document Processing**: PyPDF2, python-docx
- **Data Visualization**: Plotly
- **PDF Generation**: ReportLab

## 📋 Prerequisites

- Python 3.7+
- OpenAI API key (for AI features)
- Required Python packages (see requirements.txt)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/skillshift.git
   cd skillshift
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**

   - Get your API key from [OpenAI](https://platform.openai.com/)
   - Set it as an environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```

4. **Run the application**

   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and go to `http://localhost:8501`

## 📖 Usage

1. **Upload Resume**: Upload your resume in PDF or DOCX format
2. **Paste Job Description**: Enter the job description text
3. **Specify Target Role**: Enter your desired job role
4. **Analyze**: Click "Submit Job Description" to start analysis
5. **Review Results**: View skill gaps, AI feedback, and recommendations
6. **Download Report**: Generate and download a PDF report

## 🏗️ Project Structure

```
skillshift/
├── app.py                 # Main Streamlit application
├── resume_parser.py       # Resume parsing functionality
├── job_parser.py          # Job description parsing
├── skill_comparator.py    # Skill comparison logic
├── recommender.py         # AI recommendations and feedback
├── utils.py              # Utility functions and PDF generation
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── assets/              # Static assets (CSS, images)
    └── style.css        # Custom styling (if used)
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for AI features

### Customization

- Modify `utils.py` to add more skills to the skill database
- Update `recommender.py` to customize AI prompts
- Adjust styling in `assets/style.css` (if using custom CSS)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Chandana Gangaraju**

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Streamlit for the web framework
- The open-source community for various Python libraries

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**SkillShift** - Empowering your career with AI-driven insights
