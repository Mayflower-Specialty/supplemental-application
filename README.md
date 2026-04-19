# Mayflower AI Liability Supplemental Application

This repository contains a Python script that generates a professional PDF supplemental application form for AI Liability Insurance coverage using ReportLab.

## Overview

The application form is designed for companies seeking AI-specific insurance coverage modules including:
- AI Directors and Officers Liability (AI-D&O)
- AI Employment Practices Liability (AI-EPL)
- AI Professional Liability (AI-E&O)
- AI DIC Excess

## Features

- **Professional Typography**: Uses custom Google Fonts (Libre Baskerville Regular and Montserrat Light) for the Mayflower Specialty wordmark
- **Comprehensive Coverage**: 12 sections covering AI governance, data governance, operations, incident response, regulatory compliance, and more
- **Brand Consistency**: Incorporates Mayflower Specialty brand colors and logo throughout
- **ReportLab Platypus**: Built using ReportLab's high-level layout engine for precise formatting

## Building the PDF

```bash
python build_mayflower_app.py
```

The generated PDF will be saved to `pdfs/Mayflower_AI_Liability_Supplemental_Application_v4.pdf`

## Requirements

- Python 3.x
- ReportLab library (`pip install reportlab`)

## Logo Fonts

- **MAYFLOWER**: Libre Baskerville Regular (Google Font)
- **SPECIALTY**: Montserrat Light (Google Font)

Font files are located in `assets/` and are automatically registered when the script runs.

## Structure

- `build_mayflower_app.py` - Main PDF generation script
- `assets/` - Logo images and custom font files
- `pdfs/` - Generated PDF output directory
