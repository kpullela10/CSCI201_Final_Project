import type { Pin } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('authToken');
  const headers: HeadersInit = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export async function getWeeklyPins(): Promise<Pin[]> {
  const response = await fetch(`${API_BASE_URL}/api/pins/weekly`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch weekly pins');
  }

  return response.json();
}

export async function getMyPins(): Promise<Pin[]> {
  const response = await fetch(`${API_BASE_URL}/api/pins/my`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch my pins');
  }

  return response.json();
}

export async function createPin(formData: FormData): Promise<Pin> {
  const response = await fetch(`${API_BASE_URL}/api/pins`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData,
  });

  if (!response.ok) {
    if (response.status === 429) {
      throw new Error("You've reached the pin limit (4–5 pins per 30 minutes). Try again later.");
    }
    const error = await response.json().catch(() => ({ message: 'Failed to create pin' }));
    throw new Error(error.message || 'Failed to create pin');
  }

  return response.json();
}

export async function getPinById(pinID: number): Promise<Pin> {
  const response = await fetch(`${API_BASE_URL}/api/pins/${pinID}`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch pin');
  }

  return response.json();
}

