# Design-and-Development-of-Natural-Language-Interface-for-Agriculture-Infrastructure# 🌾 Agri Assistant – Natural Language Interface for Agriculture Infrastructure

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, AI‑powered agricultural chatbot. Ask about crop cultivation, pest control, fertilizer, market prices, irrigation, or organic farming – using simple natural language. Available as **terminal CLI**, **web widget**, and **Streamlit app** .

![Agri Assistant Demo](docs/screenshot_main.png)
*Replace with your actual screenshot.*

## ✨ Features

- **Crop Guides** – rice, wheat, maize (soil, climate, varieties, yield).
- **Pest & Disease Control** – IPM strategies for stem borer, aphids, rust, blight.
- **Fertilizer Calculator** – NPK recommendation (urea, DAP, MOP) by crop and area.
- **Market Prices** – min/max/avg prices + trend for rice, wheat, maize, cotton.
- **Weather Simulator** – time‑based temperature & humidity.
- **Organic Farming** – panchagavya, neem oil, vermicompost.
- **Irrigation Planner** – drip vs sprinkler vs flood.
- **Quick Buttons** – one‑click access to 12 common topics.
- **Dark Mode UI** – glassmorphism design.

## 🖥️ Demo

![Terminal interface](docs/screenshot_terminal.png)
*Terminal version asking "rice farming tips".*

![Streamlit chat](docs/screenshot_streamlit.png)
*Streamlit app conversation.*

## 📦 Tech Stack

- Python 3.10+
- Streamlit (dashboard)
- HTML / CSS / JavaScript (web version)
- Pandas / NumPy (optional for price data)

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/agri-assistant.git
cd agri-assistant
pip install streamlit
streamlit run app.py
