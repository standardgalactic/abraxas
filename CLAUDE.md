# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Abraxas is a multidisciplinary research repository focused on theoretical frameworks, philosophical concepts, and experimental computational approaches. It combines knowledge curation with AI-powered content processing rather than traditional software development.

## Core Architecture

### Content Processing Pipeline
The repository implements a sophisticated text processing and analysis workflow:

1. **Multi-format text extraction** (`extract-text.py`) - Converts PDF, EPUB, and MHTML files to plain text
2. **AI-powered summarization** (`get-context.sh`) - Uses Ollama with granite3.2:8b model for automated content analysis  
3. **Parallel cloud processing** (`cloud/lambda_function.py`) - AWS Lambda functions for distributed URL processing
4. **Text analysis** (`common-words.py`) - NLTK-based frequency analysis and stopword filtering

### Key Technologies
- **Python** - Primary language for text processing and analysis
- **Ollama** - Local AI model (granite3.2:8b) for content summarization
- **AWS Lambda** - Parallel processing with SQS message queues
- **NLTK** - Natural language processing
- **PyMuPDF, ebooklib, BeautifulSoup4** - Multi-format document parsing

## Essential Commands

### Text Processing
```bash
# Extract text from documents (PDF, EPUB, MHTML)
python extract-text.py file1.pdf file2.epub
python extract-text.py  # Process all supported files in current directory

# Analyze word frequency in text files
python common-words.py <file_path>

# Generate AI summaries of all text files recursively
./get-context.sh
```

### Cloud Infrastructure
```bash
# Deploy AWS Lambda function for parallel processing
cd cloud/
./createlambda.sh
```

## Directory Structure

- **Root level** - Main research documents and core processing scripts
- **Specialized subdirectories**:
  - `cloud/` - AWS Lambda functions and parallel processing infrastructure
  - `NCL/` - Null Convention Logic research and Scratch integration
  - `algorithmic-bias/`, `cosmology/`, `deontology/`, `logic/` etc. - Thematic research collections
  - `fonts/` - Custom typography and alternative scripts
  - `Empathic-Intelligence/` - AI emotion research transcripts

## Dependencies

### Python Requirements
```bash
pip install PyMuPDF ebooklib beautifulsoup4 nltk google-cloud-texttospeech openai boto3
```

### System Requirements
- **Ollama** - For local AI model inference (granite3.2:8b model)
- **AWS CLI** - For Lambda deployment and SQS integration
- **NLTK data** - Download required datasets for text analysis

## Development Workflow

### Processing New Content
1. Add documents (PDF, EPUB, MHTML) to appropriate thematic directories
2. Run `extract-text.py` to convert to plain text
3. Execute `get-context.sh` to generate AI summaries
4. Use `common-words.py` for frequency analysis when needed

### Cloud Processing
The AWS Lambda infrastructure (`cloud/lambda_function.py`) processes URLs in parallel using ThreadPoolExecutor with SQS message queues. Queue URL is hardcoded for `us-east-1` region.

## Research Focus Areas

This repository explores theoretical computing concepts including:
- **Null Convention Logic (NCL)** - Asynchronous computing architectures
- **Active Inference** - Cognitive architecture research  
- **Mereological Space Ontology** - Philosophical frameworks for AI ethics
- **Empathic Intelligence** - Emotion-aware AI systems

## Key Architectural Notes

- No traditional build system - manual script execution required
- Research-oriented rather than production software
- Heavy emphasis on AI-augmented content processing
- Experimental computing concepts integrated with philosophical research
- Content organized thematically rather than by technical function