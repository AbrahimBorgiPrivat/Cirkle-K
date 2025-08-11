# Circle K — Loyalty Simulation and Transaction Modeling

This Python project simulates customer behavior and loyalty transactions for Circle K.  
It models segmentation, transaction flows, cashier logic, campaign tracking, and loads the results into a PostgreSQL environment using modular and testable components.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Poetry** for dependency management
- A valid `.env` file for database credentials

---

### 📦 Installation

1. **Clone the repository**
   ```sh
   git clone <repository-url>
   cd source/code
   ```

2. **Install Poetry**
   ```sh
   pip install poetry
   ```

3. **Set up virtualenv inside the project folder**
   ```sh
   poetry config virtualenvs.in-project true
   ```

4. **Install dependencies**
   ```sh
   poetry install
   ```

5. **Create a `.env` file**
   ```ini
   DB_HOST=<your-database-host>
   DB_NAME=<your-database-name>
   DB_PORT=<your-database-port>
   DB_USERNAME=<your-database-username>
   DB_PASSWORD=<your-database-password>
   ```

6. **Activate the virtual environment**
   ```sh
   poetry shell
   ```

7. **Run a test script**
   ```sh
   poetry run python test_poetry_script.py
   ```

---

## 🧱 Project Structure

```plaintext
source/code/
├── classes/          # Shared logic and DB classes
├── scripts/          # Orchestration and ETL control scripts
│   ├── api/          # External API connectors (e.g. CVR)
│   ├── pipelines/    # Ingestion from DAGI, DAR, etc.
│   ├── simulations/  # Data generation (customers, cashiers, transactions)
│   └── upserts/      # Upsert logic for PostgreSQL targets
├── utils/            # Helpers for env loading, orchestrator, time logic
├── .env              # Local config (not committed)
├── pyproject.toml    # Poetry dependencies and metadata
├── README.md         # This file
```

---

## 🔁 Running the Simulation Pipeline

Main simulation pipeline is executed via:

```bash
poetry run python scripts/run_simulation_pipeline.py
```

Inside this file, modules are defined like:

```python
run_modules = [
    ("Simulate Products", upserts.simu_products),
    ("Simulate Campaign Groups", upserts.simu_campaignsgroups),
    ("Upsert Stations", upserts.stations),
    ("Simulate Cashiers", upserts.simu_cashier),
    ("Simulate Segmentation Groups", upserts.simu_segmentationgroups),
    ("Simulate Customers & Cards", upserts.simu_customer_cards),
    ("Simulate Transactions", upserts.simu_transactions)
]
```

Each module is independent and fault-tolerant.

---

## 🧪 Debugging

To enter the shell and run scripts manually:

```bash
poetry shell
python scripts/run_simulation_pipeline.py
```

---

## 🛠 Troubleshooting

- **`ModuleNotFoundError`**  
  Ensure you're using Poetry’s environment:
  ```sh
  poetry shell
  ```

- **Dependencies not installing**  
  Try:
  ```sh
  poetry lock --no-update
  poetry install
  ```

---

## 🤝 Contributing

1. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```

2. Make changes and commit:
   ```sh
   git commit -m "Add feature"
   ```

3. Push to GitHub:
   ```sh
   git push origin feature-branch
   ```

4. Open a pull request

---

## 🔒 License

This project is internal and intended only for use in the Circle K data and analytics environment.  
All rights reserved.
