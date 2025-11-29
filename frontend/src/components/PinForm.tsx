import { useState, FormEvent, ChangeEvent } from 'react';
import { createPin } from '../api/pins';
import type { Pin } from '../types';

interface PinFormProps {
  lat: number;
  lng: number;
  onSuccess: (pin: Pin) => void;
  onCancel: () => void;
}

// Default squirrel images - verified squirrel photos from Pixabay (free stock photos)
const DEFAULT_IMAGES = [
  { 
    id: 'squirrel1', 
    url: 'https://images.pexels.com/photos/109009/squirrel-grey-brown-fur-109009.jpeg?cs=srgb&dl=pexels-pixabay-109009.jpg&fm=jpg', 
    label: 'Gray Squirrel' 
  },
  { 
    id: 'squirrel2', 
    url: 'https://images.unsplash.com/photo-1617397410847-bf7edff4663d?q=80&w=3087&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 
    label: 'Red Squirrel' 
  },
  { 
    id: 'squirrel3', 
    url: 'https://images.unsplash.com/photo-1555281614-8d58d2611325?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 
    label: 'Tree Squirrel' 
  },
  { 
    id: 'squirrel4', 
    url: 'https://images.unsplash.com/photo-1618794810354-0cb994333dd5?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 
    label: 'Cute Squirrel' 
  },
  { 
    id: 'squirrel5', 
    url: 'https://images.unsplash.com/photo-1525419649932-37d78bfe21a7?q=80&w=2090&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 
    label: 'Squirrel Eating' 
  },
  { 
    id: 'squirrel6', 
    url: 'https://images.unsplash.com/photo-1661536974630-ba1964202932?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 
    label: 'Squirrel on Branch' 
  },
];

export function PinForm({ lat, lng, onSuccess, onCancel }: PinFormProps) {
  const [description, setDescription] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [selectedDefaultImage, setSelectedDefaultImage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
      setSelectedDefaultImage(null); // Clear default selection when file is selected
    }
  };

  const handleDefaultImageSelect = (imageUrl: string) => {
    setSelectedDefaultImage(imageUrl);
    setImageFile(null); // Clear file selection when default is selected
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      setIsSubmitting(true);
      const formData = new FormData();
      formData.append('lat', lat.toString());
      formData.append('lng', lng.toString());
      formData.append('description', description);
      
      // If a file is uploaded, use that; otherwise use default image URL if selected
      if (imageFile) {
        formData.append('image', imageFile);
      } else if (selectedDefaultImage) {
        formData.append('image_url', selectedDefaultImage);
      }

      const newPin = await createPin(formData);
      onSuccess(newPin);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create pin');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full">
      <h2 className="text-xl font-bold mb-4">Drop a Pin</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Location
          </label>
          <div className="text-sm text-gray-600">
            Lat: {lat.toFixed(6)}, Lng: {lng.toFixed(6)}
          </div>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows={3}
            placeholder="Describe the squirrel you spotted..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Image (optional)
          </label>
          
          {/* Default Images Selection */}
          <div className="mb-4">
            <p className="text-xs text-gray-500 mb-2">Choose a default image:</p>
            <div className="grid grid-cols-3 gap-2">
              {DEFAULT_IMAGES.map((img) => (
                <button
                  key={img.id}
                  type="button"
                  onClick={() => handleDefaultImageSelect(img.url)}
                  className={`relative aspect-square rounded-md overflow-hidden border-2 transition ${
                    selectedDefaultImage === img.url
                      ? 'border-blue-500 ring-2 ring-blue-300'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <img
                    src={img.url}
                    alt={img.label}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      // Fallback if image fails to load
                      (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect width="100" height="100" fill="%23ddd"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%23999"%3E🐿️%3C/text%3E%3C/svg%3E';
                    }}
                  />
                  {selectedDefaultImage === img.url && (
                    <div className="absolute inset-0 bg-blue-500 bg-opacity-20 flex items-center justify-center">
                      <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="relative mb-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">OR</span>
            </div>
          </div>

          {/* File Upload */}
          <div>
            <p className="text-xs text-gray-500 mb-2">Upload your own image:</p>
            <input
              id="image"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            {imageFile && (
              <div className="mt-2 text-sm text-gray-600">
                Selected: {imageFile.name}
              </div>
            )}
          </div>
        </div>

        <div className="flex space-x-3">
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {isSubmitting ? 'Creating...' : 'Create Pin'}
          </button>
        </div>
      </form>
    </div>
  );
}

