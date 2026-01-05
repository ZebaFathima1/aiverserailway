# Django Backend API Structure

This document provides a comprehensive overview of the Django backend API structure.

## Project Structure

```
backend/
├── aiverse_api/          # Main Django project
│   ├── settings.py       # Django settings (CORS, REST, JWT)
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # WSGI config
│   └── asgi.py          # ASGI config
├── users/               # User management app
│   ├── models.py        # Custom User model
│   ├── serializers.py   # User serializers
│   ├── views.py         # Auth & user management views
│   ├── urls.py          # Auth endpoints
│   └── admin_urls.py    # Admin user management endpoints
├── events/              # Events management app
│   ├── models.py        # Event, EventImage, EventRegistration
│   ├── serializers.py   # Event serializers
│   ├── views.py         # Event CRUD operations
│   └── urls.py          # Event endpoints
├── payments/            # Payments app
│   ├── models.py        # Payment model
│   ├── serializers.py   # Payment serializers
│   ├── views.py         # Payment management
│   └── urls.py          # Payment endpoints
├── analytics/           # Analytics app
│   ├── models.py        # Activity tracking
│   ├── views.py         # Dashboard analytics
│   └── urls.py          # Analytics endpoints
├── media/               # Uploaded files
├── manage.py
└── requirements.txt
```

## Database Models

### User (users/models.py)
```python
- email (unique, login field)
- username
- full_name
- phone
- college
- profile_image (ImageField)
- is_admin (BooleanField)
- created_at, updated_at
```

### Event (events/models.py)
```python
- title, slug
- description, short_description
- date, end_date
- venue
- registration_fee
- max_participants
- status (upcoming/ongoing/completed/cancelled)
- featured_image
- is_featured
```

### EventImage (events/models.py)
```python
- event (ForeignKey)
- image (ImageField)
- caption
- uploaded_at
```

### EventRegistration (events/models.py)
```python
- user (ForeignKey)
- event (ForeignKey)
- registered_at
- is_active
```

### Payment (payments/models.py)
```python
- user (ForeignKey)
- event (ForeignKey, optional)
- amount
- transaction_id
- payment_screenshot (ImageField)
- status (pending/approved/rejected)
- notes
- submitted_at, processed_at
- processed_by (ForeignKey to User)
```

### Activity (analytics/models.py)
```python
- user (ForeignKey)
- action (CharField)
- activity_type (login/registration/payment/event/other)
- timestamp
```

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /register/` - User registration
- `POST /login/` - User login (JWT)
- `GET /profile/` - Get user profile
- `PATCH /profile/` - Update user profile

### Events (`/api/events/`)
- `GET /` - List all events
- `POST /` - Create event (admin)
- `GET /{slug}/` - Get event details
- `PATCH /{slug}/` - Update event (admin)
- `DELETE /{slug}/` - Delete event (admin)
- `POST /{slug}/add_image/` - Add gallery image (admin)
- `GET /{slug}/registrations/` - Get event registrations

### Payments (`/api/payments/`)
- `GET /` - List payments
- `POST /` - Submit payment
- `GET /{id}/` - Get payment details
- `PATCH /{id}/` - Update payment (admin)
- `DELETE /{id}/` - Delete payment (admin)
- `POST /{id}/approve/` - Approve payment (admin)
- `POST /{id}/reject/` - Reject payment (admin)

### Admin Users (`/api/admin-users/`)
- `GET /` - List all users (admin)
- `GET /{id}/` - Get user details (admin)
- `PATCH /{id}/` - Update user (admin)
- `DELETE /{id}/` - Delete user (admin)
- `POST /{id}/toggle_admin/` - Toggle admin status (admin)

### Analytics (`/api/analytics/`)
- `GET /dashboard/` - Dashboard statistics (admin)

## Authentication

### JWT Authentication
- Uses `djangorestframework-simplejwt`
- Access token lifetime: 1 day
- Refresh token lifetime: 7 days
- Tokens are included in requests via `Authorization: Bearer <token>` header

### Permissions
- **AllowAny**: Registration, login
- **IsAuthenticated**: Profile, payment submission
- **IsAdminUser**: Admin dashboard, user management, event management, payment approval

## CORS Configuration

Allowed origins:
- `http://localhost:8080`
- `http://127.0.0.1:8080`
- `http://localhost:3000` (legacy)
- `http://127.0.0.1:3000` (legacy)

## Media Files

Uploaded files are stored in `backend/media/`:
- `profile_images/` - User profile pictures
- `event_images/` - Event featured images
- `event_gallery/` - Event gallery images
- `payment_screenshots/` - Payment proof screenshots

## Security Best Practices

1. **Change SECRET_KEY in production**
2. **Set DEBUG=False in production**
3. **Use environment variables for sensitive data**
4. **Enable HTTPS in production**
5. **Implement rate limiting for API endpoints**
6. **Add proper file upload validation**
7. **Implement CSRF protection for non-API views**

## Development Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py create_admin

# Run development server
python manage.py runserver

# Create admin user (custom command)
python manage.py create_admin
```
