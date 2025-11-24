import type { LeaderboardEntry, Pin } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('authToken');
  const headers: HeadersInit = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export interface LeaderboardResponse {
  entries: LeaderboardEntry[];
  totalCount: number;
}

export async function getLeaderboard(
  type: 'weekly' | 'all-time',
  page: number,
  pageSize: number
): Promise<LeaderboardResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/leaderboard?type=${type}&page=${page}&pageSize=${pageSize}`,
    {
      method: 'GET',
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch leaderboard');
  }

  return response.json();
}

export async function getUserPins(userID: number): Promise<Pin[]> {
  const response = await fetch(`${API_BASE_URL}/api/users/${userID}/pins`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user pins');
  }

  return response.json();
}

