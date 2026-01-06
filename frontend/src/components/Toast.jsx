import { useAppContext } from '../context/AppContext'
import './Toast.css'

export const Toast = () => {
  const { error, success, clearMessages } = useAppContext()

  if (!error && !success) return null

  return (
    <div className={`toast ${error ? 'error' : 'success'}`}>
      <div className="toast-content">
        <span>{error || success}</span>
        <button className="toast-close" onClick={clearMessages}>×</button>
      </div>
    </div>
  )
}
