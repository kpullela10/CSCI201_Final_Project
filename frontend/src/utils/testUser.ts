import type { AuthResponse } from '../api/auth';
import type { User } from '../types';

interface WindowWithTestUtils extends Window {
  loginTestUser?: () => void;
  createTestUser?: () => AuthResponse;
}

export function createTestUser(): AuthResponse {
  const testUser: User = {
    userID: 999,
    username: 'testuser',
    email: 'testuser@usc.edu',
  };

  const fakeToken = `test_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  return {
    token: fakeToken,
    user: testUser,
  };
}

export function quickTestLogin(): void {
  try {
    const response = createTestUser();
    localStorage.setItem('authToken', response.token);
    localStorage.setItem('authUser', JSON.stringify(response.user));
    window.location.reload();
  } catch {
    alert('Failed to login test user.');
  }
}

if (typeof window !== 'undefined') {
  const win = window as WindowWithTestUtils;
  win.loginTestUser = quickTestLogin;
  win.createTestUser = createTestUser;
}
