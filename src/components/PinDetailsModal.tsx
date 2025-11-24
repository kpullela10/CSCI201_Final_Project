import type { Pin } from '../types';
import { formatDate, formatRelativeTime } from '../utils/dateFormat';

interface PinDetailsModalProps {
  pin: Pin | null;
  onClose: () => void;
}

export function PinDetailsModal({ pin, onClose }: PinDetailsModalProps) {
  if (!pin) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onClose}>
      <div
        className="bg-white rounded-lg shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-2xl font-bold text-gray-800">Pin Details</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
            >
              ×
            </button>
          </div>

          {pin.image_url && (
            <div className="mb-4">
              <img
                src={pin.image_url}
                alt="Squirrel"
                className="w-full h-64 object-cover rounded-md"
              />
            </div>
          )}

          <div className="space-y-3">
            {pin.description && (
              <div>
                <h3 className="text-sm font-medium text-gray-500 mb-1">Description</h3>
                <p className="text-gray-800">{pin.description}</p>
              </div>
            )}

            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">User</h3>
              <p className="text-gray-800">{pin.username || `User ID: ${pin.userID}`}</p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Time</h3>
              <p className="text-gray-800">{formatDate(pin.created_at)}</p>
              <p className="text-sm text-gray-500 mt-1">{formatRelativeTime(pin.created_at)}</p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Coordinates</h3>
              <p className="text-gray-800">
                Lat: {pin.lat.toFixed(6)}, Lng: {pin.lng.toFixed(6)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

