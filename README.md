# PaleoGPT: Knowledge Extraction and QA System for Paleontology

PaleoGPT is a specialized deep learning system designed for the automated processing of paleontological literature. It focuses on high-precision knowledge extraction and domain-specific intelligent question-answering.

[Image of an architecture diagram showing a web interface, a FastAPI service for AI, and a Spring Boot service for business logic]

## 🌟 Key Features

* **Automated Literature Extraction**: High-precision extraction of tables, professional entities, and geological images from research papers.
* **Paleontological QA**: Intelligent dialogue services powered by domain-specific language models for term explanation and knowledge inquiry.
* **Human-in-the-loop Correction**: A user-friendly Vue 3 interface for reviewing and manually correcting AI extraction results.

---

## 📂 Project Structure

```text
.
├── dist/                # Frontend production build (Vue 3 + Vite)
├── aiAPI/               # Python Backend (FastAPI)
│   ├── main.py          # Entry point for AI services
│   ├── requirements.txt # Python dependency list
│   └── models/          # [IMPORTANT] Directory for model weights
└── db/                  # Database initialization scripts (.sql)

## 📊 Sample Extraction Results
To help users understand the system's performance without running the full models, we provide pre-generated extraction examples in the `aiAPI/output_data` directory.

These samples include:
* **Table Extraction**: JSON/CSV outputs of paleontological fossil data.
* **Entity Extraction**: Identified taxonomic names and geological periods.
* **Image Extraction**: Cropped and processed fossil images from literature.

🚀 Quick Start Guide
1. Prerequisites
OS: Windows / Linux / macOS

Java: JDK 21

Python: 3.9 or higher

Database: MySQL 8.0 (Recommended)

Web Server: Nginx (for hosting the dist folder)

2. Database Setup
Create a new database in MySQL (e.g., paleogpt_db).

Import the initialization SQL script located in the db/ directory.

Update the application.yml or .properties file in the Java project to match your local database credentials.

3. Model Deployment (Critical)
Note: This repository does not include pre-trained model weights due to file size and licensing.

Download the model weights from [Insert your download link here, e.g., Hugging Face or Cloud Drive].

Place the downloaded files into the aiAPI/models/ directory.

Ensure the file names match the paths defined in the Python source code.

4. Running the Backend
Start the FastAPI Service:
    cd aiAPI
    pip install -r requirements.txt
    python main.py

Start the Java Core Service:
    cd baseAPI/target
    java -jar gpt-demo-1.0-SNAPSHOT.jar

5. API Reference
The frontend interacts with the AI models via the following endpoints:

Table Extraction: /api/project/tableExtra

Entity Extraction: /api/project/entityExtra

Image Extraction: /api/project/imageExtra

🛠 Tech Stack
Frontend: Vue 3 + Element Plus + Vite

Backend: FastAPI (Python) + Spring Boot (Java)

Database: MySQL + Redis

Deep Learning: PyTorch + Transformers

📝 License and Disclaimer
The source code is licensed under the MIT License.

Model Weights: Provided for academic research only. Commercial use is strictly prohibited without prior authorization.

## Citation
If you find this work useful in your research, please cite:
@article{yourname2026paleogpt,
  title={PaleoGPT: Knowledge Extraction and QA System for Paleontology},
  author={Your Name and Others},
  journal={Your Journal/Conference Name},
  year={2026}
}