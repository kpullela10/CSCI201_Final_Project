import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { AuthForm } from '../components/AuthForm';

export function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');

  // Redirect if already authenticated
  if (isAuthenticated) {
    navigate('/map');
    return null;
  }

  const handleLogin = async (email: string, username: string, password: string) => {
    setError('');
    try {
      await login(email, password);
      navigate('/map');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
      throw err; // Re-throw so AuthForm can handle it
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link to="/signup" className="font-medium text-blue-600 hover:text-blue-500">
              create a new account
            </Link>
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-8">
          <AuthForm mode="login" onSubmit={handleLogin} error={error} />
        </div>
      </div>
    </div>
  );
}

