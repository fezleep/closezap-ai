# CloseZap AI - Frontend

React + Vite + TailwindCSS dashboard for managing leads.

## Features

- **Leads Dashboard**: View all leads with name, phone, status, and last message
- **Status Management**: Update lead status with a dropdown (New, Contacted, Qualified, Converted, Lost)
- **Real-time Stats**: Overview cards showing lead counts by status
- **API Integration**: Connects to backend via GET /leads and PATCH /leads/:id
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean SaaS-style interface with TailwindCSS

## Prerequisites

- Node.js 18+ installed
- Backend API running at `http://localhost:8080` (configurable in `vite.config.js`)

## Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## API Configuration

The frontend proxies API requests to the backend. Update the proxy in `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8080', // Change to your backend URL
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /leads | Get all leads |
| PATCH | /leads/:id | Update lead status |

### Expected Lead Object

```json
{
  "id": "string",
  "name": "string",
  "phone": "string",
  "email": "string (optional)",
  "status": "new | contacted | qualified | converted | lost",
  "lastMessage": "string",
  "lastContactAt": "ISO 8601 date string"
}
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx       # Main dashboard page
│   │   ├── LeadsTable.jsx      # Leads table component
│   │   └── StatusDropdown.jsx  # Status update dropdown
│   ├── hooks/
│   │   └── useLeads.js         # Custom hook for leads data
│   ├── services/
│   │   └── leads.js            # API service layer
│   ├── index.css               # Global styles + Tailwind
│   └── main.jsx                # Entry point
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Production Build

```bash
# Build optimized production bundle
npm run build

# Preview the build locally
npm run preview
```

The build output will be in the `dist/` directory.
