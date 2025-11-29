import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { quickTestLogin } from '../utils/testUser';

export function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/map');
  };

  return (
    <nav className="bg-[#990000] shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/map" className="text-xl font-bold text-white hover:text-gray-200">
              Squirrel Spotter USC
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-white">Welcome, {user?.username}</span>
                <Link
                  to="/map"
                  className="px-4 py-2 text-white hover:text-gray-200 hover:bg-[#7a0000] rounded-md transition"
                >
                  Drop Pin
                </Link>
                <Link
                  to="/leaderboard"
                  className="px-4 py-2 text-white hover:text-gray-200 hover:bg-[#7a0000] rounded-md transition"
                >
                  Leaderboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-white text-[#990000] rounded-md hover:bg-gray-100 transition font-semibold"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={quickTestLogin}
                  className="px-4 py-2 text-white hover:text-gray-200 hover:bg-[#7a0000] rounded-md transition border border-white/30"
                  title="Quick login with test user (testuser@usc.edu)"
                >
                  Test Login
                </button>
                <Link
                  to="/login"
                  className="px-4 py-2 text-white hover:text-gray-200 hover:bg-[#7a0000] rounded-md transition"
                >
                  Login / Signup
                </Link>
                <Link
                  to="/leaderboard"
                  className="px-4 py-2 text-white hover:text-gray-200 hover:bg-[#7a0000] rounded-md transition"
                >
                  Leaderboard
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

