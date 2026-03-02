import type { EventItem } from '../types/event';

interface Props {
  events: EventItem[];
}

export function EventsList({ events }: Props) {
  if (!events.length) return <p>No hay carreras con estos filtros.</p>;

  return (
    <ul className="events-list">
      {events.map((event) => (
        <li key={event.id}>
          <h3>{event.name}</h3>
          <p>
            {new Date(event.date).toLocaleDateString()} · {event.distance_km} km · {event.type}
          </p>
          <p>{event.location}</p>
          <a href={event.source_url} target="_blank" rel="noreferrer">
            Enlace original
          </a>
        </li>
      ))}
    </ul>
  );
}
