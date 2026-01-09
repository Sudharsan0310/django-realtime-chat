💬 Real-Time Chat Application

A production-ready, full-stack real-time chat application featuring WebSocket communication, group messaging, and live user tracking. Built with Django and deployed on Render with PostgreSQL database.

🚀 Live Demo

**[Click here to view live application](https://realtime-chat-r818.onrender.com)** 

> **Test Credentials:** Create a new account or use the demo features


🌟 Key Features

- **Real-Time Messaging** - Instant message delivery using WebSocket technology
- **Group Chat Rooms** - Create and manage multiple chat groups with admin controls
- **Private Messaging** - One-on-one direct messaging between users
- **Live User Tracking** - Real-time online/offline status and location tracking
- **Responsive Design** - Fully optimized for mobile, tablet, and desktop devices
- **User Authentication** - Secure login/signup with django-allauth
- **Profile Management** - Customizable user profiles with avatar uploads
- **Admin Dashboard** - Full-featured Django admin for user and group management

🛠️ Technologies Used

### Backend
- **Django 5.2** - Python web framework
- **Django Channels** - WebSocket support for real-time features
- **Daphne** - ASGI server for WebSocket handling
- **PostgreSQL** - Production database
- **Django Allauth** - User authentication and authorization
- **WhiteNoise** - Static file serving

### Frontend
- **HTML5 & CSS3** - Semantic markup and styling
- **JavaScript** - Interactive UI components
- **HTMX** - Lightweight JavaScript framework

### Deployment & DevOps
- **Render.com** - Cloud hosting platform
- **Git & GitHub** - Version control
- **Gunicorn/Daphne** - Production server

💡 Technical Highlights

## Real-Time Communication
Implemented WebSocket protocol using Django Channels for bi-directional communication, enabling instant message delivery and live user status updates without page refreshes.

## Database Design
Designed efficient database schema with proper relationships between Users, Profiles, ChatGroups, and Messages. Implemented optimized queries to minimize database hits.

## Responsive UI/UX
Created mobile-first responsive design using CSS, ensuring seamless experience across all devices. Implemented touch-friendly interfaces and adaptive layouts.

## Production Deployment
Successfully deployed to production environment with:
- PostgreSQL database configuration
- Static file optimization with WhiteNoise
- Environment-based settings management
- Secure HTTPS implementation
- Error handling and logging

## Security Features
- CSRF protection enabled
- Secure session cookies in production
- SQL injection prevention through Django ORM
- XSS protection with Django templates
- Secure password hashing

📦 Installation & Setup

### Prerequisites
- Python 3.12+
- PostgreSQL (optional for local development)
- Git

### Local Development
```bash
# Clone the repository
git clone https://github.com/Sudharsan0310/django-realtime-chat.git
cd django-realtime-chat

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to view the application.

🎯 Key Learnings & Challenges

### Real-Time Communication
Learned WebSocket protocol implementation and handling asynchronous connections. Managed challenges with connection drops and implemented reconnection logic.

### Database Optimization
Implemented efficient database queries using `select_related` and `prefetch_related` to reduce query count and improve performance.

### Deployment
Gained hands-on experience deploying Django applications to production, configuring environment variables, managing static files, and troubleshooting deployment issues.

### Responsive Design
Developed mobile-first approach using CSS, ensuring consistent user experience across different screen sizes and devices.

📈 Future Enhancements

- [ ] Message search functionality
- [ ] File and image sharing in chats
- [ ] Voice/video calling integration
- [ ] Push notifications
- [ ] Message reactions and emojis
- [ ] Read receipts
- [ ] Typing indicators
- [ ] Dark mode theme
- [ ] Message encryption
- [ ] Group video calls

🐛 Known Issues

- Free tier deployment may experience cold starts (initial load delay)
- Media files require external storage for production scalability
- In-memory channel layer limits to single server instance

About ME :

Name : Sudharsan J S

I'm a passionate full-stack developer with expertise in Python and Django. This project demonstrates my ability to build production-ready applications from scratch, including:

- Backend development with Django
- Real-time features with WebSockets
- Database design and optimization
- Responsive frontend development
- Production deployment and DevOps
- Problem-solving and debugging

 Connect With Me

- **LinkedIn:** [linkedin.com/in/yourprofile](https://linkedin.com/in/
sudharsanjs)
- **GitHub:** [github.com/yourusername](https://github.com/Sudharsan0310)
- **Email:** jssudharsan7@gmail.com

🙏 Acknowledgments

- Django documentation for comprehensive guides
- Django Channels for WebSocket implementation
- TailwindCSS for the utility-first CSS framework
- Render for free tier hosting

---

## ⭐ Show Your Support

If you found this project interesting or helpful, please consider giving it a star! ⭐

---

**Built with ❤️ by [Sudharshan ]**
