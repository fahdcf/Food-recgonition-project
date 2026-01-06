import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import { Navbar } from './components/Navbar'
import { Toast } from './components/Toast'
import { Landing } from './pages/Landing'
import { Upload } from './pages/Upload'
import { Dashboard } from './pages/Dashboard'
import { AllDishes } from './pages/AllDishes'
import { DishDetail } from './pages/DishDetail'
import './App.css'

function App() {
  return (
    <Router>
      <AppProvider>
        <div className="app">
          <Navbar />
          <Toast />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/dishes" element={<AllDishes />} />
            <Route path="/dishes/:id" element={<DishDetail />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </AppProvider>
    </Router>
  )
}

export default App
