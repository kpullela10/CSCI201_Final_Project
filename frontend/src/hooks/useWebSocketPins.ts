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
  const isMountedRef = useRef(true);
  const MAX_RECONNECT_ATTEMPTS = 5;

  const fetchPins = useCallback(async () => {
    if (!isMountedRef.current) return;
    
    try {
      setIsLoading(true);
      const fetchedPins = filter === 'my' ? await getMyPins() : await getWeeklyPins();
      if (isMountedRef.current) {
        setPins(fetchedPins);
      }
    } catch (error) {
      console.error('Failed to fetch pins:', error);
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  }, [filter]);

  const startPolling = useCallback(() => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    pollIntervalRef.current = window.setInterval(() => {
      fetchPins();
    }, 30000);
  }, [fetchPins]);

  const connectWebSocket = useCallback(() => {
    // Don't create new connection if one already exists and is open
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const token = localStorage.getItem('authToken');
    
    if (!token) {
      console.log('No auth token available, waiting...');
      // Try again after a short delay
      reconnectTimeoutRef.current = window.setTimeout(() => {
        if (isMountedRef.current) {
          connectWebSocket();
        }
      }, 1000);
      return;
    }

    const wsUrl = `${WS_URL}/ws/pins?token=${token}`;

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        if (!isMountedRef.current) {
          ws.close();
          return;
        }
        
        setIsConnected(true);
        reconnectAttemptsRef.current = 0;
        console.log('WebSocket connected successfully');
        
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
        }
      };

      ws.onmessage = (event) => {
        if (!isMountedRef.current) return;
        
        try {
          const data = JSON.parse(event.data);
          const newPins = Array.isArray(data) ? data : [data];

          setPins((prevPins) => {
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
        if (ws.readyState === WebSocket.CONNECTING) {
          console.error('Error during connection attempt');
        }
        setIsConnected(false);
      };

      ws.onclose = (event) => {
        if (!isMountedRef.current) return;
        
        setIsConnected(false);
        console.log(`WebSocket closed (code: ${event.code}, reason: ${event.reason || 'none'}, wasClean: ${event.wasClean})`);
        
        if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          reconnectAttemptsRef.current += 1;
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000);
          console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttemptsRef.current})`);
          
          reconnectTimeoutRef.current = window.setTimeout(() => {
            if (isMountedRef.current) {
              connectWebSocket();
            }
          }, delay);
        } else {
          console.log('Max reconnect attempts reached, falling back to polling');
          startPolling();
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setIsConnected(false);
      startPolling();
    }
  }, [startPolling]);

  // Fetch pins when filter changes
  useEffect(() => {
    fetchPins();
  }, [fetchPins]);

  // Initialize WebSocket connection on mount
  useEffect(() => {
    isMountedRef.current = true;
    

    const initTimeout = setTimeout(() => {
      if (isMountedRef.current) {
        connectWebSocket();
      }
    }, 100);

    return () => {
      isMountedRef.current = false;
      clearTimeout(initTimeout);
      
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connectWebSocket]);

  const filteredPins = useMemo(() => {
    if (filter === 'my' && user) {
      return pins.filter((pin) => pin.userID === user.userID);
    }
    return pins;
  }, [pins, filter, user]);

  return { pins: filteredPins, isConnected, isLoading };
}