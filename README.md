# PaleoGPT: Knowledge Extraction and QA System for Paleontology

PaleoGPT: Knowledge Extraction and QA System for Paleontology
PaleoGPT is a specialized deep learning system designed for the automated processing of paleontological literature. It focuses on high-precision knowledge extraction and domain-specific intelligent question-answering.


🌟 Key Features
Automated Literature Extraction: High-precision extraction of tables, professional entities, and labeled fossil images from research papers.

Paleontological QA: Intelligent dialogue services powered by domain-specific language models using Adaptive RAG technology.

Human-in-the-loop Correction: A user-friendly Vue 3 interface for reviewing and manually correcting AI extraction results to ensure high-quality database construction.



## 📂 Project Structure

```text
.
├── dist/                # Frontend production build (Vue 3 + Vite)
├── aiAPI/               # AI Service Backend (FastAPI)
│   ├── main.py          # Entry point for AI services
│   ├── requirements.txt # Python dependency list
│   └── output_data/     # Pre-generated sample extraction results
└── db/                  # Database schema and sample JSON documents

📊 Sample Extraction Results
To facilitate research reproducibility, we provide pre-generated extraction examples in the aiAPI/output_data directory. These samples include:

Table Extraction: JSON/CSV outputs of recovered paleontological fossil data.

Entity Extraction: Identified taxonomic names and geological periods linked with evidence sentences.

Image Extraction: Processed fossil images with automatically calibrated scale bars.

🚀 Quick Start Guide

1. Prerequisites
OS: Windows / Linux / macOS

Java: JDK 21

Python: 3.9 or higher

Database: MongoDB 6.0+ (Essential for multi-modal data storage)

Web Server: Nginx (for hosting the dist folder)

2. Database Setup
Ensure your MongoDB service is running.

Initialize the database using the sample JSON documents in the db/ directory. You can use the mongoimport tool to load these samples.

Update the MongoDB URI in the application.yml (Java) and Python config files to match your local credentials.

3. Model Deployment (Critical)
Note: This repository does not include pre-trained model weights due to file size.

Download the model weights from [Insert Zenodo/Hugging Face link].

Place the downloaded weights into the aiAPI/models/ directory.

4. Running the System
AI Backend: cd aiAPI && pip install -r requirements.txt && python main.py

Java Core: cd baseAPI && java -jar gpt-demo-1.0-SNAPSHOT.jar

🛠 Tech Stack

Frontend: Vue 3 + Element Plus + Vite

Backend: FastAPI (Python) + Spring Boot (Java)

Database: MongoDB (Core storage) + Redis (Caching)

Deep Learning: PyTorch + Transformers (Qwen/Llama series)

📝 License

Code License: This project is licensed under the MIT License.

Data/Weights: Provided for academic research only.

## Citation
If you find this work useful in your research, please cite:
@article{yourname2026paleogpt,
  title={PaleoGPT: Knowledge Extraction and QA System for Paleontology},
  author={Your Name and Others},
  journal={Your Journal/Conference Name},
  year={2026}
}