import { useEffect, useRef, useState, useMemo, useCallback } from 'react';
import type { Pin } from '../types';
import { getWeeklyPins, getMyPins } from '../api/pins';
import { useAuth } from './useAuth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
const WS_URL = API_BASE_URL.replace(/^http/, 'ws');

export function useWebSocketPins(filter: 'all' | 'my' = 'all') {
  const [pins, setPins] = useState<Pin[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useAuth();
  const wsRef = useRef<WebSocket | null>(null);
  const pollIntervalRef = useRef<number | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const MAX_RECONNECT_ATTEMPTS = 5;

  const fetchPins = useCallback(async () => {
    try {
      setIsLoading(true);
      const fetchedPins = filter === 'my' ? await getMyPins() : await getWeeklyPins();
      setPins(fetchedPins);
    } catch (error) {
      console.error('Failed to fetch pins:', error);
    } finally {
      setIsLoading(false);
    }
  }, [filter]);

  const startPolling = () => {
    // Poll every 30 seconds as fallback
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    pollIntervalRef.current = window.setInterval(async () => {
      await fetchPins();
    }, 30000);
  };

  const connectWebSocket = () => {
    const token = localStorage.getItem('authToken');
    const wsUrl = token
      ? `${WS_URL}/ws/pins?token=${token}`
      : `${WS_URL}/ws/pins`;

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setIsConnected(true);
        reconnectAttemptsRef.current = 0;
        console.log('WebSocket connected');
        // Clear polling if WebSocket is connected
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
        }
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const newPins = Array.isArray(data) ? data : [data];

          setPins((prevPins) => {
            // Merge new pins without duplicates
            const pinMap = new Map(prevPins.map((pin) => [pin.pinID, pin]));
            newPins.forEach((pin: Pin) => {
              pinMap.set(pin.pinID, pin);
            });
            return Array.from(pinMap.values());
          });
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      ws.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket disconnected, falling back to polling');
        
        // Try to reconnect if we haven't exceeded max attempts
        if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          reconnectAttemptsRef.current += 1;
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000);
          reconnectTimeoutRef.current = window.setTimeout(() => {
            connectWebSocket();
          }, delay);
        } else {
          // Start polling as fallback after max reconnect attempts
          startPolling();
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setIsConnected(false);
      startPolling();
    }
  };

  // Fetch pins when filter changes
  useEffect(() => {
    fetchPins();
  }, [filter]);

  useEffect(() => {
    // Initial fetch
    fetchPins();

    // Try to establish WebSocket connection
    connectWebSocket();

    // Cleanup
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  // Filter pins based on filter type (already handled by API, but double-check)
  const filteredPins = useMemo(() => {
    if (filter === 'my' && user) {
      return pins.filter((pin) => pin.userID === user.userID);
    }
    return pins;
  }, [pins, filter, user]);

  return { pins: filteredPins, isConnected, isLoading };
}

