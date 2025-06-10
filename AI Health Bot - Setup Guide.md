# AI Health Bot - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ installed
- Node.js 20+ installed
- pnpm package manager

### Backend Setup (Flask API)

1. **Extract the backend archive**
   ```bash
   unzip health_bot_backend_src.zip
   cd health_bot_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server**
   ```bash
   cd src
   python main.py
   ```
   
   The API will be available at: http://localhost:5000

### Frontend Setup (React App)

1. **Extract the frontend archive**
   ```bash
   unzip health_bot_frontend_src.zip
   cd health_bot_frontend
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Run the development server**
   ```bash
   pnpm run dev --host
   ```
   
   The app will be available at: http://localhost:5173

## 🎯 Features Overview

### ✅ Implemented Features

#### Authentication & User Management
- User registration with health profile setup
- Secure login with JWT tokens
- Password hashing with bcrypt
- User profile management

#### Health Data Tracking
- **Vitals**: Blood pressure, heart rate monitoring
- **Exercise**: Activity and workout logging
- **Nutrition**: Diet and meal tracking
- **Medication**: Medicine schedules and reminders
- **Symptoms**: Mood and symptom tracking
- **Sleep & Hydration**: Sleep patterns and water intake

#### Goals & Progress
- Health goal setting and tracking
- Progress visualization
- BMI calculation and health scores
- Personalized recommendations

#### Notifications & Reminders
- Medication reminders
- Daily motivational messages
- Health goal alerts
- Custom reminder creation

#### Dashboard & Analytics
- Health overview with key metrics
- Recent activity tracking
- Quick action buttons
- Progress charts and visualizations

### 🔧 Technical Architecture

#### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite for development
- **Authentication**: JWT tokens with bcrypt hashing
- **API**: RESTful endpoints with CORS support
- **Security**: Input validation and sanitization

#### Frontend (React)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with shadcn/ui components
- **Icons**: Lucide React icons
- **State Management**: React hooks and context
- **Responsive**: Mobile-first design

#### Database Schema
- **Users**: Authentication and profile data
- **Health Records**: Comprehensive health tracking
- **Goals**: Goal setting and progress tracking
- **Notifications**: Reminders and alerts system

## 📱 User Interface

### Pages & Components
1. **Login/Register**: Secure authentication with health profile setup
2. **Dashboard**: Health overview with key metrics and quick actions
3. **Health Tracking**: Tabbed interface for different health categories
4. **Goals**: Goal setting and progress tracking
5. **Notifications**: Reminder and alert management
6. **Profile**: User and health profile management

### Design Features
- Clean, medical-grade interface
- Responsive design for all devices
- Intuitive navigation with clear visual hierarchy
- Accessibility-focused components
- Professional color scheme with health-themed icons

## 🔐 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- CORS configuration for secure API access
- Input validation and sanitization
- Secure session management

## 🚀 Deployment Options

### Local Development
- Backend: `python src/main.py` (Port 5000)
- Frontend: `pnpm run dev --host` (Port 5173)

### Production Deployment
- Backend: Use gunicorn or similar WSGI server
- Frontend: Build with `pnpm run build` and serve static files
- Database: Migrate to PostgreSQL for production
- Environment: Configure environment variables for security

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Health Records
- `GET /api/health/records` - Get user's health records
- `POST /api/health/records` - Add new health record
- `PUT /api/health/records/:id` - Update health record
- `DELETE /api/health/records/:id` - Delete health record

### Goals
- `GET /api/goals` - Get user's goals
- `POST /api/goals` - Create new goal
- `PUT /api/goals/:id` - Update goal
- `DELETE /api/goals/:id` - Delete goal

### Notifications
- `GET /api/notifications` - Get user's notifications
- `POST /api/notifications` - Create notification
- `PUT /api/notifications/:id` - Update notification
- `DELETE /api/notifications/:id` - Delete notification

## 🎨 Customization

### Adding New Health Categories
1. Update the database models in `src/models/user.py`
2. Add new API endpoints in `src/routes/health.py`
3. Create new UI components in the frontend
4. Update the health tracking tabs

### Styling Customization
- Modify `tailwind.config.js` for theme changes
- Update component styles in `src/components/ui/`
- Customize colors and typography in `src/index.css`

## 🐛 Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in configuration files
2. **Database errors**: Ensure SQLite file permissions
3. **CORS issues**: Check backend CORS configuration
4. **Package installation**: Use correct Node.js and Python versions

### Development Tips
- Use browser developer tools for debugging
- Check backend logs for API errors
- Ensure both servers are running simultaneously
- Test API endpoints with tools like Postman

## 📈 Future Enhancements

### Planned Features
- Data visualization with charts and graphs
- Integration with wearable devices
- AI-powered health insights and recommendations
- Social features for health communities
- Export data functionality
- Mobile app development
- Telemedicine integration

### Technical Improvements
- Real-time notifications with WebSockets
- Advanced analytics and reporting
- Machine learning for personalized recommendations
- Integration with external health APIs
- Enhanced security with OAuth2
- Performance optimization and caching

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the API documentation
3. Examine the source code comments
4. Test with the provided sample data

The AI Health Bot is designed to be a comprehensive health tracking solution with room for extensive customization and enhancement based on specific needs.

