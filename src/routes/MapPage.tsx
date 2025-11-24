import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useWebSocketPins } from '../hooks/useWebSocketPins';
import { MapView } from '../components/MapView';
import { PinForm } from '../components/PinForm';
import { PinDetailsModal } from '../components/PinDetailsModal';
import type { Pin } from '../types';

export function MapPage() {
  const { isAuthenticated } = useAuth();
  const [selectedPin, setSelectedPin] = useState<Pin | null>(null);
  const [showPinForm, setShowPinForm] = useState(false);
  const [pinFormLocation, setPinFormLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [successMessage, setSuccessMessage] = useState('');

  // Show all pins for now (filter removed from UI)
  const { pins, isLoading } = useWebSocketPins('all');

  const handlePinClick = (pin: Pin) => {
    setSelectedPin(pin);
  };

  const handleMapClick = (lat: number, lng: number) => {
    if (!isAuthenticated) {
      // Redirect to login if trying to drop pin without authentication
      window.location.href = '/login';
      return;
    }
    setPinFormLocation({ lat, lng });
    setShowPinForm(true);
  };

  const handlePinCreated = (newPin: Pin) => {
    setShowPinForm(false);
    setPinFormLocation(null);
    setSuccessMessage('Pin created successfully!');
    setTimeout(() => setSuccessMessage(''), 3000);
  };

  const handleCancelPinForm = () => {
    setShowPinForm(false);
    setPinFormLocation(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="h-screen flex flex-col">
        {/* Success message */}
        {successMessage && (
          <div className="bg-green-50 border-l-4 border-green-500 text-green-700 px-4 py-3 mx-4 mt-2 rounded absolute top-20 left-0 right-0 z-30">
            {successMessage}
          </div>
        )}

        {/* Map */}
        <div className="flex-1 relative min-h-0">
          {isLoading && pins.length === 0 ? (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-100 z-0">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2"></div>
                <p className="text-gray-600">Loading pins...</p>
              </div>
            </div>
          ) : null}
          <MapView
            pins={pins}
            onPinClick={handlePinClick}
            onMapClick={handleMapClick}
            canDropPin={isAuthenticated}
          />

          {/* Pin Form Overlay */}
          {showPinForm && pinFormLocation && (
            <>
              <div
                className="absolute inset-0 bg-black bg-opacity-30 z-10"
                onClick={handleCancelPinForm}
              />
              <div className="absolute top-4 left-4 z-20">
                <PinForm
                  lat={pinFormLocation.lat}
                  lng={pinFormLocation.lng}
                  onSuccess={handlePinCreated}
                  onCancel={handleCancelPinForm}
                />
              </div>
            </>
          )}
        </div>
      </div>

      {/* Pin Details Modal */}
      <PinDetailsModal pin={selectedPin} onClose={() => setSelectedPin(null)} />
    </div>
  );
}

