# AI-Powered Resume Analyzer

An AI-powered resume analysis application built using Python, Streamlit, and Sentence Transformers.

## Features

- PDF resume uploading and text extraction
- Semantic similarity analysis using pretrained transformer embeddings
- Technical skill extraction and matching
- Transferable skill identification
- Education and experience analysis
- Project relevance analysis
- Job title matching
- Interactive candidate-job matching dashboard
- Downloadable analysis reports

## Technologies

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- PyMuPDF
- Plotly

## How It Works

1. Upload a PDF resume.
2. Paste a job description.
3. The application extracts the resume text.
4. A pretrained transformer model generates semantic embeddings.
5. The system compares the resume against job requirements.
6. It analyzes technical skills, education, experience, and project relevance.
7. Results are displayed through an interactive dashboard.

## Installation

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── resume_analyzer.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Future Improvements

- More accurate experience extraction from employment dates
- Context-aware education and qualification matching
- Expanded technical skill recognition
- Improved candidate-job scoring through evaluation datasets
- Support for additional resume formats

## Disclaimer

Matching scores are experimental indicators based on semantic similarity and rule-based analysis. They are not verified hiring decisions or official ATS scores.