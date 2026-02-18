import type { EventItem } from '../types/event';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export interface EventFilters {
  distanceMin?: number;
  distanceMax?: number;
  type?: string;
  from?: string;
  near?: string;
  radius?: number;
  page?: number;
}

export async function fetchEvents(filters: EventFilters): Promise<EventItem[]> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== '') params.set(key, String(value));
  });

  const response = await fetch(`${API_BASE}/events?${params.toString()}`);
  if (!response.ok) throw new Error('Could not fetch events');
  return response.json();
}
