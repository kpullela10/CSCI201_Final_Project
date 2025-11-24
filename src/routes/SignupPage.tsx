import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { AuthForm } from '../components/AuthForm';

export function SignupPage() {
  const { signup, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');

  // Redirect if already authenticated
  if (isAuthenticated) {
    navigate('/map');
    return null;
  }

  const handleSignup = async (email: string, username: string, password: string) => {
    setError('');
    try {
      await signup(email, username, password);
      navigate('/map');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed');
      throw err; // Re-throw so AuthForm can handle it
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
              Sign in
            </Link>
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-8">
          <AuthForm mode="signup" onSubmit={handleSignup} error={error} />
        </div>
      </div>
    </div>
  );
}

