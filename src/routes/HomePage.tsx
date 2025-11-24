import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">Squirrel Spotter USC</h1>
          <p className="text-xl text-gray-600">
            Spot, share, and compete to find the most squirrels around USC!
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Welcome!</h2>
          <p className="text-gray-600 mb-6">
            Join the USC community in spotting and documenting squirrels around campus.
            Drop pins on the map when you see a squirrel, compete on the leaderboard,
            and see real-time updates from other spotters.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {!isAuthenticated ? (
              <>
                <Link
                  to="/login"
                  className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition text-center"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition text-center"
                >
                  Sign Up
                </Link>
              </>
            ) : (
              <Link
                to="/map"
                className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition text-center"
              >
                Go to Map
              </Link>
            )}
            <Link
              to="/leaderboard"
              className="px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition text-center"
            >
              View Leaderboard
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">📍 Drop Pins</h3>
            <p className="text-gray-600">
              Click on the map to mark where you spotted a squirrel. Add photos and descriptions!
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">🏆 Compete</h3>
            <p className="text-gray-600">
              Climb the leaderboard by spotting the most squirrels. Weekly and all-time rankings!
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">⚡ Real-time</h3>
            <p className="text-gray-600">
              See new pins appear in real-time as other users spot squirrels around campus.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

