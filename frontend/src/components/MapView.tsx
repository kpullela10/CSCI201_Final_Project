import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { Pin } from '../types';

interface MapViewProps {
  pins: Pin[];
  onPinClick: (pin: Pin) => void;
  onMapClick: (lat: number, lng: number) => void;
  canDropPin: boolean;
}

// Fix for default marker icons in Leaflet with Vite
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// USC campus coordinates
const USC_CENTER: [number, number] = [34.0224, -118.2851];

// Component to handle map clicks
function MapClickHandler({ onMapClick, canDropPin }: { onMapClick: (lat: number, lng: number) => void; canDropPin: boolean }) {
  useMapEvents({
    click: (e) => {
      if (canDropPin) {
        onMapClick(e.latlng.lat, e.latlng.lng);
      }
    },
  });
  return null;
}

export function MapView({ pins, onPinClick, onMapClick, canDropPin }: MapViewProps) {
  return (
    <div className="w-full h-full relative">
      <MapContainer
        center={USC_CENTER}
        zoom={15}
        style={{ height: '100%', width: '100%', minHeight: '600px' }}
        className="z-0"
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapClickHandler onMapClick={onMapClick} canDropPin={canDropPin} />
        
        {pins.map((pin) => (
          <Marker
            key={pin.pinID}
            position={[pin.lat, pin.lng]}
            eventHandlers={{
              click: () => {
                onPinClick(pin);
              },
            }}
          >
            <Popup>
              <div className="text-sm">
                <p className="font-semibold">{pin.description || 'Squirrel Spot'}</p>
                {pin.username && <p className="text-gray-600">by {pin.username}</p>}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
