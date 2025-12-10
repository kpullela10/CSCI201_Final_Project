import { useEffect, useRef, useState, useMemo, useCallback } from 'react';
import type { Pin } from '../types';
import { getWeeklyPins, getMyPins } from '../api/pins';
import { useAuth } from './useAuth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
const WS_URL = API_BASE_URL.replace(/^https?/, (protocol) => protocol === 'https' ? 'wss' : 'ws');

const POLL_INTERVAL_MS = 30000;
const INITIAL_RECONNECT_DELAY_MS = 1000;
const MAX_RECONNECT_DELAY_MS = 30000;
const MAX_RECONNECT_ATTEMPTS = 5;
const AUTH_RETRY_DELAY_MS = 1000;
const INIT_DELAY_MS = 100;

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

  const fetchPins = useCallback(async () => {
    if (!isMountedRef.current) return;
    
    try {
      setIsLoading(true);
      const fetchedPins = filter === 'my' ? await getMyPins() : await getWeeklyPins();
      if (isMountedRef.current) {
        setPins(fetchedPins);
      }
    } catch {
      // Network error, will retry on next poll
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
    }, POLL_INTERVAL_MS);
  }, [fetchPins]);

  const connectWebSocket = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const token = localStorage.getItem('authToken');
    
    if (!token) {
      reconnectTimeoutRef.current = window.setTimeout(() => {
        if (isMountedRef.current) {
          connectWebSocket();
        }
      }, AUTH_RETRY_DELAY_MS);
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
        } catch {
          // Invalid message format, ignore
        }
      };

      ws.onerror = () => {
        setIsConnected(false);
      };

      ws.onclose = () => {
        if (!isMountedRef.current) return;

        setIsConnected(false);

        if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          reconnectAttemptsRef.current += 1;
          const delay = Math.min(
            INITIAL_RECONNECT_DELAY_MS * Math.pow(2, reconnectAttemptsRef.current),
            MAX_RECONNECT_DELAY_MS
          );

          reconnectTimeoutRef.current = window.setTimeout(() => {
            if (isMountedRef.current) {
              connectWebSocket();
            }
          }, delay);
        } else {
          startPolling();
        }
      };

      wsRef.current = ws;
    } catch {
      setIsConnected(false);
      startPolling();
    }
  }, [startPolling]);

  useEffect(() => {
    fetchPins();
  }, [fetchPins]);

  useEffect(() => {
    isMountedRef.current = true;

    const initTimeout = setTimeout(() => {
      if (isMountedRef.current) {
        connectWebSocket();
      }
    }, INIT_DELAY_MS);

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