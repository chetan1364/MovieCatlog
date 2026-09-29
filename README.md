# Movie Catalog Project

A comprehensive, full-stack Movie Catalog web application designed to browse, search, and manage a collection of movies from different film industries. This project was built to practice relational database structures, RESTful API design, and authentication concepts.

## 🚀 Technologies Used

### Backend
- **Language**: PHP 8+
- **Framework**: Laravel 11.x
- **Database**: SQLite (Development)
- **ORM**: Eloquent ORM for interacting with database models and establishing relationships.

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Architecture**: Vanilla JavaScript with AJAX/Fetch API for dynamic client-side rendering.
- **Styling**: Custom CSS (Vanilla)

## 🏗️ Implementation Details

### Architecture & Routing
- The frontend consists of static HTML pages (`index.html`, `movie.html`, `admin.html`) located in the `public/` directory.
- Laravel's `routes/web.php` serves these static files and handles basic HTTP Authentication for the `/admin` route.
- The application uses Laravel's API routes (`routes/api.php` if applicable or controllers) to deliver JSON data to the frontend JavaScript.

### Database Design
The relational database utilizes several interconnected tables managed via Laravel Migrations:
- **Movies**: Stores core movie details (title, synopsis, release year, duration, poster).
- **Directors**: One-to-Many relationship with Movies.
- **Actors**: Many-to-Many relationship with Movies (via `movie_actors` pivot table).
- **Genres**: Many-to-Many relationship with Movies (via `movie_genres` pivot table).
- **Ratings**: One-to-Many relationship with Movies.

### Features
- **Catalog Browsing**: Users can view an extensive list of 30+ pre-seeded movies spanning multiple industries (Hollywood, Tollywood, Bollywood, Kollywood, Sandalwood).
- **Advanced Filtering & Search**: Client-side filtering by genre, release year, title, or cast/director name.
- **Admin Panel**: A secure dashboard protected by HTTP Basic Authentication, prompting for a username and password before granting access.

## ⚙️ Setup & Installation

1. **Clone the repository** (if applicable).
2. **Install PHP Dependencies**:
   ```bash
   composer install
   ```
3. **Environment Setup**:
   Copy the example `.env` file and generate an application key:
   ```bash
   cp .env.example .env
   php artisan key:generate
   ```
4. **Database Setup**:
   Run the database migrations and seed the initial 30+ movies:
   ```bash
   php artisan migrate:fresh --seed
   ```
5. **Run the Application**:
   Start the Laravel local development server:
   ```bash
   php artisan serve
   ```
   *The application will be accessible at http://127.0.0.1:8000.*

## 🔒 Security
- **Admin Access**: Navigating to the Admin page prompts for secure login credentials (`admin` / `password`) implemented seamlessly through Laravel's HTTP request verification.
