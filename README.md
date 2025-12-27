# Pursite Backend Project

## Project Overview

This is the backend for Pursite, a dynamic platform built with Django and Django Rest Framework. Pursite features a robust product catalog managed by administrators, enabling regular users to create and manage their own sales listings based on these products. It also includes comprehensive user engagement functionalities such as comments, and a secure authentication system using JWT.

## Key Features

- **Product Catalog Management:** Admin-only interface for creating and managing a master list of products, brands, and categories, complete with image uploads.
- **User-Generated Listings (Posts):** Users can create posts to sell existing catalog products, including pricing and captions.
- **Comment System:** A two-level nested comment and reply system for post discussions.
- **Secure Authentication:** JWT (JSON Web Tokens) for user authentication, featuring refresh token rotation and blacklisting for enhanced security.
- **Modular Application Structure:** Clean separation of concerns with dedicated apps for `Product`, `Post`, and `Action`.
- **Comprehensive Logging:** Detailed activity and security logging for traceability and debugging.

## Technologies Used

- **Python:** 3.13+
- **Django:** Web framework
- **Django Rest Framework (DRF):** For building powerful REST APIs
- **Django Simple JWT:** For token-based authentication
- **SQLite3:** Default database (easily configurable for PostgreSQL/MySQL)

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Ensure you have the following installed:
- Python 3.13 or higher
- `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [hhttps://github.com/Pursite/webpage.git](https://github.com/Pursite/webpage.git)
    cd web-site
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    * **Note:** You'll need to create `requirements.txt` first. (We can generate this together if you like!)

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

### Configuration

Create a `.env` file in the project root directory (next to `manage.py`) and add your environment variables.
* **`.env` example:**
    ```
    SECRET_KEY='your_django_secret_key_here'
    DEBUG=True
    # Add any other sensitive settings here
    ```
    Replace `your_django_secret_key_here` with a strong, random string. You can generate one using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.

### Running the Server

Start the Django development server:
```bash
python manage.py runserver