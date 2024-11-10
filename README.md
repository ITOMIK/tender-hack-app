# Python Document & Data Similarity Checker

<img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white"> <img src="https://img.shields.io/badge/Gensim-%23F7DF1E.svg?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/requests-%2300add8?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/PyPDF2-grey?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/Camelot-grey?style=for-the-badge&logo=python">

---

This backend application parses PDF files, extracts data, and performs similarity checks against reference values stored in a template `card` object. The project uses a combination of NLP techniques and cosine similarity metrics to validate extracted information, which is then compared to the standardized card reference. Additionally, it communicates with a public API to retrieve supplementary data for comparison.

## Features

- **PDF Parsing**: Extracts structured data from PDF files (e.g., names, addresses, serial numbers) using PyPDF2 and Camelot.
- **Data Similarity Checks**: Utilizes Gensim's Word2Vec embeddings and cosine similarity to compare document content with predefined templates.
- **API Interaction**: Requests data from the specified API endpoint and validates it against the reference template (`card`).
- **CSV Parsing**: Converts parsed data into CSV format for structured storage and analysis.

## Getting Started

### Prerequisites

Ensure you have the following libraries installed:

```bash
pip install gensim numpy requests PyPDF2 camelot-py scikit-learn
