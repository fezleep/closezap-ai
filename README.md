# CloseZap AI

built by Felipe — evolving into a real AI-powered sales system

---

## Why I built this

leads don’t wait

if you don’t respond fast enough, someone else does

this project started from that simple observation

i wanted to build something that could

respond instantly
handle multiple conversations
and never forget to follow up

---

## What this is

closezap is a lead management system with automation in mind

it is not just a CRUD

the goal is to simulate a real sales flow

you receive leads
track their status
interact over time
and move them through a pipeline

---

## Current state

this project is functional and actively evolving

you can already

create leads
list leads
update their lifecycle
and visualize everything in a simple dashboard

---

## Backend

built with fastapi

provides a clean and simple API

you can

create leads
retrieve leads
close leads

data is stored in sqlite for simplicity
the structure is ready to scale to other databases

---

## Automation

there is a background scheduler running

it was designed to handle follow-ups automatically

this part is still evolving, but the foundation is already there

---

## Frontend

built with react and vite

focused on clarity

you can

see all leads
understand their status
and follow interactions

no unnecessary complexity

---

## Tech stack

backend
fastapi (python)

frontend
react + vite

database
sqlite

planned
openai
whatsapp integration

---

## Running locally

### backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python run.py
```

api

http://localhost:8000

docs

http://localhost:8000/docs

---

### frontend

```bash
cd frontend
npm install
npm run dev
```

app

http://localhost:3000

---

## Example request

creating a lead

```json
POST /api/leads

{
  "name": "Test Lead",
  "phone": "11999999999",
  "interest": "Automation",
  "status": "new",
  "intent": "hot"
}
```

---

## Project structure

backend

app
routes
services
models

frontend

src
components
services

---

## What i am building towards

this is not meant to stay a demo

the idea is to evolve this into something closer to a real product

next steps include

ai-generated responses
lead qualification
whatsapp integration
better user experience
deployment

---

## About me

i’m Felipe

i build systems to learn by doing

this project is part of my focus on

backend architecture
automation
ai-driven products

---

## Final note

this project is not finished

and that is intentional

it is being improved step by step

with the goal of becoming something that could actually be used in a real scenario
