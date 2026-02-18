import { useEffect, useState } from 'react';
import { fetchEvents, type EventFilters } from '../api/client';
import type { EventItem } from '../types/event';

export function useEvents(filters: EventFilters) {
  const [events, setEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchEvents(filters)
      .then((data) => {
        setEvents(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [JSON.stringify(filters)]);

  return { events, loading, error };
}
