GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --font-inter: 'Inter', sans-serif;
  --bg-color: #F7F8FA;
  --surface-color: #FFFFFF;
  --border-color: #E5E7EB;
  --primary-blue: #2563EB;
}

body {
  font-family: 'Inter', sans-serif !important;
  background-color: #F7F8FA !important;
  color: #111827 !important;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Restrained Minimalist Card Styling */
.sw-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  transition: border-color 0.15s ease;
}
.sw-card:hover {
  border-color: #D1D5DB;
}

/* Primary Button */
.sw-btn-primary {
  background-color: #2563EB !important;
  color: #FFFFFF !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  text-transform: none !important;
  transition: background-color 0.15s ease !important;
}
.sw-btn-primary:hover {
  background-color: #1D4ED8 !important;
}

/* Secondary Button */
.sw-btn-secondary {
  background-color: #F3F4F6 !important;
  color: #374151 !important;
  border: 1px solid #E5E7EB !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  text-transform: none !important;
}
.sw-btn-secondary:hover {
  background-color: #E5E7EB !important;
}

/* Danger Button */
.sw-btn-danger {
  background-color: #DC2626 !important;
  color: #FFFFFF !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  text-transform: none !important;
}
.sw-btn-danger:hover {
  background-color: #B91C1C !important;
}

/* Sidebar Active Link */
.sw-nav-active {
  background-color: #EBF8FF !important;
  border-left: 3px solid #2563EB !important;
  color: #2563EB !important;
  font-weight: 600 !important;
}
.sw-nav-item {
  transition: all 0.15s ease;
  color: #4B5563;
  font-weight: 500;
  border-left: 3px solid transparent;
}
.sw-nav-item:hover {
  background-color: #F9FAFB;
  color: #111827;
}

/* Status Pulse Animation */
@keyframes status-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.status-pulse {
  animation: status-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Clean Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #F7F8FA;
}
::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #9CA3AF;
}
"""
