# Purixia BD - Product Agent Information

## Overview
Purixia BD is a premier e-commerce platform specializing in high-quality gadgets and tech accessories in Bangladesh. The project is built with a modern stack featuring a Next.js frontend and a Django REST Framework (DRF) backend.

## Key Features
- **Modern UI/UX**: Built with React, Next.js, and Tailwind CSS for a fast, responsive, and premium shopping experience.
- **Dynamic Catalog**: Categorized products with detailed specifications, ratings, and stock status.
- **Secure Authentication**: JWT-based authentication for users with registration and profile management.
- **Shopping Cart**: Advanced cart management with real-time updates and persistence.
- **Checkout Flow**: Streamlined ordering process with multiple payment methods (Cash on Delivery, Card, bKash, Nagad) and delivery options.
- **Order Tracking**: Users can view their order history and status.

## Tech Stack
### Frontend
- **Framework**: Next.js 14+ (App Router)
- **State Management**: Zustand
- **Data Fetching**: Tanstack Query (React Query)
- **Forms**: React Hook Form with Zod validation
- **Styling**: Tailwind CSS & Framer Motion
- **Icons**: Lucide React

### Backend
- **Framework**: Django & Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: SimpleJWT
- **Media**: Django File Storage for product images and banners

## Project Structure
- `frontend/`: Next.js application
  - `src/app/`: App router pages
  - `src/components/`: Reusable UI components
  - `src/hooks/`: Custom React hooks for data fetching and logic
  - `src/services/`: API service layers
  - `src/stores/`: Zustand stores for global state
- `backend/`: Django application
  - `apps/`: Modular Django apps (users, catalog, cart, orders, banners)
  - `core/`: Project settings and configurations

## Development
To run the project locally:
1. **Backend**:
   - Navigate to `backend/`
   - Install dependencies: `pip install -r requirements.txt`
   - Run migrations: `python manage.py migrate`
   - Start server: `python manage.py runserver`
2. **Frontend**:
   - Navigate to `frontend/`
   - Install dependencies: `npm install`
   - Start development server: `npm run dev`

---
© 2026 Purixia BD. All rights reserved.
