 🎰 Casino Machine Tracker

A full-stack web app to track broken slot machines at a casino and mark them fixed.

 📦 Tech Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Data**: In-memory (soon: file or database)
- **Hosting**: Runs locally

 🛠 Features

- Submit new machine reports with:
  - Machine #
  - Serial #
  - Vendor
  - Date down
  - Technician
- View all out-of-service machines in red cards (horizontal)
- Check a box to mark a machine fixed (card turns green)
- See live status updates instantly

 🚀 How to Run

 Backend (FastAPI)

```bash
cd backend
uvicorn CasinoDatabaseCode:app --reload
