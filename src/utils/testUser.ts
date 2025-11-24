import type { AuthResponse } from '../api/auth';
import type { User } from '../types';

/**
 * Creates a dummy test user for testing purposes (MOCK - no backend required)
 * This creates a fake user in localStorage without making API calls
 */
export function createTestUser(): AuthResponse {
  const testUser: User = {
    userID: 999,
    username: 'testuser',
    email: 'testuser@usc.edu',
  };

  // Generate a fake token
  const fakeToken = 'test_token_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

  const response: AuthResponse = {
    token: fakeToken,
    user: testUser,
  };

  console.log('✅ Test user created (MOCK - no backend required)!', response);
  return response;
}

/**
 * Quick login function for test user (MOCK - no backend required)
 * Call this from browser console: window.loginTestUser()
 */
export function quickTestLogin(): void {
  try {
    const response = createTestUser();
    // Store in localStorage
    localStorage.setItem('authToken', response.token);
    localStorage.setItem('authUser', JSON.stringify(response.user));
    console.log('✅ Test user logged in! Reloading page...');
    // Reload page to update auth state
    window.location.reload();
  } catch (error) {
    console.error('Failed to login test user:', error);
    alert('Failed to login test user. Check console for details.');
  }
}

// Make it available globally for easy access from browser console
if (typeof window !== 'undefined') {
  (window as any).loginTestUser = quickTestLogin;
  (window as any).createTestUser = createTestUser;
}

