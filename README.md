# Tractian Integrations Engineering Technical Test

A Python-based integration system that provides bidirectional workorder synchronization between a customer ERP system and Tractian's TracOS platform. The system reads workorders from an inbound folder, processes them through MongoDB, and outputs processed workorders to an outbound folder.

## 🏗️ System Architecture

### Directory Structure

```
tractian_integrations_engineering_technical_test/
├── data/                          # Data directories for file I/O
│   ├── inbound/                   # Input JSON files (customer ERP format)
│   └── outbound/                  # Output JSON files (processed results)
├── src/                           # Main application source code
│   ├── routes/                    # Read/Write operations
│   │   └── costumer_routes.py     # Customer ERP system I/O operations
│   ├── services/                  # Read/Write operations on our system
│   │   └── tracos_service.py      # TracOS MongoDB operations
│   ├── payload_translator/        # Data translation between systems
│   │   └── payload_translator.py  # Format conversion logic
│   ├── schemas/                   # Data validation schemas
│   │   ├── customer_schema.py     # Customer ERP data models
│   │   └── tracos_schema.py       # TracOS data models
│   ├── CONSTS.py                  # Project constants and configuration
│   └── main.py                    # Application entry point
├── tests/                         # Test suite
│   ├── test_costumer.py           # Customer routes tests
│   ├── test_payload_translation.py # Translation logic tests
│   └── test_tracos_service.py     # TracOS service tests
├── docker-compose.yml             # MongoDB container setup
├── pyproject.toml                 # Poetry dependencies and configuration
└── README.md                      # This file
```

### Core Components

- **Routes** (`src/routes/`): Handle Read/Write operations with external systems
  - `costumer_routes.py`: Manages file I/O operations for customer ERP system
- **Services** (`src/services/`): Handle Read/Write operations on our internal system
  - `tracos_service.py`: Manages MongoDB operations for TracOS platform
- **Payload Translator** (`src/payload_translator/`): Translates data between different system formats
  - `payload_translator.py`: Converts between customer ERP and TracOS data formats

## 🚀 Installation

### Prerequisites

- Python 3.11
- Poetry (Python package manager)
- Docker and Docker Compose (for MongoDB)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tractian_integrations_engineering_technical_test
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Start MongoDB using Docker**
   ```bash
   docker-compose up -d
   ```

5. **Set up environment variables** (create a `.env` file in the root directory)
   ```bash
   MONGO_URI=mongodb://localhost:27017/tractian
   DATA_INBOUND_DIR=data/inbound
   DATA_OUTBOUND_DIR=data/outbound
   ```

## 🏃‍♂️ Running the Application

### Execute the main application
```bash
PYTHONPATH=src poetry run python -m src.main
```

This will:
1. Process workorders from the inbound folder
2. Translate them to TracOS format
3. Store them in MongoDB
4. Query and translate back to customer format
5. Save results to the outbound folder

### Run tests
```bash
 PYTHONPATH=src poetry run pytest tests/
```



For specific test files:
```bash
PYTHONPATH=src poetry run pytest tests/test_costumer.py
```

## 📋 System Workflow

### Inbound Processing
1. **Read JSON files** from `data/inbound/` folder (simulating customer API responses)
2. **Validate required fields** (id, status, createdAt, etc.)
3. **Translate payload** from customer format → TracOS format
4. **Insert/update records** in MongoDB collection

### Outbound Processing
1. **Query MongoDB** for workorders with `isSynced = false`
2. **Translate payload** from TracOS format → customer format
3. **Write JSON files** to `data/outbound/` folder
4. **Mark documents** with `isSynced = true` and set `syncedAt` timestamp

### Data Translation Features
- **Date normalization** to UTC ISO 8601 format
- **Enum/status mapping** (e.g., customer "created" → TracOS "NEW")
- **Field mapping** between different system schemas

## 🔧 Configuration

### Environment Variables
- `MONGO_URI`: MongoDB connection string
- `DATA_INBOUND_DIR`: Input folder path for customer workorders
- `DATA_OUTBOUND_DIR`: Output folder path for processed workorders

### Sample Input Format (Customer ERP)
```json
{
  "orderNo": 1,
  "isCanceled": false,
  "isDeleted": false,
  "isDone": false,
  "isOnHold": false,
  "isPending": false,
  "summary": "Example workorder #1",
  "creationDate": "2025-07-08T20:19:57.355919+00:00",
  "lastUpdateDate": "2025-07-08T21:19:57.355919+00:00",
  "deletedDate": null
}
```



## 🧪 Testing

The project includes comprehensive tests covering:
- Customer routes functionality
- Payload translation logic
- TracOS service operations
- End-to-end workflow verification

### Test Structure
- `test_costumer.py`: Tests for customer ERP system interactions
- `test_payload_translation.py`: Tests for data format translation
- `test_tracos_service.py`: Tests for MongoDB operations



## 📄 License

This project is part of the Tractian Integrations Engineering Technical Test.
