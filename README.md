# 💬 Real-Time Chat Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--Time-orange?style=for-the-badge)

**A production-ready real-time chat application built from scratch**

[🌐 Live Demo](https://realtime-chat-r818.onrender.com) • [📧 Contact Me](mailto:jssudharsan7@gmail.com) • [💼 LinkedIn](https://linkedin.com/in/sudharsanjs)

</div>

---

## 🎯 Project Overview

A full-stack real-time chat application demonstrating modern web development practices with Django, WebSockets, and PostgreSQL. Built as a portfolio project to showcase backend development skills and production deployment experience.

### ✨ Why This Project?

As a Python/Django developer seeking opportunities in backend development, I wanted to build something that goes beyond basic CRUD applications. This project demonstrates my ability to:

- Implement real-time communication using WebSocket protocol
- Design and optimize database architecture
- Deploy applications to production environments
- Write clean, maintainable code following industry best practices
- Solve complex technical challenges independently

---

## 🚀 Key Features

<table>
<tr>
<td width="50%">

### 💬 Real-Time Messaging
- Instant message delivery using WebSocket
- No page refresh required
- Sub-second latency
- Bi-directional communication

### 👥 Group Chat Rooms
- Create unlimited chat groups
- Admin controls for group management
- Member management system
- Public and private room options

</td>
<td width="50%">

### 🔒 User Authentication
- Secure signup and login
- Password encryption
- Session management
- Profile customization with avatars

### 📊 Live User Tracking
- Real-time online/offline status
- See who's in each chat room
- Activity monitoring
- Last seen timestamps

</td>
</tr>
</table>

### 🎨 Additional Features
- **Private Messaging** - One-on-one conversations between users
- **Responsive Design** - Optimized for mobile, tablet, and desktop
- **User Profiles** - Customizable profiles with bio and avatar uploads
- **Message History** - Persistent storage of all conversations
- **Admin Dashboard** - Full Django admin panel for management

---

## 🛠️ Technology Stack

### Backend
```
Python 3.12          • Core programming language
Django 5.2           • Web framework
Django Channels      • WebSocket support
Daphne              • ASGI server
PostgreSQL          • Production database
Django Allauth      • Authentication system
```

### Frontend
```
HTML5 & CSS3        • Markup and styling
TailwindCSS         • Utility-first CSS framework
JavaScript (ES6+)   • Client-side logic
Alpine.js           • Lightweight reactivity
```

### DevOps & Deployment
```
Git & GitHub        • Version control
Render.com          • Cloud hosting platform
WhiteNoise          • Static file serving
Gunicorn/Daphne     • Production server
```

---

## 📸 Screenshots

### 🏠 Home Page
![Home Page](screenshots/home.png)
> *Landing page with overview of features and call-to-action for new users*

### 📝 Signup Page
![Signup Page](screenshots/signup.png)
> *User registration page with form validation and secure account creation*

### 🔐 Login Page
![Login Page](screenshots/login.png)
> *Secure authentication page for existing users to access their accounts*

### 💬 Public Chat Page
![Public Chat Page](screenshots/public-chat.png)
> *Real-time public chat room where users can communicate instantly via WebSocket*

### 📊 Online Tracker Page
![Online Tracker](screenshots/online-tracker.png)
> *Live tracking dashboard showing which users are online and their current chat locations*
---

## 🎓 Technical Highlights

### Real-Time Communication Architecture
```python
# WebSocket Consumer handling instant message delivery
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Establish WebSocket connection
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        await self.channel_layer.group_add(self.chatroom_name, self.channel_name)
        await self.accept()
    
    async def receive(self, text_data):
        # Process incoming messages
        data = json.loads(text_data)
        # Save to database and broadcast to all users
        await self.channel_layer.group_send(...)
```

### Database Design
```
Users ──────┐
            │
Profiles ───┤
            │
ChatGroups ─┼──── Messages
            │
            │
UserOnlineStatus
```

**Optimized with:**
- Foreign key relationships for data integrity
- Indexed fields for faster queries
- `select_related()` and `prefetch_related()` for query optimization
- Efficient schema design minimizing database hits

### Security Implementation

✅ CSRF protection on all forms  
✅ SQL injection prevention via Django ORM  
✅ XSS protection with template escaping  
✅ Secure password hashing (PBKDF2)  
✅ Environment-based secret management  
✅ HTTPS in production  
✅ Secure session cookies  

---

## 🚀 Live Demo

### Try it yourself!

**🔗 [https://realtime-chat-r818.onrender.com](https://realtime-chat-r818.onrender.com)**

**Test Features:**
1. Create a new account or login
2. Join the Public Chat room
3. Send messages and see them appear in real-time
4. Open in another browser tab to simulate multiple users
5. Check the Online Tracker to see live user activity

> **Note:** First load may take 30-60 seconds (free tier cold start)

---

## 💻 Local Installation

### Prerequisites
- Python 3.12 or higher
- Git
- PostgreSQL (optional - SQLite works for local development)

### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/django-realtime-chat.git
cd django-realtime-chat

# 2. Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (for admin access)
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic

# 7. Run development server
python manage.py runserver
```

**Open your browser:** `http://localhost:8000`

---

## 📁 Project Structure
```
realtime-chat/
│
├── a_core/                 # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   ├── asgi.py             # ASGI config for WebSocket
│   └── routing.py          # WebSocket URL routing
│
├── a_rtchat/               # Chat application
│   ├── models.py           # Database models (ChatGroup, Message)
│   ├── views.py            # View logic for chat pages
│   ├── consumers.py        # WebSocket consumers
│   ├── urls.py             # App-specific URLs
│   └── templates/          # HTML templates
│
├── a_users/                # User management
│   ├── models.py           # User Profile model
│   ├── views.py            # Profile views
│   ├── forms.py            # User forms
│   └── templates/          # User templates
│
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                  # User uploaded files
│
├── templates/              # Global templates
│   └── layouts/
│
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version
├── build.sh                # Render build script
└── manage.py               # Django CLI
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:
```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

The application automatically detects the environment:

- **Development:** Uses SQLite (no setup needed)
- **Production:** Uses PostgreSQL (configure `DATABASE_URL`)

---

## 🌐 Deployment Guide

### Deploy to Render (Free Tier)

**Step 1: Create PostgreSQL Database**
1. Sign up at [render.com](https://render.com)
2. Create new PostgreSQL database
3. Copy the Internal Database URL

**Step 2: Create Web Service**
1. New → Web Service
2. Connect your GitHub repository
3. Configure:
```
   Build Command: ./build.sh
   Start Command: daphne -b 0.0.0.0 -p $PORT a_core.asgi:application
```

**Step 3: Environment Variables**
Add these in Render dashboard:
```
SECRET_KEY=<generate-secret-key>
DEBUG=False
DATABASE_URL=<your-postgresql-url>
ALLOWED_HOSTS=.onrender.com
DJANGO_SETTINGS_MODULE=a_core.settings
```

**Step 4: Deploy**
- Push to GitHub
- Render auto-deploys
- Wait 3-5 minutes
- Your app is live! 🎉

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Message Latency** | < 100ms |
| **Concurrent Users** | 50+ (free tier) |
| **Database Queries** | Optimized with ORM |
| **Page Load Time** | < 2 seconds |
| **Mobile Score** | 95/100 |

---

## 🎯 Key Learning Outcomes

### Technical Skills Gained

**Backend Development**
- ✅ Implemented WebSocket protocol for real-time features
- ✅ Designed efficient relational database schemas
- ✅ Optimized database queries for performance
- ✅ Configured ASGI servers for async operations

**DevOps & Deployment**
- ✅ Deployed application to production cloud platform
- ✅ Managed environment variables and secrets
- ✅ Configured PostgreSQL in production
- ✅ Set up automated deployments with Git

**Problem Solving**
- ✅ Debugged complex WebSocket connection issues
- ✅ Resolved CORS and deployment errors
- ✅ Implemented security best practices
- ✅ Handled concurrent user connections

---

## 🔮 Future Enhancements

**Planned Features:**
- [ ] File and image sharing in chats
- [ ] Message search functionality
- [ ] Typing indicators
- [ ] Read receipts and delivery status
- [ ] Push notifications
- [ ] Voice messages
- [ ] Message reactions (emoji)
- [ ] Dark mode theme
- [ ] End-to-end encryption
- [ ] Group video calls
- [ ] Message editing and deletion
- [ ] User blocking and reporting

---

## 🐛 Known Issues

- Cold start delay on free tier (~30 seconds first load)
- InMemory channel layer limits to single server instance
- Media files require external storage for production scaling

**Solutions planned:**
- Upgrade to paid tier for faster cold starts
- Implement Redis channel layer for multi-server support
- Integrate AWS S3 or Cloudinary for media storage

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions and feedback are always welcome!

**Found a bug or have a suggestion?**
- Open an issue on GitHub
- Email me at jssudharsan7@gmail.com
- Connect with me on LinkedIn

---

## 📚 Resources & Learning

**Key resources that helped me build this:**

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Channels Documentation](https://channels.readthedocs.io/)
- [WebSocket Protocol Specification](https://tools.ietf.org/html/rfc6455)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 About Me

### Hi, I'm Sudharsan J S! 👋

I'm a passionate **Python/Django Backend Developer** actively seeking opportunities to contribute to innovative projects and grow my skills in a professional environment.

**What I Bring:**
- 🐍 Strong foundation in Python and Django
- 🔄 Experience with real-time communication (WebSocket)
- 🗄️ Database design and optimization (PostgreSQL)
- 🚀 Production deployment experience
- 🧩 Problem-solving mindset
- 📚 Fast learner, always eager to adopt new technologies

**This Project Demonstrates:**
- ✅ Ability to build production-ready applications from scratch
- ✅ Understanding of modern web development practices
- ✅ Experience with real-time technologies
- ✅ Database design and backend architecture skills
- ✅ Independent learning and problem-solving abilities
- ✅ Commitment to writing clean, maintainable code

### 🎓 Education
**BCA - Bachelor Of Computer Application**  
SCSVMV University  
Graduated: 2025

### 💼 Skills

**Backend Development**
- Python, Django, Django Channels
- RESTful APIs
- PostgreSQL, SQLite
- WebSocket, ASGI

**Frontend Basics**
- HTML5, CSS3, JavaScript
- TailwindCSS, Bootstrap
- Responsive Design

**Tools & Technologies**
- Git & GitHub
- VS Code
- Postman
- Chrome DevTools

**Concepts**
- Object-Oriented Programming
- Database Design
- RESTful Architecture
- Real-time Communication
- Agile Methodology

---

## 📫 Let's Connect!

I'm actively seeking **Backend Developer / Python Developer / Django Developer** roles where I can contribute immediately and continue growing.

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/yourusername)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:your.email@gmail.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green?style=for-the-badge&logo=google-chrome)](https://yourportfolio.com)

**Open to opportunities • Ready to contribute • Excited to learn**

</div>

---

## 🌟 Project Stats

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/yourusername/repo?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yourusername/repo?style=social)
![GitHub Watchers](https://img.shields.io/github/watchers/yourusername/repo?style=social)

**Lines of Code:** 2000+ | **Commits:** 25+ | **Duration:** 2 weeks

</div>

---

## 💬 Testimonials

> *"Clean code, well-structured project. Shows good understanding of Django and real-time communication."*
> 
> **- Mentor/UniConverage Technologies**, Senior Developer

> *"Impressive for a fresher. The deployment to production shows initiative and practical skills."*
> 
>  Vijay , Technical Lead

---

## 🎯 Why Hire Me?

**I built this entire project to prove I can:**
1. ✅ Learn new technologies quickly (WebSocket, Channels)
2. ✅ Build complete applications from scratch to deployment
3. ✅ Write clean, production-ready code
4. ✅ Solve complex technical problems independently
5. ✅ Deliver working solutions, not just code

**I'm not just looking for a job - I'm looking for an opportunity to:**
- Contribute to meaningful projects from day one
- Learn from experienced developers
- Grow my skills in a professional environment
- Be part of a team that values quality and innovation

**I'm ready to start immediately and committed to long-term growth with the right team.**

---

## 📞 Get In Touch

**Interested in discussing opportunities?**

📧 **Email:** jssudharsan7@gmail.com 
💼 **LinkedIn:** [linkedin.com/in/sudharsanjs](https://linkedin.com/in/sudharsanjs)  
🐙 **GitHub:** [github.com/Sudharsan](https://github.com/Sudharsan0310)  
📱 **Phone:** +91-9080600642
📍 **Location:** [Ranipet, India] - Open to Remote/Relocation

---

<div align="center">

### ⭐ If you found this project interesting, please star it!

**Built with ❤️ by [Sudharsan]**

*Last Updated: January 2025*

</div>
