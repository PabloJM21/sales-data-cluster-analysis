# Sales Data ETL Pipeline

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline designed to extract sales data from a specified API, transform the data for analysis, and load it into a MySQL database. The pipeline is structured to focus on seasonally adjusted monthly percentage changes across different categories.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Data Structure](#data-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- Extracts seasonally adjusted data from an API.
- Transforms the data to facilitate analysis.
- Loads the processed data into a MySQL database.
- Handles different categories and data types effectively.
- Supports monthly data retrieval for specified years.

## Getting Started
These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites
- Python 3.6 or higher
- MySQL Server
- An API key for data extraction (replace `API_KEY` in the code)
- Required Python packages (listed in requirements.txt)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sales-data-etl.git

