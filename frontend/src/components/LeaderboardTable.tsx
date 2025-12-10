import type { LeaderboardEntry, Pin } from '../types';
import { useState } from 'react';
import { getUserPins } from '../api/leaderboard';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

function getImageUrl(imageUrl: string | undefined): string | null {
  if (!imageUrl) return null;
  
  // If it's already a full URL (starts with http:// or https://), return as-is
  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl;
  }
  
  // Otherwise, prepend the backend API base URL
  // Remove leading slash if present to avoid double slashes
  const cleanUrl = imageUrl.startsWith('/') ? imageUrl.substring(1) : imageUrl;
  return `${API_BASE_URL}/${cleanUrl}`;
}

interface LeaderboardTableProps {
  entries: LeaderboardEntry[];
  onUserClick?: (userID: number) => void;
}

export function LeaderboardTable({ entries, onUserClick }: LeaderboardTableProps) {
  const [selectedUserPins, setSelectedUserPins] = useState<Pin[] | null>(null);
  const [loadingUserID, setLoadingUserID] = useState<number | null>(null);

  const handleUserClick = async (userID: number) => {
    if (onUserClick) {
      onUserClick(userID);
      return;
    }

    try {
      setLoadingUserID(userID);
      const pins = await getUserPins(userID);
      setSelectedUserPins(pins);
    } catch (error) {
      console.error('Failed to fetch user pins:', error);
      alert('Failed to load user pins');
    } finally {
      setLoadingUserID(null);
    }
  };

  const closeModal = () => {
    setSelectedUserPins(null);
  };

  return (
    <>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rank
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Username
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Weekly Pins
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Total Pins
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {entries.map((entry, index) => (
              <tr
                key={entry.userID}
                className="hover:bg-gray-50 cursor-pointer transition"
                onClick={() => handleUserClick(entry.userID)}
              >
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {index + 1}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {entry.username}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {entry.weekly_pins}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {entry.total_pins}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedUserPins && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={closeModal}>
          <div
            className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-gray-800">
                  Pins by {selectedUserPins[0]?.username || 'User'}
                </h2>
                <button
                  onClick={closeModal}
                  className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
                >
                  ×
                </button>
              </div>

              {selectedUserPins.length === 0 ? (
                <p className="text-gray-500">No pins found for this user.</p>
              ) : (
                <div className="space-y-4">
                  {selectedUserPins.map((pin) => {
                    const fullImageUrl = getImageUrl(pin.image_url);
                    return (
                      <div key={pin.pinID} className="border border-gray-200 rounded-md p-4">
                        {fullImageUrl && (
                          <img
                            src={fullImageUrl}
                            alt="Squirrel"
                            className="w-full h-48 object-cover rounded-md mb-2"
                            onError={(e) => {
                              // Hide image if it fails to load
                              e.currentTarget.style.display = 'none';
                            }}
                          />
                        )}
                      {pin.description && (
                        <p className="text-gray-800 mb-2">{pin.description}</p>
                      )}
                      <p className="text-sm text-gray-500">
                        {new Date(pin.created_at).toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(pin.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {loadingUserID && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6">
            <p className="text-gray-800">Loading pins...</p>
          </div>
        </div>
      )}
    </>
  );
}

