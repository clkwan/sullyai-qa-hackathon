## 🧪 Testing

This project uses **Pytest** for API integration tests with structured logging captured in HTML reports.

### Running Tests Locally

1. Ensure the mock API server is running:
   ```bash
   npm run dev
   npm run seed  # if needed, to reload seed data
2. Activate your Python virtual environment:
   ```bash
   source venv/bin/activate
3. Run the tests:
   ```bash
   pytest
4. Open the HTML report:
   open report.html

```mermaid
flowchart TD
    A[Seed Data - Users, Hotels, Rooms] --> B[API Server - Express + SQLite]
    B --> C[Pytest Test Suite]
    C --> D{Test Logic}
    D -->|Valid Inputs| E[Booking Created via API]
    D -->|Invalid Inputs| F[Errors Logged & Reported]
    C --> G[Logs Captured]
    C --> H[HTML Test Report - report.html]
    H --> I[CI/CD Artifact - GitHub Actions]

