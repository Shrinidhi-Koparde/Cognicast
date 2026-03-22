import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { HiOutlineSparkles, HiOutlineArrowRightOnRectangle, HiOutlineUser } from 'react-icons/hi2';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand">
          <HiOutlineSparkles className="brand-icon" />
          <span className="brand-text">CAstPod</span>
        </Link>

        {user && (
          <div className="navbar-links">
            <Link
              to="/"
              className={`nav-link ${isActive('/') ? 'active' : ''}`}
            >
              Dashboard
            </Link>
            <Link
              to="/upload"
              className={`nav-link ${isActive('/upload') ? 'active' : ''}`}
            >
              New Session
            </Link>
          </div>
        )}

        {user && (
          <div className="navbar-user">
            <div className="user-avatar">
              <HiOutlineUser />
            </div>
            <span className="user-name">{user.name}</span>
            <button className="btn-ghost nav-logout" onClick={handleLogout} title="Logout">
              <HiOutlineArrowRightOnRectangle />
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
