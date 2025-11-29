export interface User {
  userID: number;
  username: string;
  email: string;
  // password is never stored in frontend state, only sent in auth requests
}

export interface Pin {
  pinID: number;
  userID: number;
  lat: number;
  lng: number;
  description?: string;
  created_at: string; // ISO timestamp
  image_url?: string;
  username?: string; // optional: populated by backend for display
}

export interface LeaderboardEntry {
  userID: number;
  username: string;
  total_pins: number;
  weekly_pins: number;
}

