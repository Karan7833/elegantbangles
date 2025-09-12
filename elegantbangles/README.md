# BangleBar - Elegant Jewelry E-commerce Website

A beautiful and responsive e-commerce website for elegant bangles and jewelry built with Flask and Bootstrap.

## 🌟 Features

### Authentication System
- **User Registration** with email validation
- **User Login** with session management
- **Automatic Login** after successful signup
- **Password Toggle** visibility in forms
- **Session-based** user experience

### Product Features
- **Dynamic Product Search** with real-time filtering
- **Search Highlighting** for better user experience
- **No Results Message** when products not found
- **Responsive Product Grid** with beautiful cards
- **Product Categories** (Bangles, Rings, Necklaces)

### User Interface
- **Responsive Design** for mobile and desktop
- **Bootstrap 5** for modern styling
- **Font Awesome Icons** throughout the interface
- **Personalized Welcome Messages** for logged-in users
- **Dynamic Navbar** based on login status

### Shopping Features
- **Shopping Cart** functionality
- **Product Showcase** with detailed views
- **Checkout Process** with order placement
- **Customer Care** support section

## 🚀 Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework**: Bootstrap 5
- **Database**: SQLite
- **Icons**: Font Awesome 6
- **Security**: Werkzeug password hashing

## 📁 Project Structure

```
elegantbangles/
├── static/
│   ├── banglescript.js      # JavaScript functionality
│   ├── banglestyle.css      # Custom styles
│   └── images/              # Product images
├── templates/
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   ├── signup.html          # Registration page
│   ├── checkout.html        # Checkout page
│   └── other pages...
├── elegantback.py           # Main Flask application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd elegantbangles
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python elegantback.py
   ```

4. **Access the website**
   - Open your browser and go to `http://localhost:5000`

## 🎯 Key Features Explained

### Search Functionality
- **Real-time Search**: Products filter as you type
- **Smart Matching**: Searches product names, prices, and descriptions
- **Visual Feedback**: Highlights matching text in yellow
- **No Results Handling**: Shows friendly message when no products found

### User Authentication
- **Secure Registration**: Email validation and password hashing
- **Session Management**: Automatic login after signup
- **Personalized Experience**: Shows user's first name in navbar
- **Profile Options**: Dropdown menu with user-specific actions

### Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Bootstrap Grid**: Flexible layout system
- **Touch-Friendly**: Easy navigation on mobile devices

## 🔧 Configuration

The application uses the following configuration:
- **Database**: SQLite (users.db)
- **Secret Key**: Set in elegantback.py
- **Port**: 5000 (default Flask port)
- **Debug Mode**: Enabled for development

## 📱 Screenshots

- **Home Page**: Beautiful product showcase with search
- **Login/Signup**: Clean, modern authentication forms
- **Product Search**: Real-time filtering with highlighting
- **User Dashboard**: Personalized experience for logged-in users

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Developer

Created with ❤️ for elegant jewelry lovers.

---

**Note**: This is a development project. For production use, ensure proper security measures and environment configuration.
