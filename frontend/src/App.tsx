import { useState } from 'react';
import { Filters } from './components/Filters';
import { EventsList } from './components/EventsList';
import { EventsMap } from './components/EventsMap';
import { useEvents } from './hooks/useEvents';
import type { EventFilters } from './api/client';
import './styles.css';

export default function App() {
  const [filters, setFilters] = useState<EventFilters>({ page: 1 });
  const { events, loading, error } = useEvents(filters);

  const useMyLocation = () => {
    navigator.geolocation.getCurrentPosition((position) => {
      const near = `${position.coords.latitude},${position.coords.longitude}`;
      setFilters((prev) => ({ ...prev, near, radius: prev.radius || 50 }));
    });
  };

  return (
    <main className="container">
      <h1>Próximas carreras en Galicia</h1>
      <Filters filters={filters} setFilters={setFilters} useMyLocation={useMyLocation} />
      {loading && <p>Cargando eventos...</p>}
      {error && <p>Error: {error}</p>}
      <EventsMap events={events} />
      <EventsList events={events} />
      <div className="pagination">
        <button disabled={(filters.page || 1) <= 1} onClick={() => setFilters({ ...filters, page: (filters.page || 1) - 1 })}>
          Anterior
        </button>
        <span>Página {filters.page || 1}</span>
        <button onClick={() => setFilters({ ...filters, page: (filters.page || 1) + 1 })}>Siguiente</button>
      </div>
    </main>
  );
}
